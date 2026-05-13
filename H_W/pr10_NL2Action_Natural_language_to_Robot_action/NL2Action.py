import openai
import paho.mqtt.client as mqtt #wokwi와 통신하기 위한 mqtt 라이브러리
import json
import dotenv
import os

dotenv.load_dotenv()

# 1. 설정정보
# wokwi 코드와 반드시 동일한 브로커와 토픽 사용
MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "agri_log/robot/control/msm03"
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

# 2. MQTT 클라이언트 설정 (서버가 명령을 보내는 '송신기' 력할)
try :
    client= mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
except:
    client = mqtt.Client()

client.connect(MQTT_BROKER, 1883,60)
client.loop_start()
print(f"MQTT 서버 연결 완료 : {MQTT_BROKER}")

# 3. AI 판단 및 명령 전송함수
def ask_ai_and_control(user_text):
    print(f"\n[사용자 입력] : {user_text}")

    # OPENAI API 를 사용하여 사용자의 의도를 분석
    # 판단형 기능을 수행하도록 프롬프트 설계

    from openai import OpenAI
    ai_client= OpenAI(api_key=OPENAI_API_KEY)

    system_instruction= """
    당신은 농업용 로봇 제어 에이전트 입니다. 
    사용자의 말을 듣고 다음 두가지 중 하나를 결정하세요.
    1. 팬을 켜야 하는 상황이면 JSON 으로 {"action": "FAN_ON"}을 출력
    2. 팬을 꺼야하는 상황이면 JSON으로 {"action":"FAN_OFF"}를 출력
    그 외의 대답은 절대 하지 마시오.

    """

    # AI에게 판단 요청
    response = ai_client.chat.completions.create(
        model = "gpt-4o",
        response_format={"type":"json_object"}
        messages=[
            {"role": "system", "content":system_instruction},
            {"role": "user", "content": user_text}
        ]
    )

    # AI가 뱉은 JSON 문자열을 가져오기.
    ai_decision = response.choices[0].message.content
    print(f"[AI 판단 결과]:{ai_decision}")

    try :
        # AI의 판단이 올바른 JSON 인지 확인 작업
        command_data = json.loads(ai_decision)

        # 4. Wokwi(ESP32)로 명령 전송
        # MQTT 토픽으로 JSON 데이터를 발행(Publish)
        client.publish(MQTT_TOPIC,json.dumps(command_data))
        print(f"결과 : {MQTT_TOPIC} 채널로 제어 명령을 전송")

    except Exception as e:
        print("AI가 유효하지 않은 명령을 생성했습니다. ",e)

# 5. 실행 루프
print("AI 로봇 에이전트가 가동되었습니다. 명령을 입력하세요 (종료 : q)")
while True:
    user_input = input("명령 입력 >")
    if user_input.lower()=='q':
        break

    # AI판단 및 제어 함수 실행
    ask_ai_and_control(user_input)

client.disconnect()
