import network
from machine import Pin
import ujson
from umqtt.simple import MQTTClient
import time
import dht

#1. 하드웨어 설정
led_pin = Pin(2,Pin.OUT)
sensor = dht.DHT22(Pin(15))

#2. 설정 정보
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""
MQTT_BROKER = "broker.hivemq.com"
TOPIC_CONTROL = "agri_log/robot/control/msm03"
TOPIC_STATUS = "agri_log/robot/status/msm03"

# 3. 명령어 수신 (call back 함수)
def on_message(topic,msg):
    print(f"\n[서버 명령 수신] : {msg}")
    try:
        data = ujson.loads(msg)
        if data.get("action") == "FAN_ON":
            led_pin.value(1)
            print(">>>결과 : 팬 가동 (LED_ON)")
        elif data.get("action")=="FAN_OFF":
            led_pin.value(0)
            print(">>>결과 : 팬 정지")
    except Exception as e:
        print("명령 해석 오류 :" ,e)

#4. WIFI 및 MQTT 연결
print("WIFI 연결중 ...", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(WIFI_SSID,WIFI_PASSWORD)
while not sta_if.isconnected(): time.sleep(0.5)
print("완료")

client = MQTTClient("esp32_msm03_auto",MQTT_BROKER)
client.set_callback(on_message)

try:
    client.connect()
    client.subscribe(TOPIC_CONTROL)
    print("MQTT 서버 연결 및 구독 성공")
except Exception as e:
    print("MQTT 연결 실패", e)


# 5. 메인 루프(5초마다 상태보고)
last_report = 0
try:
    while True:
        client.check_msg() #명령 대기

        if time.time() - last_report >=5:
            try:
                sensor.measure()
                temp = sensor.temperature()
                hum = sensor.humidity()

                status ={
                    "temperature":temp,
                    "humidity":hum,
                    "fan_status":"ON" if led_pin.value(1) else "OFF"

                }
                client.publish(TOPIC_STATUS,ujson.dumps(status))
                print(f"상태보고 : {temp}도,{hum}%")
                last_report=time.time()
            
            except:
                print("센서 읽기 실패")

        time.sleep(0.1)

finally:
    client.disconnect()