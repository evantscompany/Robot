import serial
import time
import json
import sqlite3

# 1. DB 테이블 구성 
conn = sqlite3.connect('robot_axis_data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
create table if not exists control_logs_axis (
               id integer primary key autoincrement,
               device_id text,
               joystick_x integer,
               mcu_timestamp integer,
               angle_x integer,
               pc_time real
    )
''')
conn.commit()

try:
    py_serial = serial.Serial(port='COM5', baudrate=9600,timeout=1)
    print("1방향 제어 시스템 가동!, 조이스틱 돌려보기")
    time.sleep(2)
except Exception as e:
    print(f"연결실패 :{e}")
    exit()

try:
    while True:
        if py_serial.in_waiting >0:
            raw_data = py_serial.readline().decode('utf-8').strip()

            # 버퍼에 데이터가 너무 많이 쌓여있으면
            # 과거의 밀린 데이터는 과감히 버리고 가장 최신 데이터만 읽도록 버퍼 청소

            if py_serial.in_waiting >2048:
                py_serial.reset_input_buffer()
                print("WARN - 시리얼 버퍼 오버플로우 감지 - 버퍼 초기화 수행")
                continue

            try:
                # 데이터 읽기 및 디코딩 에러 무시 처리
                raw_bytes = py_serial.readline()
                raw_data = raw_bytes.decode('utf-8',errors='ignore').strip()

                # 빈 데이터가 들어오면 아래 로직을 타지 않고 패스
                if not raw_data:
                    continue

                data_json = json.loads(raw_data)

                joy_x = int(data_json.get('joystick_x',512))
                mcu_time = int(data_json.get('mcu_timestamp',0))
                dev_id = data_json.get('device_id','UNKNOWN')

                # X축 모터 각도 매핑 및 클리핑 (정밀 연산)
                target_angle_x = int((joy_x / 1023.0) * 180)
                target_angle_x = max(0, min(180, target_angle_x))

                print(f"[수신] x:{joy_x:4d} -> [송신] 명령각도 x:{target_angle_x}도")

                # DB 저장 
                cursor.execute('''
                    INSERT INTO control_logs_axis (device_id, joystick_x, mcu_timestamp, angle_x, pc_time)
                    VALUES (?, ?, ?, ?, ?)
                ''', (dev_id, joy_x, mcu_time, target_angle_x, time.time()))
                conn.commit()

                # 아두이노로 명령 송신
                cmd_json = f'{{"angle_x":{target_angle_x}}}\n'
                py_serial.write(cmd_json.encode('utf-8'))
            
            except json.JSONDecodeError:
                # 데이터가 잘리거나 깨져서 JSON 파싱에 실패해도 그냥 다음 루프로 통과
                pass
            except KeyError as ke:
                # 딕셔너리 키 에러 방어
                print(f"[데이터 누락 패스]: {ke}")
                pass
            except UnicodeDecodeError:
                # 순간적인 노이즈로 바이트 디코딩이 꺠진 경우 방어
                pass
            try:
                data_json = json.loads(raw_data)
                joy_x = data_json['joystick_x']
                mcu_time = data_json['mcu_timestamp']
                dev_id = data_json['device_id']
                
                target_angle_x = int((joy_x / 1023.0) * 180)
                # x축 모터 각도 매핑 계산
                target_angle_x = max(0, min(180,target_angle_x))

                print(f"[수신] x:{joy_x:4d} -> [송신] 명령각도 x:{target_angle_x}도")

                # DB 저장 
                cursor.execute('''
                    INSERT INTO control_logs_axis (device_id, joystick_x, mcu_timestamp, angle_x, pc_time)
                    VALUES (?, ?, ?, ?, ?)
                ''', (dev_id, joy_x, mcu_time, target_angle_x, time.time()))
                conn.commit()

                # 아두이노로 명령 송신
                cmd_json = f'{{"angle_x":{target_angle_x}}}\n'
                py_serial.write(cmd_json.encode('utf-8'))
            
            except json.JSONDecodeError:
                pass

except KeyboardInterrupt:
    py_serial.close()
    conn.close()
    print("\n시스템 종료")