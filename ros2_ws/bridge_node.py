import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial
import json
import time

class ArduinoSerialBridge(Node):
    def __init__(self):
        super().__init__('arduino_serial_bridge')
        
        # 1. ROS 2 퍼블리셔 및 서브스크라이버 설정
        # 조이스틱 원시값을 세상에 알릴 토픽 발행자
        self.joy_pub = self.create_publisher(Int32, '/joystick_raw', 10)
        
        # 모터 명령 각도를 받아올 토픽 구독자
        self.motor_sub = self.create_subscription(Int32, '/motor_cmd', self.motor_cmd_callback, 10)

        # 2. 시리얼 포트 초기화 (오전 설정을 리눅스 환경에 맞게 매핑)
        try:
            self.py_serial = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=0.1)
            time.sleep(2) # 아두이노 부팅 대기 안정화
            self.get_logger().info('✅ 아두이노 시리얼 포트 연결 성공 (/dev/ttyACM0)')
        except Exception as e:
            self.get_logger().error(f'❌ 아두이노 연결 실패: {e}')
            exit()

        # 3. 데이터 수집을 위한 ROS 2 타이머 루프 생성 (100ms 주기로 구동 = 10Hz)
        self.timer = self.create_timer(0.1, self.serial_receive_loop)

    def serial_receive_loop(self):
        """아두이노에서 오는 조이스틱 데이터를 수신하여 ROS 2 토픽으로 발행하는 루프"""
        try:
            if self.py_serial.in_waiting > 0:
                # 오전 실습에서 검증된 버퍼 오버플로우 방어 코드
                if self.py_serial.in_waiting > 2048:
                    self.py_serial.reset_input_buffer()
                    return

                raw_bytes = self.py_serial.readline()
                raw_data = raw_bytes.decode('utf-8', errors='ignore').strip()

                if not raw_data:
                    return

                # JSON 디코딩 및 결측치 방어
                data_json = json.loads(raw_data)
                joy_x = int(data_json.get('joystick_x', 512))

                # ROS 2 표준 메시지에 데이터 담기
                msg = Int32()
                msg.data = joy_x
                
                # 토픽 발행! (/joystick_raw 토픽으로 데이터가 날아갑니다)
                self.joy_pub.publish(msg)
                self.get_logger().info(f'🎰 [시리얼->ROS2] 조이스틱 수신: {joy_x}')

        except json.JSONDecodeError:
            pass
        except Exception as e:
            self.get_logger().warn(f'수신 루프 에러 발생: {e}')

    def motor_cmd_callback(self, msg):
        """ROS 2 시스템에서 계산된 제어 명령 각도를 받아 아두이노로 쏴주는 콜백 함수"""
        target_angle = msg.data
        
        # 하드웨어 보호용 클리핑
        target_angle = max(0, min(180, target_angle))
        
        # 아두이노 규격 JSON 명령어 조립
        cmd_json = f'{{"angle_x":{target_angle}}}\n'
        
        try:
            self.py_serial.write(cmd_json.encode('utf-8'))
            self.get_logger().info(f'⚙️ [ROS2->시리얼] 모터 명령 송신: {target_angle}도')
        except Exception as e:
            self.get_logger().error(f'시리얼 송신 실패: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = ArduinoSerialBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.py_serial.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()