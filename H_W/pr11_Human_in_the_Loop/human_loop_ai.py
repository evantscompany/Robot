import openai
import paho.mqtt.client as mqtt
import json
import dotenv
import os
import speech_recognition as sr # 음성 인식 라이브러리

dotenv.load_dotenv()

#설정 
MQTT_BROKER = "broker.hivemq.com"
TOPIC_CONTROL = "agri_log/robot/control/msm03"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#MQTT 설정
try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
except:
    client = mqtt.Client()
    
client.connect(MQTT_BROKER, 1883,60)
client.loop_start()

#음성 인식기 초기화 
recognizer = sr.Recognizer()
mic = sr.Microphone()

def listen_voice():
    with mic as source:
        print("\n 말씀하세요.. (듣고 있습니다)")
        recognizer.adjust_for_ambient_noise(source) 
        audio = recognizer.listen(source)

        try : 
            text = recognizer.recognize_google(audio,language='ko-KR')
            print(f"인식된 문장 {text}")
            return text
        except:
            print("목소리를 이해하지 못했습니다.")
            return None

def ask_ai_and_control(user_text):
    from openai import OpenAI
    ai_client = OpenAI(api_key=OPENAI_API_KEY)

    system_instruction = """
    당신은 농업용 로봇 제어 에이전트입니다. 사용자의 음성을 분석하여 JSON으로 응답하세요.
    1. 팬 켜기: {"action": "FAN_ON", "msg": "팬을 가동합니다."}
    2. 팬 끄기: {"action": "FAN_OFF", "msg": "팬을 정지합니다."}
    반드시 JSON만 출력하세요.

    """

    response = ai_client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_text}
        ]
    )

    res = json.loads(response.choices[0].message.content)
    print(f"AI 파단 : {res['msg']}")

    # 승인절차
    confirm = input(f"[{res['action']}] 실행 할까요? (y/n):")
    if confirm.lower()=="y":
        client.publish(TOPIC_CONTROL,json.dumps({"action":res["action"]}))
        print("명령 전송완료")

print("음성 제어 시스템 가동 ")

try:
    while True:
        input("\n [Enter를 누르면 음성 인식을 시작합니다]")
        vocie_text = listen_voice()

        if vocie_text:
            ask_ai_and_control(vocie_text)

except KeyboardInterrupt:
    print("시스템 종료")
finally:
    client.disconnect()

# 아두이노로 실습 진행