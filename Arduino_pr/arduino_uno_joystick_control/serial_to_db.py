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