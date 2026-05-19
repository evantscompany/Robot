# Arduino UNO Joystick Control

## 프로젝트 개요

아두이노 UNO와 아날로그 조이스틱을 이용하여 로봇 관절을 **실시간으로 제어하고 모니터링**하는 시스템입니다.
조이스틱 입력 → 아두이노 시리얼 송수신 → 데이터베이스 저장 → 웹소켓 스트리밍 → Streamlit 대시보드 시각화의 완전한 제어 파이프라인입니다.

### 프로젝트 동작 화면

![프로젝트 스크린샷](./스크린샷 2026-05-19 172228.png)

---

## 하드웨어 구성

| 부품 | 핀 번호 | 설명 |
|------|---------|------|
| Joystick X | A0 | 아날로그 입력 (0~1023) |
| Servo Motor | 9 | PWM 출력으로 서보 제어 |
| Serial RX/TX | 0/1 | PC와의 시리얼 통신 (9600 baud) |

---

## 시스템 아키텍처

### Arduino 펌웨어 (main.cpp)
- **라이브러리**: `Servo.h`, `ArduinoJson.h`
- **송신** (100ms 주기):
  ```json
  {
    "mcu_timestamp": 12500,
    "joystick_x": 512,
    "device_id": "UNO_ROBOT_02"
  }
  ```
- **수신**: PC에서 JSON 형식의 각도 명령 수신
  ```json
  {
    "angle_x": 90
  }
  ```
- **서보 제어**: 0°~180° 범위로 제한된 안전 제어

### Python Backend

#### `serial_to_db.py` - 시리얼 데이터 수집기
- 아두이노 COM5 포트 (9600 baud)에서 JSON 데이터 수신
- 조이스틱 아날로그값(0~1023) → 서보 각도(0~180°) 매핑
- 수신 데이터를 SQLite DB(`robot_axis_data.db`)에 저장
- **테이블 구조**: `control_logs_axis`
  ```
  id, device_id, joystick_x, mcu_timestamp, angle_x, pc_time
  ```

#### `server.py` - FastAPI 웹소켓 서버
- **포트**: 8000
- **기능**:
  - 백그라운드 스레드에서 시리얼 포트 지속 모니터링
  - 연결된 모든 웹소켓 클라이언트에게 실시간 데이터 브로드캐스트
  - ConnectionManager로 클라이언트 세션 관리
  - CORS 미들웨어 적용
- **엔드포인트**: `ws://localhost:8000/ws`

#### `app.py` - Streamlit 대시보드
- **포트**: 8501 (기본)
- **기능**:
  - 웹소켓으로 FastAPI 서버 연결
  - 실시간 메트릭 3가지 표시:
    - 🤖 MCU 가동 시간 (ms)
    - 🕹️ 조이스틱 원시값
    - ⚙️ 서보모터 타겟 각도
  - 메모리 효율화를 위해 최신 50개 프레임만 버퍼 유지
  - 실시간 모터 각도 변화 라인 차트 시각화

---

## 실행 방법

### 1. 환경 설정
```bash
# Python 가상환경 생성 및 활성화
python -m venv venv
.\venv\Scripts\Activate.ps1

# 패키지 설치
pip install fastapi uvicorn websockets pyserial streamlit pandas
```

### 2. 아두이노 펌웨어 업로드
```bash
# PlatformIO 사용
pio run -t upload
# 또는 Arduino IDE에서 직접 업로드
```

### 3. 백엔드 서버 시작
```bash
python server.py
# FastAPI 서버가 ws://localhost:8000/ws에서 대기
```

### 4. Streamlit 대시보드 실행 (새 터미널)
```bash
streamlit run app.py
# http://localhost:8501에서 대시보드 접근 가능
```

### 5. 실시간 데이터 스트리밍 시작
- Streamlit 사이드바의 "📡 실시간 데이터 스트리밍 시작" 버튼 클릭
- 조이스틱 조작 시 대시보드에 실시간으로 반영됨

---

## 데이터 흐름도

```
[Joystick Input]
       ↓
  [Arduino UNO]
       ↓
  [JSON over Serial]
       ↓
  [serial_to_db.py] → [robot_axis_data.db]
       ↓
  [FastAPI Server]
       ↓
  [WebSocket Broadcast]
       ↓
  [Streamlit Dashboard]
       ↓
    [Visualization]
```

---

## 데이터베이스 스키마

```sql
CREATE TABLE control_logs_axis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT,              -- 아두이노 기기 ID
    joystick_x INTEGER,          -- 조이스틱 아날로그값 (0~1023)
    mcu_timestamp INTEGER,       -- 아두이노 내부 타임스탬프 (ms)
    angle_x INTEGER,             -- 서보 각도 명령 (0~180)
    pc_time REAL                 -- PC 수신 시간 (Unix timestamp)
)
```

---

## 주요 기능

- **JSON 기반 안전한 시리얼 통신** - ArduinoJson 라이브러리로 파싱 안정성 확보
- **실시간 웹소켓 스트리밍** - 100ms 주기로 지속적인 데이터 수신
- **데이터 영속성** - SQLite DB에 모든 제어 기록 저장
- **메모리 효율성** - 순환 버퍼로 대시보드 메모리 누수 방지
- **에러 안전성** - 시리얼 버퍼 오버플로우 감지 및 자동 초기화
- **시각화** - 실시간 라인 차트로 서보 각도 변화 추적

---

## 문제 해결

### 시리얼 포트 연결 실패
- COM 포트 번호 확인 (기본값: COM5)
- 드라이버 재설치 (CP2102 또는 CH340)
- 아두이노와 USB 케이블 재연결

### 웹소켓 연결 오류
- FastAPI 서버가 실행 중인지 확인 (`python server.py`)
- 방화벽 포트 8000 허용 확인
- 브라우저 콘솔 F12에서 에러 메시지 확인

### 데이터가 대시보드에 표시되지 않음
- 조이스틱이 제대로 연결되었는지 확인 (A0 핀)
- serial_to_db.py가 데이터를 수신하는지 콘솔 로그 확인
- robot_axis_data.db 파일이 생성되었는지 확인

---

## 라이센스 및 참고

- **아두이노 라이브러리**: `Servo.h`, `ArduinoJson.h`
- **Python 프레임워크**: FastAPI, Streamlit
- **Database**: SQLite3
