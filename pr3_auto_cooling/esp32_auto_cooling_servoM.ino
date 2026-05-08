import network
import urequests
import time
from machine import Pin , ADC, PWM

# 1. 설정
led = Pin(2,Pin.OUT)
adc = ADC(Pin(4)) #가변저항 연결핀
adc.atten(ADC.ATTN_11DB) #0~3.3V 범위를 읽기 위한 설정

# 서보모터 설정
servo = PWM(Pin(18),freq=50) #서보는 보통 50Hz 사용

def set_servo_angle(angle):
    # 각도 0~180을 PWM 듀티 사이클로 변환 (약 20~120 사이 값)
    duty = int((angle/180*100)+20)
    servo.duty(duty)


WIFI_SSID = "Wokwi-GUEST"
WIFI_PASS = ""

BASE_URL="http://bulb-plural-lushly.ngrok-free.dev"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID,WIFI_PASS)
    while not wlan.isconnected():pass
    print("Wifi Connected")

connect_wifi()

while True:
    try:
        # 1. 온도 읽기 (0~4095 값을 0~100도로 변환)
        val = adc.read()
        temp = int((val/4095)*100)

        # 온도에 따른 서보모터 각도 조절 (밸브 제어)
        # 온도 30도면 0도, 100도면 180도 열리게 계산
        angle=max(0,min(180,(temp-30)*2.5))
        set_servo_angle(angle)


        # 2. 서버에 온도 전송 (POST)
        urequests.post(f"{BASE_URL}/update", json={"temp":temp})

        # 3. 서버에서 명령 수신(GET)
        res = urequests.get(f"{BASE_URL}/command")
        command=res.json()

        print(f"온도 : {temp}도, 밸브각도: {int(angle)} 명령 :{command['led']}")

        # 4. 명령에 따라 LED 제어
        if command['led'] =='ON':
            led.value(1)
        else:
            led.value(0)

        res.close()
    except Exception as e:
        print("Error:", e)
    time.sleep(1)
