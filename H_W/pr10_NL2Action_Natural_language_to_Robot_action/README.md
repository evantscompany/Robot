# NL2Action: 자연어 기반 로봇 제어

이 프로젝트는 사용자의 자연어 명령을 OpenAI API로 해석하여 MQTT를 통해 Wokwi/ESP32 기반 농업 로봇에 제어 신호를 전송합니다.

## 구성
- `NL2Action.py`: 사용자 입력을 받아 OpenAI에 질의하고, 반환된 JSON 명령을 MQTT로 발행합니다.
- `.env` 파일: `OPENAI_API_KEY`를 안전하게 저장합니다. 이 파일은 소스 저장소에 커밋하지 마세요.

## 주요 동작
1. `OPENAI_API_KEY`를 환경 변수로 로드
2. `broker.hivemq.com` MQTT 브로커에 연결
3. 사용자 입력을 받아 OpenAI에 전송
4. 응답에서 `{"action": "FAN_ON"}` 또는 `{"action": "FAN_OFF"}` 형태의 JSON을 추출
5. MQTT 토픽 `agri_log/robot/control/msm03`으로 명령 발행

## 실행 방법
1. 필요한 패키지 설치
   - `openai`
   - `paho-mqtt`
   - `python-dotenv`

2. `.env` 파일에 OpenAI API 키 추가
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

3. 스크립트 실행
   ```bash
   python NL2Action.py
   ```

4. 명령어 입력
   - 예: `팬을 켜줘`, `팬 꺼줘`
   - 종료하려면 `q` 입력

## 보안 주의
- API 키는 절대 코드에 하드코딩하지 마세요.
- `.env` 파일과 민감 정보는 Git 저장소에 포함시키지 않습니다.
- 공개 MQTT 브로커를 사용하므로, 실제 운영 환경에서는 인증과 암호화가 적용된 브로커 사용을 권장합니다.

## 참고
- 이 프로젝트는 농업용 로봇의 팬 제어 명령 분석 예시입니다.
- OpenAI 모델은 `gpt-4o`를 사용하며, 응답 포맷을 JSON 객체로 제한하도록 설정되어 있습니다.
