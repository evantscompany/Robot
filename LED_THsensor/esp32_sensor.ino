# import network
# import urequests
# import time
# from machine import Pin



# # 1. 와이파이 연결 (Wokwi 가상 환경)
# print("Connecting to WiFi...")
# wifi = network.WLAN(network.STA_IF)
# wifi.active(True)
# wifi.connect('Wokwi-GUEST', '')

# while not wifi.isconnected():
#     print(".", end="")
#     time.sleep(0.5)
# print("\nWiFi Connected!")

# # 2. 내 ngrok 엔드포인트 주소
# # 반드시 /sensor 까지 붙여주세요!
# SERVER_URL = "http://bulb-plural-lushly.ngrok-free.dev/sensor"
# led = Pin(18, Pin.OUT)

# headers = {'ngrok-skip-browser-warning': '69420'}

# while True:
#     try:
#         # 내 PC의 FastAPI 서버에 "온도 값 줘!"라고 요청
#         print("Requesting sensor data...")
#         res = urequests.get(SERVER_URL, headers=headers)
        
#         if res.status_code == 200:
#             data = res.json()
#             temp = data['temperature']
#             print(f"Server Temp: {temp}C")
            
#             # 온도가 25도 이상이면 LED를 켭니다.
#             if temp >= 25.0:
#                 led.value(1)
#                 print("Action: LED ON")
#             else:
#                 led.value(0)
#                 print("Action: LED OFF")
        
#         res.close() # 요청 완료 후 세션 닫기
#     except Exception as e:
#         print("Error connecting to server:", e)
    
#     time.sleep(3) # 3초마다 반복

#------------------------------------------------------------------------- 

import network
import urequests
import time
from machine import Pin
import dht

# update-sensor api 연동
# 1. 연결설정
SERVER_URL_UPDATE="http://bulb-plural-lushly.ngrok-free.dev/update-sensor"
headers = {'ngrok-skip-browser-warning': 'true', 'Content-Type': 'application/json'}

# 2. 센서 및 LED 설정
sensor = dht.DHT22(Pin(15))
led=Pin(18,Pin.OUT)

# 1. 와이파이 연결 (Wokwi 가상 환경)
print("Connecting to WiFi...")
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect('Wokwi-GUEST', '')

while not wifi.isconnected():
    print(".", end="")
    time.sleep(0.5)
print("\nWiFi Connected!")

print("데이터 전송 시작")

while True:
    try:
        # 센서값 읽기
        sensor.measure()
        t=sensor.temperature()
        h=sensor.humidity()

        # 서버로 보낼 데이터 뭉치(json) 만들기
        payload={
            "temperature":t,
            "humidity":h
        }
        print(f"보내는 중 .. 온도 :{t}도, 습도{h}퍼센트")

        # POST요청으로 데이터 전송!
        res = urequests.post(SERVER_URL_UPDATE,json=payload,headers=headers)

        if res.status_code==200:
            print("서버 전송 성공")
            # 서버가 보낸 응답 확인
            if t>=30.0:
                led.value(1)
            else:
                led.value(0)
        res.close()
    
    except Exception as e:
        print("전송실패 :",e)
        time.sleep(5)