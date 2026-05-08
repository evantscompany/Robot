# app/services/hardware.py

try:
    # RPi.GPIO는 라즈베리 파이 같은 ARM 보드에서만 작동하는 라이브러리입니다.
    import RPi.GPIO as GPIO
except ImportError:
    # 윈도우나 Mac처럼 GPIO 라이브러리를 쓸 수 없는 환경을 위해 '가짜(Mock)' 클래스를 만듭니다.
    # 이렇게 하면 PC에서도 에러 없이 프로그램이 실행됩니다.
    class GPIO:
        BCM = 11  # 핀 번호를 CPU 기준으로 읽겠다는 설정값
        OUT = 1   # 핀을 출력 모드로 쓰겠다는 설정값
        HIGH = 1  # 3.3V 전압을 보내라는 신호
        LOW = 0   # 전압을 끊으라는 신호
        
        @staticmethod
        def setmode(mode): pass  # 실제 동작 대신 '무시'하고 넘어갑니다.
        @staticmethod
        def setup(pin, mode): pass
        @staticmethod
        def output(pin, value): 
            # 실제로 전기를 보내는 대신 터미널에 결과를 찍어줍니다.
            print(f"[하드웨어 시뮬레이션] {pin}번 핀의 상태를 {value}로 변경했습니다.")
        @staticmethod
        def cleanup(): pass

# 우리가 제어할 LED가 연결된 핀 번호 (18번)
LED_PIN = 18

class HardwareService:
    """
    하드웨어 제어와 관련된 모든 기능을 모아둔 클래스입니다.
    이 클래스 덕분에 백엔드 본체(main.py)는 복잡한 하드웨어 지식을 몰라도 됩니다.
    """
    def __init__(self):
        # 클래스가 생성될 때 초기 설정을 진행합니다.
        GPIO.setmode(GPIO.BCM)      # 핀 번호 체계 설정
        GPIO.setup(LED_PIN, GPIO.OUT) # 18번 핀을 전기를 내보내는(출력) 용도로 쓰겠다고 설정

    def set_led(self, status: bool):
        """
        LED 상태를 변경하는 함수
        :param status: True면 켜고, False면 끕니다.
        """
        # True면 HIGH(전압 ON), False면 LOW(전압 OFF) 값을 선택
        value = GPIO.HIGH if status else GPIO.LOW
        GPIO.output(LED_PIN, value)  # 하드웨어 핀에 전기 신호 전달
        return {"status": "success", "led_on": status}

    def get_sensor_data(self):
        """
        센서 값을 읽어오는 함수 (현재는 가짜 데이터를 무작위로 생성)
        """
        import random
        # 실제 환경에서는 여기서 센서 드라이버를 호출해 값을 가져옵니다.
        return {"temperature": round(random.uniform(20.0, 30.0), 2)}

# 다른 파일(main.py)에서 이 기술자를 바로 부를 수 있도록 미리 인스턴스를 하나 만들어둡니다.
hardware_service = HardwareService()