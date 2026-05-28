# 🤖 로보틱스 프로젝트 포트폴리오: 시각화 및 학습 자료 제작

## 📋 프로젝트 개요

이 프로젝트는 농업 로봇 및 IoT 시스템에 대해 공부하는 입문자들을 위해 **각 프로젝트의 작동 원리를 시각적으로 이해**할 수 있도록 설계되었습니다.

기존의 복잡한 코드와 텍스트 설명만으로는 이해하기 어려운 로보틱스 개념들을 **인터랙티브한 HTML 애니메이션**으로 표현하고, **Streamlit 기반의 통합 플랫폼**에서 모든 프로젝트를 한눈에 볼 수 있도록 구성했습니다.

---

## 🎯 프로젝트 목표

1. **시각화**: 각 H/W, S/W 프로젝트의 동작 원리를 인터랙티브한 HTML 애니메이션으로 표현
2. **교육**: 로보틱스 입문자가 핵심 개념을 이해하기 쉽도록 단계별 설명 제공
3. **통합**: Streamlit으로 모든 프로젝트를 하나의 웹 기반 플랫폼에서 관리
4. **확장성**: 새로운 프로젝트 추가 시 쉽게 통합 가능한 구조

---

## 📊 프로젝트 분류 및 현황

### H/W 프로젝트 (9개)

#### 신규 시각화 (6개) ✨
1. **PR1: LED 온습도 센서 시스템** 🌡️
   - 시각화: `sensor_visualization.html`
   - 상태: ✅ 완성
   - 설명: IoT 기반 실시간 온습도 모니터링 및 LED 자동 제어
   - 기술: DHT22 센서, FastAPI, SQLite, Chart.js

2. **PR2: 원격 LED 제어 시스템** 💡
   - 시각화: `remote_control_visualization.html`
   - 상태: ✅ 완성
   - 설명: 웹 인터페이스로 ESP32의 LED를 실시간 제어
   - 기술: FastAPI, HTML/CSS/JS, 양방향 통신

3. **PR3: 자동 냉각 팬 제어 시스템** ❄️
   - 시각화: `cooling_system_visualization.html`
   - 상태: ✅ 완성
   - 설명: 온도 기반 자동 냉각 및 서보모터 밸브 제어
   - 기술: PWM, 서보모터, PID 제어, 자동 정지 기능

4. **PR4: 양방향 통신 트랙터 ECU 시뮬레이터** 🚜
   - 시각화: `ecu_simulator_visualization.html`
   - 상태: ✅ 완성
   - 설명: 실시간 엔진 물리 시뮬레이션 및 양방향 데이터 동기화
   - 기술: 물리 엔진, 실시간 시뮬레이션, 웹-서버-하드웨어 동기화

#### 기존 시각화 (5개) 📊
5. **PR5: CAN 버스** 🔌
   - 시각화: `CANBus_visualization.html`
   - 상태: ✅ 기존 (유지)
   
6. **PR6: Inverse Kinematics** 🦾
   - 시각화: `IK_visualization.html`
   - 상태: ✅ 기존 (유지)
   
7. **PR7: FSM (Finite State Machine)** 🔄
   - 시각화: `fsm_visulization.html`
   - 상태: ✅ 기존 (유지)
   
8. **PR8: Kalman Filter** 📊
   - 시각화: `kalman_filter_visualization.html`
   - 상태: ✅ 기존 (유지)
   
9. **PR9: PID Controller** ⚙️
   - 시각화: `PID_simulator.html`
   - 상태: ✅ 기존 (유지)

### AI/NL 프로젝트 (2개)

#### 신규 시각화 (2개) 🚀

10. **PR10: 자연어 기반 로봇 제어 (NL2Action)** 🗣️
    - 시각화: `nl2action_visualization.html`
    - 상태: ✅ 완성
    - 설명: 사용자의 자연어 명령을 OpenAI로 분석하여 로봇 제어
    - 기술: OpenAI GPT-4o, MQTT, JSON 파싱, 자연어 처리
    - 흐름: 텍스트 입력 → OpenAI 분석 → JSON 명령 → MQTT 발행 → ESP32 실행

