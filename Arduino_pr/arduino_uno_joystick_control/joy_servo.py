import serial
import json
import time

# 1. 시리얼 포트 설정 (WSL2 환경)
# 아두이노가 연결된 포트로 변경하세요 (예: /dev/ttyACM0)
SERIAL_PORT = 'COM5' 
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) # 아두이노 부팅 대기
    print(f"[{SERIAL_PORT}] 연결 성공! 조이스틱 제어 시작.")
except Exception as e:
    print(f"연결 실패: {e}")
    exit()

try:
    while True:
        if ser.in_waiting > 0:
            # 아두이노로부터 데이터 읽기
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue
            
            try:
                data = json.loads(line)
                joy_x = data.get('joystick_x')
                
                if joy_x is not None:
                    # 2. 매핑: 0~1023 -> 30~150 (코드의 constrain 범위)
                    angle = int((joy_x / 1023.0) * 120 + 30)
                    
                    # 3. 아두이노로 명령 전송
                    cmd = {"angle_x": angle}
                    ser.write((json.dumps(cmd) + "\n").encode('utf-8'))
                    print(f"Joy: {joy_x} -> Angle: {angle}")
                    
            except json.JSONDecodeError:
                continue

except KeyboardInterrupt:
    ser.close()
    print("종료되었습니다.")