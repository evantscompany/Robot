import streamlit as st
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="로보틱스 프로젝트 포트폴리오",
    page_icon="robot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 제목
col1, col2 = st.columns([0.05, 0.95])
with col1:
    st.write("")
with col2:
    st.title("로보틱스 프로젝트 포트폴리오")
    st.write("농업 로봇 제어 및 IoT 시스템 시각화")

st.divider()

# 사이드바 네비게이션
with st.sidebar:
    st.header("프로젝트 목록")
    st.write("---")
    page = st.radio("보기 선택", ["홈", "H/W 프로젝트", "AI/NL 프로젝트", "가이드"])

# 홈 페이지
if page == "홈":
    st.header("환영합니다")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        ### 프로젝트 개요
        이 포트폴리오는 IoT와 로보틱스를 공부하는 입문자들을 위해 설계되었습니다.
        각 프로젝트의 작동 원리를 시각적으로 이해할 수 있도록 HTML 애니메이션으로 제작했습니다.
        """)
    
    with col2:
        st.success("""
        ### 프로젝트 통계
        - 총 11개 프로젝트
        - H/W: 9개 (센서, 제어, 통신)
        - AI/NL: 2개 (자연어 처리)
        - 신규 시각화: 6개
        - 기존 시각화: 5개
        """)
    
    st.divider()
    
    # 기술 스택
    st.subheader("사용된 기술")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write("**백엔드**")
        st.write("- FastAPI")
        st.write("- SQLite")
        st.write("- Python")
    
    with col2:
        st.write("**하드웨어**")
        st.write("- ESP32")
        st.write("- Arduino")
        st.write("- Wokwi")
    
    with col3:
        st.write("**통신**")
        st.write("- MQTT")
        st.write("- HTTP")
        st.write("- ngrok")
    
    with col4:
        st.write("**AI/머신러닝**")
        st.write("- OpenAI GPT-4o")
        st.write("- Speech Recognition")
        st.write("- 자연어 처리")
    
    st.divider()
    
    # 프로젝트 흐름
    st.subheader("학습 흐름")
    
    learning_path = {
        "기초 (PR1-3)": "센서 입출력, LED 제어, 온습도 측정",
        "중급 (PR4-9)": "양방향 통신, 제어 알고리즘, 신호 처리",
        "고급 (PR10-11)": "AI 연동, 자연어 처리, 인간-AI 협업"
    }
    
    for level, desc in learning_path.items():
        st.write(f"**{level}**")
        st.write(f"- {desc}")
        st.write("")

# H/W 프로젝트 페이지
elif page == "H/W 프로젝트":
    st.header("하드웨어 프로젝트")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["PR1", "PR2", "PR3", "PR4", "기존 프로젝트"])
    
    with tab1:
        st.subheader("PR1: LED 온습도 센서 시스템")
        st.write("IoT 기반 실시간 환경 모니터링 및 제어")
        
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.write("""
            ### 시스템 설명
            - **입력**: DHT22 센서에서 온습도 데이터 수집
            - **처리**: ESP32에서 데이터 처리 및 LED 제어 로직 실행
            - **출력**: FastAPI 서버로 데이터 전송 및 웹 대시보드 표시
            - **저장**: SQLite DB에 시계열 데이터 저장
            
            ### 주요 기능
            ✓ 실시간 온습도 측정  
            ✓ 온도 30°C 이상 시 LED 자동 점등  
            ✓ 데이터 로깅 및 분석  
            ✓ 웹 기반 대시보드
            """)
        with col2:
            st.info("**난이도**: ⭐⭐☆☆☆")
            st.info("**분야**: IoT, 센서")
            st.info("**시간**: 3-4시간")
        
        # HTML 시각화 삽입
        html_file = Path("H_W/pr1_LED_THsensor/sensor_visualization.html")
        if html_file.exists():
            with open(html_file, encoding="utf-8") as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=1200, scrolling=True)
        else:
            st.warning("시각화 파일을 찾을 수 없습니다")
    
    with tab2:
        st.subheader("PR2: 원격 LED 제어 시스템")
        st.write("웹 기반 실시간 원격 제어 및 모니터링")
        
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.write("""
            ### 시스템 설명
            - **웹 인터페이스**: HTML/CSS/JavaScript 대시보드
            - **서버**: FastAPI로 상태 관리
            - **하드웨어**: ESP32가 1초 간격으로 상태 조회
            - **제어**: 웹 → 서버 → ESP32 → LED
            
            ### 주요 기능
            ✓ 웹 기반 LED 제어  
            ✓ 실시간 상태 모니터링 (1초 간격)  
            ✓ 반응형 UI 디자인  
            ✓ 메모리 기반 상태 저장
            """)
        with col2:
            st.info("**난이도**: ⭐⭐⭐☆☆")
            st.info("**분야**: 웹, IoT")
            st.info("**시간**: 4-5시간")
        
        html_file = Path("H_W/pr2_remote_control/remote_control_visualization.html")
        if html_file.exists():
            with open(html_file, encoding="utf-8") as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=1200, scrolling=True)
        else:
            st.warning("시각화 파일을 찾을 수 없습니다")
    
    with tab3:
        st.subheader("PR3: 자동 냉각 팬 제어 시스템")
        st.write("온도 기반 자동 냉각 및 서보모터 제어")
        
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.write("""
            ### 시스템 설명
            - **센서**: 가변저항으로 온도 시뮬레이션
            - **제어**: ESP32에서 팬 속도와 서보모터 각도 계산
            - **안전**: 80°C 이상 시 LED 경고 및 자동 정지
            - **모니터링**: 웹 대시보드에서 실시간 시각화
            
            ### 주요 기능
            ✓ 온도 비례 팬 속도 조절  
            ✓ 서보모터 밸브 제어 (0-180°)  
            ✓ 과열 방지 자동 정지  
            ✓ 데이터 로깅 및 차트 표시
            """)
        with col2:
            st.info("**난이도**: ⭐⭐⭐☆☆")
            st.info("**분야**: 제어, 로보틱스")
            st.info("**시간**: 5-6시간")
        
        html_file = Path("H_W/pr3_auto_cooling/cooling_system_visualization.html")
        if html_file.exists():
            with open(html_file, encoding="utf-8") as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=1200, scrolling=True)
        else:
            st.warning("시각화 파일을 찾을 수 없습니다")
    
    with tab4:
        st.subheader("PR4: 양방향 통신 트랙터 ECU 시뮬레이터")
        st.write("실시간 엔진 제어 및 양방향 데이터 동기화")
        
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.write("""
            ### 시스템 설명
            - **물리 시뮬레이션**: RPM, 온도, 속도를 실시간 계산
            - **양방향 통신**: 웹 ↔ 서버 ↔ ESP32 실시간 동기화
            - **ECU 제어**: FastAPI에서 엔진 시뮬레이션 실행
            - **안전 기능**: 과열 시 자동 정지
            
            ### 주요 기능
            ✓ 실시간 엔진 시뮬레이션  
            ✓ 양방향 데이터 동기화  
            ✓ 웹 제어 및 피드백  
            ✓ 다중 센서 추적 (RPM, 온도, 속도, 연료)
            """)
        with col2:
            st.info("**난이도**: ⭐⭐⭐⭐☆")
            st.info("**분야**: 통신, 시뮬레이션")
            st.info("**시간**: 6-7시간")
        
        html_file = Path("H_W/pr4_Two-way_communication/ecu_simulator_visualization.html")
        if html_file.exists():
            with open(html_file, encoding="utf-8") as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=1200, scrolling=True)
        else:
            st.warning("시각화 파일을 찾을 수 없습니다")
    
    with tab5:
        st.subheader("기존 시각화 프로젝트")
        
        existing_projects = [
            ("PR5", "CAN 버스", "pr5_CANbus", "CANBus_visualization.html"),
            ("PR6", "Inverse Kinematics", "pr6_Inverse_Kinematics_IK", "IK_visualization.html"),
            ("PR7", "FSM", "pr7_fsm_Finite_state_machine", "fsm_visulization.html"),
            ("PR8", "Kalman Filter", "pr8_Kalman_Filter", "kalman_filter_visualization.html"),
            ("PR9", "PID Controller", "pr9_PID_controller", "PID_simulator.html"),
        ]
        
        for num, name, folder, html_file in existing_projects:
            if st.checkbox(name, value=False):
                st.write(f"### {name}")
                html_path = Path(f"H_W/{folder}/{html_file}")
                if html_path.exists():
                    with open(html_path, encoding="utf-8") as f:
                        html_content = f.read()
                    st.components.v1.html(html_content, height=1000, scrolling=True)
                else:
                    st.warning(f"시각화 파일을 찾을 수 없습니다: {html_path}")

# AI/NL 프로젝트 페이지
elif page == "AI/NL 프로젝트":
    st.header("AI 및 자연어 처리 프로젝트")
    
    tab1, tab2 = st.tabs(["PR10", "PR11"])
    
    with tab1:
        st.subheader("PR10: 자연어 기반 로봇 제어 (NL2Action)")
        st.write("OpenAI와 MQTT를 활용한 자연언어 로봇 명령 시스템")
        
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.write("""
            ### 시스템 설명
            - **입력**: 사용자가 자연어로 명령 입력
            - **AI 분석**: OpenAI GPT-4o가 명령 의도 분석
            - **명령 생성**: JSON 형식의 구조화된 명령 생성
            - **실행**: MQTT로 명령을 IoT 기기에 즉시 전송
            
            ### 주요 기능
            ✓ 자연어 이해 (한국어 포함)  
            ✓ MQTT 토픽 기반 발행  
            ✓ 실시간 로봇 제어  
            ✓ 완전 자동화 (사람 개입 없음)
            """)
        with col2:
            st.info("**난이도**: ⭐⭐⭐⭐☆")
            st.info("**분야**: AI, NLP")
            st.info("**시간**: 4-5시간")
        
        html_file = Path("H_W/pr10_NL2Action_Natural_language_to_Robot_action/nl2action_visualization.html")
        if html_file.exists():
            with open(html_file, encoding="utf-8") as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=1200, scrolling=True)
        else:
            st.warning("시각화 파일을 찾을 수 없습니다")
    
    with tab2:
        st.subheader("PR11: 인간-AI 루프 제어 시스템")
        st.write("음성 명령, AI 분석, 사람 승인을 거쳐 로봇을 제어합니다")
        
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.write("""
            ### 시스템 설명
            - **입력**: 음성 명령 수집 (SpeechRecognition)
            - **AI 분석**: OpenAI가 음성 텍스트 의도 분석
            - **사람 승인**: 사용자가 최종 검증 및 승인
            - **실행**: 승인된 명령만 MQTT로 전송
            
            ### 주요 특징
            ✓ 음성 인식 기능  
            ✓ AI 신뢰도 표시  
            ✓ 사람의 최종 판단 (안전성)  
            ✓ 승인 전까지 명령 미실행 (보안)
            """)
        with col2:
            st.info("**난이도**: ⭐⭐⭐⭐⭐")
            st.info("**분야**: AI, UX, 안전")
            st.info("**시간**: 5-6시간")
        
        html_file = Path("H_W/pr11_Human_in_the_Loop/human_in_loop_visualization.html")
        if html_file.exists():
            with open(html_file, encoding="utf-8") as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=1200, scrolling=True)
        else:
            st.warning("시각화 파일을 찾을 수 없습니다")

# 가이드 페이지
elif page == "가이드":
    st.header("학습 가이드")
    
    tab1, tab2, tab3 = st.tabs(["시작하기", "개념 설명", "연결 정보"])
    
    with tab1:
        st.subheader("로드맵")
        
        st.markdown("""
        ### 1단계: 기초 IoT (1-2주)
        **PR1, PR2, PR3 학습**
        - LED 제어 및 센서 읽기
        - 웹 기반 제어 인터페이스
        - 온도 기반 자동 제어
        
        **배울 점:**
        - GPIO 제어 (HIGH/LOW)
        - HTTP 통신
        - 실시간 데이터 처리
        
        ### 2단계: 고급 통신 (2-3주)
        **PR4, PR5, PR6 학습**
        - 양방향 통신 및 동기화
        - CAN 버스 프로토콜
        - 역기구학 (Inverse Kinematics)
        
        **배울 점:**
        - 실시간 물리 시뮬레이션
        - 복잡한 제어 알고리즘
        - 멀티 센서 통합
        
        ### 3단계: AI 연동 (1-2주)
        **PR10, PR11 학습**
        - 자연어 처리 (NLP)
        - 음성 인식
        - 인간-AI 협업
        
        **배울 점:**
        - OpenAI API 연동
        - 머신러닝 기초
        - 안전한 AI 시스템 설계
        """)
    
    with tab2:
        st.subheader("핵심 개념")
        
        concepts = {
            "GPIO (General Purpose Input/Output)": 
                "디지털 신호를 송수신하는 ESP32의 핀. LED 켜기/끄기, 버튼 입력 등에 사용",
            
            "HTTP vs MQTT": 
                "HTTP: 요청-응답 기반 (웹). MQTT: 발행-구독 기반 (IoT)",
            
            "PWM (Pulse Width Modulation)": 
                "디지털 신호로 아날로그 신호 제어. LED 밝기, 팬 속도 조절에 사용",
            
            "양방향 통신": 
                "클라이언트와 서버가 동시에 데이터 송수신. 실시간 제어에 필수",
            
            "자연어 처리 (NLP)": 
                "사람 말을 기계가 이해하는 AI 기술. 음성/텍스트 명령 인식",
            
            "인간-AI 루프": 
                "AI가 제안하고 사람이 최종 승인. 안전성과 자율성의 균형"
        }
        
        for concept, explanation in concepts.items():
            with st.expander(concept):
                st.write(explanation)
    
    with tab3:
        st.subheader("시스템 연결도")
        
        st.markdown("""
        ```
        웹 브라우저
            ↕
        FastAPI 서버
            ↕
        Wokwi 시뮬레이터
            ↕
        ESP32 하드웨어
            ↕
        센서/액추에이터 (LED, 팬, 서보모터)
        
        
        추가 연동:
        
        입력 장치          처리               출력 장치
        ─────────         ──────────         ──────────
        마이크       →    OpenAI API    →    MQTT 브로커
        키보드       →    Python        →    ESP32
        센서         →    FastAPI       →    로봇/제어기
        ```
        """)
        
        st.info("""
        ### 주요 포트 및 URL
        
        - **FastAPI 서버**: http://localhost:8000
        - **Streamlit**: http://localhost:8501
        - **MQTT 브로커**: broker.hivemq.com:1883
        - **ngrok 터널**: (동적 URL)
        
        ### 필수 패키지
        
        ```bash
        pip install fastapi uvicorn paho-mqtt openai SpeechRecognition
        ```
        """)

# 푸터
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.write("### 연락처")
    st.write("GitHub: @robotics-portfolio")
    st.write("Email: contact@example.com")

with col2:
    st.write("### 참고 자료")
    st.write("- ESP32 공식 문서")
    st.write("- FastAPI 튜토리얼")
    st.write("- MQTT 프로토콜")

with col3:
    st.write("### 학습 출처")
    st.write("- Arduino 공식 튜토리얼")
    st.write("- Wokwi 시뮬레이터")
    st.write("- OpenAI 개발 문서")

st.write("---")
st.write("<p style='text-align: center; color: gray;'>로보틱스 프로젝트 포트폴리오 | 2024</p>", unsafe_allow_html=True)
