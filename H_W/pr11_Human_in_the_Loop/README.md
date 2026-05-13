# Human in the Loop

이 프로젝트는 음성 입력을 OpenAI로 분석하고, 사람이 최종 승인한 후 MQTT로 농업용 로봇 제어 명령을 전송합니다.

## 구성
- `human_loop_ai.py`: 음성 인식, AI 판단, 승인 후 MQTT 발행을 담당합니다.
- `esp32_human_Ai_action.ino`: ESP32 쪽 수신 및 액션 처리 코드입니다.

## 동작 흐름
1. 마이크 음성 입력을 받음
2. 음성 텍스트를 OpenAI에 전달하여 `FAN_ON`/`FAN_OFF` 명령 판단
3. AI 응답 메시지를 출력하고 사용자에게 실행 여부를 확인
4. `y` 입력 시 MQTT 토픽 `agri_log/robot/control/msm03`으로 명령 발행

## 실행 방법
1. 필요한 패키지 설치
   - `openai`
   - `paho-mqtt`
   - `python-dotenv`
   - `SpeechRecognition`
   - 추가로 `PyAudio` 등이 필요할 수 있음

2. `.env` 파일에 OpenAI API 키 추가
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

3. 스크립트 실행
   ```bash
   python human_loop_ai.py
   ```

## 주의 사항
- API 키는 코드에 직접 넣지 말고 `.env`에 저장하세요.
- 공개 MQTT 브로커를 사용하므로 실제 운영 시 인증/암호화가 적용된 브로커로 변경하는 것이 안전합니다.