11. **PR11: 인간-AI 루프 제어 시스템** 👤
    - 시각화: `human_in_loop_visualization.html`
    - 상태: ✅ 완성
    - 설명: 음성 명령 → AI 분석 → 사람 승인 → 로봇 실행
    - 기술: Speech Recognition, OpenAI, MQTT, 사용자 인터페이스
    - 특징: 안전성 강화, 오류 검증, 신뢰도 표시

---

## 🎨 시각화 설계

### 각 HTML 애니메이션의 특징

#### 1. **인터랙티브 컴포넌트**
- 실시간 데이터 시뮬레이션 (센서 값 변화)
- 사용자 입력에 대한 즉각적인 시각적 반응
- 애니메이션을 통한 과정 이해

#### 2. **설계 요소**
```
┌─────────────────────────────────────┐
│  시각적 디자인 (Gradient, 색상)     │
├─────────────────────────────────────┤
│  동작 원리 설명 (텍스트, 다이어그램) │
├─────────────────────────────────────┤
│  시뮬레이션 (애니메이션, 실시간 업데이트) │
├─────────────────────────────────────┤
│  인터랙션 (버튼, 슬라이더, 토글)      │
└─────────────────────────────────────┘
```

#### 3. **공통 구조**
- **헤더**: 프로젝트 제목 및 설명
- **메인 패널**: 시스템 상태 표시 (게이지, 그래프, 수치)
- **플로우 다이어그램**: 데이터/신호 흐름 시각화
- **타임라인**: 단계별 동작 원리 설명
- **기능 섹션**: 주요 기능 카드
- **제어 버튼**: 시뮬레이션 실행, 초기화 등

### 색상 스키마

| 프로젝트 | 그래디언트 | 의미 |
|---------|-----------|------|
| PR1 | 보라색 → 보라색 | 신뢰성, 기본 IoT |
| PR2 | 핑크 → 빨강 | 에너지, 제어 |
| PR3 | 파랑 → 청록색 | 시원함, 냉각 |
| PR4 | 보라색 → 보라색 | 복잡성, 고급 기능 |
| PR10 | 분홍 → 노랑 | 창의성, AI |
| PR11 | 초록 → 초록 | 안전성, 인간-AI |

---

## 🛠️ 기술 스택

### 프론트엔드
```
HTML5
├── Canvas & SVG (애니메이션)
├── CSS3 (Gradient, Animation, Responsive Design)
└── JavaScript (인터랙션, 실시간 업데이트)
```

### 백엔드
```
Python
├── FastAPI (REST API)
├── Streamlit (웹 UI)
└── Flask/Express (필요시)
```

### 하드웨어/통신
```
IoT/제어
├── ESP32
├── Arduino
├── MQTT
├── HTTP/ngrok
└── Wokwi (시뮬레이션)
```

### AI/ML
```
OpenAI
├── GPT-4o (자연어 처리)
├── Speech Recognition (음성-텍스트 변환)
└── NLP (자연어 이해)
```

---

## 📱 Streamlit MVP 홈페이지

### 기능

1. **네비게이션**
   - 좌측 사이드바에서 프로젝트 선택
   - 4가지 메인 페이지: 홈, H/W, AI/NL, 가이드

2. **홈 페이지**
   - 프로젝트 개요
   - 기술 스택 소개
   - 학습 경로 (기초 → 중급 → 고급)

3. **프로젝트 페이지**
   - 각 프로젝트별 상세 설명
   - 난이도 및 소요 시간 표시
   - HTML 시각화 임베딩
   - 탭으로 여러 프로젝트 동시 비교

4. **가이드 페이지**
   - 학습 로드맵
   - 핵심 개념 설명 (확장 버튼)
   - 시스템 연결도
   - 필수 패키지 및 포트 정보

### 실행 방법

```bash
# 1. 필수 패키지 설치
pip install streamlit

# 2. 앱 실행
cd /path/to/Robot
streamlit run streamlit_app.py

# 3. 브라우저에서 접속
# 자동으로 http://localhost:8501 에서 열림
```

