# wifi 연결을 위한 네트워크 모듈
# json 처리 용 모듈
# ESP의 핀처리 모듈
# 서버와 통신을 위한 MQTT 프로토콜.(Socket.IO 대용으로 임베디드에서 주로 사용된다고 함)
# time 지연시간을 위한 모듈

# 순서 : 필요 라이브러리 임포트 -> 네트워크 설정 -> 하드웨어 설정 -> 함수 -> 로깅출력

import network
import ujson
from machine import Pin
from umqtt.simple import MQTTClient
import time

# 1. 하드웨어 설정
# GPIO 2번 핀을 출력 모드로 설정 (여기선 LED, 실제 팬 대용)
led_pin = Pin(2,Pin.OUT)

# 2. 네트워크 설정
WIFI_SSID = "Wokwi-GUEST"   #Wokwi 전용 WIFI SSID
WIFI_PASSWORD = ""          #Wokwi WIFI 는 비번 x

#AI 에이전트 서버가 메시지 발행할 주소 
MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "agri_log/robot/control/msm03"

# 3. 메시지 수신 시 실행될 함수
def on_message(topic,msg):
    # 서버로부터 받은 메시지를 출력
    print(f"AI 에이전트로 부터 메시지 수신 : {msg}")

    try:
        # 받은 메시지(json 형식)를 파이썬 딕셔너리로 변환
        data = ujson.loads(msg)
        action = data.get("action") # action 의 키값 가져오기

        # AI가 내린 명령에 따라 핀 제어
        if action =="FAN_ON":
            led_pin.value(1) #LED 켜기
            print("결과 : 냉각 팬 가동 시작")

        elif action == "FAN_OFF":
            led_pin.value(0) #LED 끄기
            print("결과 : 냉각 팬 정지")

    except Exception as e:
        print("메시지 해석 중 오류 발생 :",e)

# 4. WIFI 연결과정
print("WIFI 연결중 ...", end="")
sta_if  = network.WLAN(network.STA_IF) #스테이션 모드로 WIFI 활성
sta_if.active(True)
sta_if.connect(WIFI_SSID,WIFI_PASSWORD) #연결 시도

# 연결될 때까지 대기
while not sta_if.isconnected():
    print(".",end="")
    time.sleep(0.5)
print("\nWIFI 연결 완료!")

# 5. 서버 (MQTT Broker) 연결 설정
# 클라이언트 ID 는 중복되지 않게 esp32_robot_01 로 설정
client = MQTTClient("esp32_robot_01_msm03",MQTT_BROKER)
client.set_callback(on_message) # 메세지가 오면 on_message 함수를 실행하도록 설정
client.connect()                # 서버 접속
client.subscribe(MQTT_TOPIC)    # 정해진 통로(Topic)을 구독하여 메시지 대기 시작

print(f"서버 연결 성공! {MQTT_TOPIC} 채널에서 명령을 기다리는 중")

# 6. 무한 루프(메시지 수신 대기)
try : 
    while True:
        # 서버로부터 새로운 메시지가 왔는지 체크
        client.check_msg()
        # CPU 과부하 방지를 위해 짧게 쉬기
        time.sleep(0.1)
except Exception as e:
    print("연결 종료 :",e)

finally:
    client.disconnect() #비정상 종료 시 안전하게 연결 끊기
    
 