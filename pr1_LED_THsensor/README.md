# PR1: LED 온습도 센서 시스템

IoT 기반 온습도 센서 데이터 수집 및 LED 제어 시스템

## 📋 개요
ESP32에서 온습도 센서 데이터를 수집하여 FastAPI 서버로 전송하고, 서버에서 실시간 모니터링 대시보드를 제공하는 기초 IoT 시스템입니다.

## 🏗️ 시스템 구조
```
ESP32 (DHT22 센서) → FastAPI 서버 → 웹 대시보드
                     ↓
               SQLite DB 저장
```

## 🔧 기능
- **실시간 데이터 수집**: DHT22 센서로 온도/습도 측정
- **데이터 전송**: ESP32 → 서버 (POST /update-sensor)
- **데이터베이스 저장**: SQLite에 시계열 데이터 저장
- **실시간 모니터링**: Chart.js 기반 대시보드
- **LED 자동 제어**: 온도 30°C 이상시 LED 켜짐

## 📁 파일 구조
```
pr1_LED_THsensor/
├── app/
│   ├── main.py              # FastAPI 서버 메인 파일
│   └── services/
│       └── hardware.py     # 하드웨어 제어 서비스
├── esp32_sensor.ino         # ESP32 펌웨어
├── sensor_data.db          # SQLite 데이터베이스
└── diagram.json            # 시스템 다이어그램
```

## 🚀 실행 방법

### 서버 실행
```bash
cd pr1_LED_THsensor/app
pip install fastapi uvicorn
python main.py
```

### ESP32 설정
1. Wokwi 시뮬레이터에서 `esp32_sensor.ino` 업로드
2. ngrok URL을 실제 서버 주소로 변경
3. DHT22 센서를 GPIO 15, LED를 GPIO 18에 연결

## 🌐 API 엔드포인트

| 메소드 | 경로 | 설명 |
|--------|------|------|
| POST | `/led/{status}` | LED 제어 (True/False) |
| GET | `/sensor` | 센서 값 조회 |
| POST | `/update-sensor` | 센서 데이터 수신 |
| GET | `/history` | 최근 10개 기록 조회 |
| GET | `/` | 실시간 대시보드 |

## 📊 데이터베이스 스키마
```sql
CREATE TABLE sensor_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME,
    temperature REAL,
    humidity REAL
);
```

## 🔗 통신 프로토콜
- **프로토콜**: HTTP/HTTPS
- **데이터 형식**: JSON
- **전송 주기**: 3초
- **인증**: ngrok-skip-browser-warning 헤더

## ⚙️ 설정
- **와이파이**: Wokwi-GUEST (시뮬레이션)
- **서버 주소**: ngrok 엔드포인트
- **센서 핀**: GPIO 15 (DHT22)
- **LED 핀**: GPIO 18

## 🐛 트러블슈팅
1. **데이터 전송 실패**: ngrok URL 확인 및 인터넷 연결 상태 점검
2. **센서 읽기 오류**: DHT22 센서 연결 상태 확인
3. **대시보드 로딩 실패**: Chart.js CDN 연결 상태 확인

## 📈 특징
- 실시간 데이터 시각화 (2초 갱신)
- 히스토리 데이터 관리
- 자동 LED 제어 로직
- 반응형 웹 인터페이스