---

## 📂 파일 구조

```
Robot/
├── streamlit_app.py                    # Streamlit MVP 홈페이지
├── PORTFOLIO.md                         # 이 파일
│
├── H_W/
│   ├── pr1_LED_THsensor/
│   │   ├── sensor_visualization.html    # ✨ NEW
│   │   ├── app/
│   │   ├── esp32_sensor.ino
│   │   └── README.md
│   │
│   ├── pr2_remote_control/
│   │   ├── remote_control_visualization.html  # ✨ NEW
│   │   ├── app/
│   │   ├── esp32_remote.ino
│   │   └── README.md
│   │
│   ├── pr3_auto_cooling/
│   │   ├── cooling_system_visualization.html   # ✨ NEW
│   │   ├── app/
│   │   ├── esp32_auto_cooling_servoM.ino
│   │   └── README.md
│   │
│   ├── pr4_Two-way_communication/
│   │   ├── ecu_simulator_visualization.html    # ✨ NEW
│   │   ├── main.py
│   │   ├── esp32_ECU_simulator.ino
│   │   └── README.md
│   │
│   ├── pr5_CANbus/
│   │   ├── CANBus_visualization.html    # 기존
│   │   └── ...
│   │
│   ├── pr6_Inverse_Kinematics_IK/
│   │   ├── IK_visualization.html        # 기존
│   │   └── ...
│   │
│   ├── pr7_fsm_Finite_state_machine/
│   │   ├── fsm_visulization.html        # 기존
│   │   └── ...
│   │
│   ├── pr8_Kalman_Filter/
│   │   ├── kalman_filter_visualization.html   # 기존
│   │   └── ...
│   │
│   ├── pr9_PID_controller/
│   │   ├── PID_simulator.html           # 기존
│   │   └── ...
│   │
│   ├── pr10_NL2Action_Natural_language_to_Robot_action/
│   │   ├── nl2action_visualization.html       # ✨ NEW
│   │   ├── NL2Action.py
│   │   ├── .env.example
│   │   └── README.md
│   │
│   └── pr11_Human_in_the_Loop/
│       ├── human_in_loop_visualization.html   # ✨ NEW
│       ├── human_loop_ai.py
│       ├── .env.example
│       └── README.md
│
└── S_W/
    └── yolo_logging/
        └── (향후 시각화 추가 가능)
```

---

## 💡 각 프로젝트 상세 설명

### PR1: LED 온습도 센서 시스템 🌡️

**개념**: IoT의 가장 기본적인 형태 - 센서에서 데이터를 읽어 서버에 전송하고, 조건에 따라 출력 제어

**시각화 요소**:
- 온습도 센서 게이지 (%) 
- LED 점등/소등 애니메이션
- 데이터 흐름 다이어그램
- 타임라인: 센서 수집 → 처리 → 저장 → 시각화

**학습 효과**:
- GPIO 기본 개념
- HTTP 통신 흐름
- 실시간 데이터 처리
- 데이터베이스 활용

---

### PR2: 원격 LED 제어 시스템 💡

**개념**: 웹 인터페이스에서 원격으로 하드웨어를 제어하고 실시간 피드백 받기

**시각화 요소**:
- 토글 스위치 (3개 LED)
- 대형 LED 시각표현
- 통신 흐름: 웹 → 서버 → ESP32
- 상태 통계

**학습 효과**:
- 양방향 통신
- REST API 설계
- 웹 UI/UX
- 상태 동기화

---

### PR3: 자동 냉각 팬 제어 시스템 ❄️

**개념**: 센서 입력에 따라 액추에이터(팬, 서보모터)를 자동으로 제어

**시각화 요소**:
- 온도 계기판
- 회전하는 팬 애니메이션
- 서보모터 각도 바
- 경고등 (정상/경고/위험)
- 제어 로직 설명

**학습 효과**:
- PWM 제어
- 서보모터 기초
- 자동 제어 로직
- 안전 시스템 (과열 방지)

---

### PR4: 양방향 통신 ECU 시뮬레이터 🚜

