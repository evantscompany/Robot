import asyncio
import json
import sqlite3
import threading
import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

import serial
from contextlib import asynccontextmanager


# =========================================================
# 웹소켓 접속 클라이언트 관리 매니저
# =========================================================
class ConnectionManager:

    def __init__(self):
        # 현재 접속중인 websocket 클라이언트 저장 리스트
        self.active_connections: list[WebSocket] = []

    # 클라이언트 연결 처리
    async def connect(self, websocket: WebSocket):

        # websocket 연결 승인
        await websocket.accept()

        # 활성 연결 리스트에 등록
        self.active_connections.append(websocket)

    # 클라이언트 연결 해제 처리
    def disconnect(self, websocket: WebSocket):

        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    # 현재 접속한 모든 클라이언트에게 데이터 브로드캐스트
    async def broadcast(self, message: str):

        for connection in self.active_connections:

            try:
                await connection.send_text(message)

            except Exception as e:
                print(f"[ERROR] 웹소켓 브로드캐스트 실패 : {e}")

                # 연결이 끊긴 websocket 제거
                self.disconnect(connection)


# 전역 매니저 객체 생성
manager = ConnectionManager()


# =========================================================
# 데이터베이스 초기화
# =========================================================
def init_db():

    # with 사용 시 자동 close 처리
    with sqlite3.connect('robot_axis_data.db') as conn:

        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS control_logs_axis(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                device_id TEXT,

                joystick_x INTEGER,

                mcu_timestamp INTEGER,

                angle_x INTEGER,

                pc_time REAL
            )
        ''')

        conn.commit()


# =========================================================
# 백그라운드 시리얼 수집 스레드
# =========================================================
def serial_reader_thread(loop):

    # 서버 시작 시 DB 초기화
    init_db()

    # -----------------------------------------------------
    # 시리얼 포트 연결
    # -----------------------------------------------------
    try:

        py_serial = serial.Serial(
            port='COM5',
            baudrate=9600,
            timeout=1
        )

        # 아두이노 자동 리셋 안정화 대기
        time.sleep(2)

        print('[INFO] 아두이노 시리얼 포트 연결 성공')

    except Exception as e:

        print(f"[CRITICAL ERROR] 시리얼 포트 연결 실패 : {e}")

        return

    # -----------------------------------------------------
    # 무한 데이터 수집 루프
    # -----------------------------------------------------
    while True:

        try:

            # 읽을 데이터가 존재하는 경우
            if py_serial.in_waiting > 0:

                # -------------------------------------------------
                # 버퍼 오버플로우 방어
                # -------------------------------------------------
                if py_serial.in_waiting > 2048:

                    py_serial.reset_input_buffer()

                    continue

                # -------------------------------------------------
                # 시리얼 데이터 읽기
                # -------------------------------------------------
                raw_bytes = py_serial.readline()

                # bytes → 문자열 변환
                raw_data = raw_bytes.decode(
                    'utf-8',
                    errors='ignore'
                ).strip()

                # 빈 문자열 방어
                if not raw_data:
                    continue

                # -------------------------------------------------
                # JSON 파싱
                # -------------------------------------------------
                data_json = json.loads(raw_data)

                # 안전한 key 접근
                joy_x = int(data_json.get('joystick_x', 512))

                mcu_time = int(
                    data_json.get('mcu_timestamp', 0)
                )

                dev_id = data_json.get(
                    'device_id',
                    'UNKNOWN'
                )

                # -------------------------------------------------
                # 조이스틱 → 서보각도 변환
                # 0~1023 → 0~180
                # -------------------------------------------------
                target_angle_x = int(
                    (joy_x / 1023.0) * 180
                )

                # 소프트웨어 클리핑
                target_angle_x = max(
                    0,
                    min(180, target_angle_x)
                )

                # -------------------------------------------------
                # SQLite 데이터 저장
                # -------------------------------------------------
                with sqlite3.connect(
                    'robot_axis_data.db'
                ) as conn:

                    cursor = conn.cursor()

                    cursor.execute('''
                        INSERT INTO control_logs_axis(

                            device_id,
                            joystick_x,
                            mcu_timestamp,
                            angle_x,
                            pc_time

                        )
                        VALUES(?,?,?,?,?)
                    ''', (

                        dev_id,
                        joy_x,
                        mcu_time,
                        target_angle_x,
                        time.time()

                    ))

                    conn.commit()

                # -------------------------------------------------
                # 프론트엔드 실시간 전송 패킷
                # -------------------------------------------------
                payload = {

                    "device_id": dev_id,

                    "joystick_x": joy_x,

                    "mcu_timestamp": mcu_time,

                    "angle_x": target_angle_x
                }

                # -------------------------------------------------
                # FastAPI 메인 이벤트 루프에
                # websocket 브로드캐스트 위임
                # -------------------------------------------------
                asyncio.run_coroutine_threadsafe(

                    manager.broadcast(
                        json.dumps(payload)
                    ),

                    loop
                )

                # -------------------------------------------------
                # Arduino로 제어 명령 송신
                # -------------------------------------------------
                cmd_json = (
                    f'{{"angle_x":{target_angle_x}}}\n'
                )

                py_serial.write(
                    cmd_json.encode('utf-8')
                )

        # -----------------------------------------------------
        # JSON 파싱 실패 시 무시
        # -----------------------------------------------------
        except json.JSONDecodeError:

            pass

        # -----------------------------------------------------
        # 기타 예외 처리
        # -----------------------------------------------------
        except Exception as e:

            print(
                f"[WARN] 백그라운드 시리얼 루프 예외 : {e}"
            )

            time.sleep(1)


# =========================================================
# FastAPI lifespan 관리
# startup / shutdown
# =========================================================
@asynccontextmanager
async def lifespan(app: FastAPI):

    # -----------------------------------------------------
    # Startup 영역
    # -----------------------------------------------------
    print('[SYSTEM] FastAPI 서버 시작')

    # 현재 FastAPI 메인 이벤트 루프 참조 확보
    loop = asyncio.get_running_loop()

    # 앱 객체에 loop 저장
    app.state.loop = loop

    # -----------------------------------------------------
    # 시리얼 수집 스레드 시작
    # -----------------------------------------------------
    serial_thread = threading.Thread(

        target=serial_reader_thread,

        args=(loop,),

        daemon=True
    )

    serial_thread.start()

    # -----------------------------------------------------
    # 서버 운영 영역
    # -----------------------------------------------------
    yield

    # -----------------------------------------------------
    # Shutdown 영역
    # -----------------------------------------------------
    print('[SYSTEM] FastAPI 서버 종료 시작')

    print('[SYSTEM] 자원 정리 완료')


# =========================================================
# FastAPI 앱 생성
# =========================================================
app = FastAPI(lifespan=lifespan)


# =========================================================
# CORS 설정
# 프론트엔드 통신 허용
# =========================================================
app.add_middleware(

    CORSMiddleware,

    allow_origins=['*'],

    allow_credentials=True,

    allow_methods=['*'],

    allow_headers=['*']
)


# =========================================================
# WebSocket Endpoint
# =========================================================
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    # 클라이언트 연결 등록
    await manager.connect(websocket)

    try:

        # 연결 유지 루프
        while True:

            # 클라이언트 메시지 수신 대기
            # (연결 유지 목적)
            await websocket.receive_text()

    # websocket 연결 종료 처리
    except WebSocketDisconnect:

        manager.disconnect(websocket)