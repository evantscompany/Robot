import serial
import time
import sqlite3
import json

# 1. SQLite 데이터베이스 파일 및 테이블 생성
conn = sqlite3.connect('arduino_data.db',check_same_thread=False)
cursor = conn.cursor()
cursor.execute(
    '''
    create table if not exists robot_logs(
    id integer primary key autoincrement,
    device_id text,
    mcu_timestamp integer,
    status text,
    display_value integer,
    pc_rcv_time real)
'''
)
conn.commit()


# 아두이노와 연결된 포트번호 : COM5 -> 말벌모양에서 devices에서 확인 가능함.
try:
    py_serial = serial.Serial(port='COM5', baudrate=9600,timeout=1)

    print("시리얼 데이터 수집 시작 및 DB 실시간 기록중...")
    time.sleep(2) #통신 안정화를 위해 2초 대기

except Exception as e:
    print(f"포트 연결 실패 : {e}")
    exit()

time.sleep(2)

try:
    while True:
        # 아두이노가 데이터를 보냈는지 확인
        if py_serial.in_waiting >0:
            # 한줄 단위로 읽어오기
            raw_data = py_serial.readline().decode('utf-8').strip()

            try:
                # 아두이노가 보낸 문자열을 파이썬 딕셔너리(JSON) 변환
                data_json = json.loads(raw_data)

                # 가독성 위해 터미널에 출력
                print(f"[수신 및 파싱 성공]: {data_json}")

                # 데이터베이스에 매핑하여 INSERT
                cursor.execute('''
                    insert into robot_logs (device_id, mcu_timestamp, status, display_value, pc_rcv_time)
                    values (?,?,?,?,?)
                ''',(
                    data_json['device_id'],
                    data_json['mcu_timestamp'],
                    data_json['status'],
                    data_json['display_value'],
                    time.time() #PC가 데이터를 받은 실제 시간 추가
                ))
                conn.commit() #DB에 최종 반영
            
            except json.JSONDecodeError:
                # 통신 노이즈로 JSON 이 깨져서 들어오는 경우 예외처리
                print(f"[데이터 손실/노이즈 발생]:{raw_data}")


except KeyboardInterrupt:
    # Ctrl+C 를 누르면 안전하게 통신 종료
    py_serial.close()
    print("\n통신이 안전하게 종료되었습니다. DB에 저장이 완료되었습니다.")