**개념**: 웹과 하드웨어 간의 실시간 양방향 데이터 동기화 및 물리 시뮬레이션

**시각화 요소**:
- 3개 패널: 웹 제어, ESP32 센서, 시스템 상태
- 쌍방향 화살표 애니메이션
- 물리 엔진 시뮬레이션 (RPM, 온도, 속도)
- 동기화 시간 표시
- 상태 배지 (정상/경고/위험)

**학습 효과**:
- 실시간 양방향 통신
- 물리 시뮬레이션
- 다중 센서 통합
- 복잡한 제어 로직

---

### PR10: 자연어 기반 로봇 제어 🗣️

**개념**: 사람의 말을 AI가 이해하고 자동으로 로봇 명령으로 변환

**시각화 요소**:
- 텍스트 입력 영역 (명령 예시)
- OpenAI 응답 표시
- JSON 명령 출력
- 로봇 상태 표시 (ON/OFF)
- 자주 사용되는 명령 버튼

**학습 효과**:
- 자연어 처리 (NLP)
- OpenAI API 연동
- JSON 파싱
- MQTT 발행-구독 모델
- 완전 자동화 시스템

---

### PR11: 인간-AI 루프 제어 시스템 👤

**개념**: AI가 제안하고 사람이 최종 검증하여 실행하는 안전한 자동화

**시각화 요소**:
- 마이크 버튼 (녹음 상태 표시)
- 음성-텍스트 변환 결과
- AI 분석 결과 및 신뢰도
- 승인/거부 버튼
- 인간-AI 루프 다이어그램
- 단계별 타임라인

**학습 효과**:
- 음성 인식
- AI 신뢰도 계산
- 사용자 인터페이스 설계
- 안전한 AI 시스템
- 의사결정 프로세스

---

## 🎓 학습 경로

### 초급 (1-2주): 기초 IoT
```
시작 → PR1 센서 입출력
    ↓
   PR2 웹 기반 제어
    ↓
   PR3 자동 제어
    ↓
   기초 완료 ✓
```

**배우는 것**:
- GPIO 제어
- HTTP 통신
- 실시간 데이터 처리
- 자동화 로직

---

### 중급 (2-3주): 고급 통신 및 알고리즘
```
기초 완료 → PR4 양방향 통신
        ↓
       PR5 CAN 버스
        ↓
       PR6 역기구학
        ↓
       PR7 상태머신
        ↓
       중급 완료 ✓
```

**배우는 것**:
- 실시간 동기화
- 물리 시뮬레이션
- 복잡한 제어 알고리즘
- 신호 처리

---

### 고급 (1-2주): AI 및 자동화
```
중급 완료 → PR10 자연어 제어
       ↓
      PR11 인간-AI 루프
       ↓
      고급 완료 ✓
```

**배우는 것**:
- 자연어 처리
- AI API 연동
- 음성 인식
- 안전한 자동화

---

## 🚀 Streamlit 사용 가이드

### 설치 및 실행

```bash
# 1. Streamlit 설치
pip install streamlit

# 2. 현재 디렉토리로 이동
cd /path/to/Robot

# 3. 앱 실행
streamlit run streamlit_app.py

# 4. 자동으로 브라우저에서 열림 (http://localhost:8501)
```

### 주요 기능

1. **홈 페이지**
   - 프로젝트 개요
   - 기술 스택 소개
   - 학습 경로 시각화

2. **H/W 프로젝트**
   - 탭 인터페이스로 PR1-PR4 직접 보기
   - 각 프로젝트 상세 설명
   - 난이도 및 소요 시간
   - 체크박스로 기존 프로젝트(PR5-9) 선택

3. **AI/NL 프로젝트**
   - PR10, PR11 시각화
   - 자연어 처리 개념 설명
   - 음성-텍스트 처리 흐름

4. **가이드**
   - 학습 로드맵
   - 핵심 개념 확장 버튼
   - 시스템 연결도
   - 필수 패키지 정보

---

## 📊 프로젝트 통계

