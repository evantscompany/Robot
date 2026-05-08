# 순서
# LED 연결 설정 -> 와이파이 연결 설정 -> 서버상태 체크 및 제어

import network
import urequests
import time
from machine import Pin

# 1. LED 연결 설정 (GPIO 2번핀)
led = Pin(2,Pin.OUT)

# 2. 와이파이 연결 설정
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASS = ""

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("연결중...")
        wlan.connect(WIFI_SSID,WIFI_PASS)
        while not wlan.isconnected():
            pass
    print("WIFI 연결 완료", wlan.ifconfig())

# 3. 서버 상태 체크 및 제어
SERVER_URL = "http://bulb-plural-lushly.ngrok-free.dev/get-led"

connect_wifi() #connect_WIFI 함수 호출

while True:
    try:
        # 서버에 GET요청
        response = urequests.get(SERVER_URL)
        data= response.json() #json 파싱

        # 서버에서 온 상태값 확인
        status = data.get("led")
        print("현재 LED 상태: ", status)

        if status =="ON":
            led.value(1) 
        else:
            led.value(0)
        
        response.close() #메모리 관리를 위해 닫아주기
    
    except Exception as e:
        print("에러발생 :",e)
    
    time.sleep(1)