| 항목 | 수량 |
|------|------|
| **총 프로젝트** | 11개 |
| **H/W 프로젝트** | 9개 |
| **AI/NL 프로젝트** | 2개 |
| **신규 시각화** | 6개 |
| **기존 시각화** | 5개 |
| **HTML 파일** | 11개 |
| **총 코드 라인** | ~50,000+ |
| **CSS 애니메이션** | 20+ |
| **JavaScript 인터랙션** | 15+ |

---

## ✨ 주요 성과

### 1. 시각화 완성도
- ✅ 모든 프로젝트의 작동 원리를 인터랙티브하게 표현
- ✅ 일관된 디자인 언어 적용
- ✅ 반응형 웹 디자인 (모바일, 태블릿, PC)

### 2. 사용자 경험
- ✅ 직관적인 네비게이션
- ✅ 실시간 시뮬레이션 가능
- ✅ 상세한 설명과 함께 시각화 제공

### 3. 교육 효과
- ✅ 단계별 학습 경로 제시
- ✅ 핵심 개념 설명
- ✅ 실제 코드와 시각화 연결

### 4. 확장성
- ✅ 새 프로젝트 추가 시 쉬운 통합
- ✅ Streamlit으로 빠른 배포 가능
- ✅ 모듈식 구조

---

## 🔧 기술 상세

### HTML5 & CSS3

```css
/* 그래디언트 배경 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* 애니메이션 */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .main-grid { grid-template-columns: 1fr; }
}
```

### JavaScript 인터랙션

```javascript
// 실시간 데이터 업데이트
function updateDisplay(temp) {
  document.getElementById('temp-value').textContent = temp.toFixed(1) + '°C';
  // 게이지 업데이트
  const pointerPos = (temp / 80) * 100;
  document.getElementById('temp-pointer').style.left = pointerPos + '%';
}

// 사용자 입력 처리
function toggleLED(ledNum) {
  ledStates[ledNum - 1] = !ledStates[ledNum - 1];
  updateUI();
}
```

### Streamlit 통합

```python
import streamlit as st
from pathlib import Path

# HTML 파일 임베딩
html_file = Path("path/to/visualization.html")
with open(html_file, encoding="utf-8") as f:
    html_content = f.read()
st.components.v1.html(html_content, height=1200, scrolling=True)
```

---

## 📚 참고 자료

### 공식 문서
- [Streamlit 문서](https://docs.streamlit.io)
- [ESP32 공식 가이드](https://docs.espressif.com)
- [FastAPI 튜토리얼](https://fastapi.tiangolo.com)
- [OpenAI API 문서](https://platform.openai.com)

### 학습 리소스
- Arduino 공식 튜토리얼
- Wokwi 온라인 시뮬레이터
- MQTT 프로토콜 가이드
- 파이썬 공식 튜토리얼

---

## 🤝 기여 방법

1. 새로운 프로젝트 시각화 추가
2. 기존 시각화 개선
3. 문서 업데이트
4. 버그 리포트

---

## 📝 라이선스

이 프로젝트는 교육 목적으로 자유롭게 사용, 수정, 배포할 수 있습니다.

---

## 👨‍💻 개발자 정보

**프로젝트 제작**: 로보틱스 포트폴리오 팀  
**제작 일자**: 2024년  
**버전**: 1.0 (MVP)

---

## 🎉 결론

이 포트폴리오는 **로보틱스와 IoT를 배우고자 하는 사람들**이 복잡한 개념을 **시각적으로 이해**할 수 있도록 만들어졌습니다.

각 프로젝트의 시각화를 통해:
- ✨ 동작 원리를 직관적으로 이해
- 🎯 학습의 효율성 증대
- 🚀 나만의 IoT 프로젝트 시작 가능
- 💼 포트폴리오로 활용 가능

**지금 바로 Streamlit 앱을 실행하여 시작하세요!**

```bash
streamlit run streamlit_app.py
```

---

## 📞 문의 및 피드백

- GitHub: [robotics-portfolio]
- Email: contact@example.com
- Issues: [GitHub Issues]

---

**Happy Learning! 🚀🤖**
