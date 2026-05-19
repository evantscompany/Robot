import streamlit as st
import json
import asyncio
import websockets
import pandas as pd
from collections import deque

st.set_page_config(page_title="Agri-Log 로봇 관절 모니터링", layout="wide")

st.title(" Agri-Log 실시간 데이터 수집 대시보드")
st.markdown("아두이노에서 올라오는 로봇 센서 데이터와 제어 명령 상태를 웹 화면에서 실시간 트래킹합니다.")

# 실시간 시각화 데이터 버퍼 설정 (메모리 누수 방지를 위해 최신 50개 프레임만 유지)
if "data_history" not in st.session_state:
    st.session_state.data_history = deque(maxlen=50)

# 화면 상단 수치 UI 레이아웃 구성
col1, col2, col3 = st.columns(3)
ui_mcu_time = col1.empty()
ui_joy_x = col2.empty()
ui_angle_x = col3.empty()

# 하단 그래프 영역 레이아웃 구획
chart_container = st.empty()

async def connect_to_websocket():
    uri = "ws://localhost:8000/ws"
    
    # 서버가 켜질 때까지 재시도하는 예외 안전망 구축
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                st.success("서버 웹소켓 파이프라인에 성공적으로 연결되었습니다.")
                
                while True:
                    # 웹소켓 패킷 수신
                    message = await websocket.recv()
                    data = json.loads(message)
                    
                    # 큐 버퍼에 누적 데이터 추가
                    st.session_state.data_history.append(data)
                    
                    # 상단 위젯 메트릭 실시간 업데이트
                    ui_mcu_time.metric("🤖 MCU 가동 시간 (ms)", f"{data['mcu_timestamp']}")
                    ui_joy_x.metric("🕹️ 조이스틱 원시값", f"{data['joystick_x']}")
                    ui_angle_x.metric("⚙️ 서보모터 타겟 각도", f"{data['angle_x']}°")
                    
                    # 수집된 데이터를 판다스 데이터프레임으로 변환하여 실시간 차트 렌더링
                    df = pd.DataFrame(list(st.session_state.data_history))
                    if not df.empty:
                        with chart_container.container():
                            st.subheader("실시간 모터 각도 변화 트렌드")
                            # 주축인 각도 데이터 시각화
                            st.line_chart(df[['angle_x']])
                            
        except (websockets.exceptions.ConnectionClosed, ConnectionRefusedError):
            st.warning("백엔드 서버와 연결이 원활하지 않습니다. 3초 후 재연결을 시도합니다...")
            await asyncio.sleep(3)
        except Exception as e:
            st.error(f"오류 발생: {e}")
            await asyncio.sleep(3)

# 대시보드 구동 버튼 트리거
if st.sidebar.button("📡 실시간 데이터 스트리밍 시작", use_container_width=True):
    asyncio.run(connect_to_websocket())
else:
    st.sidebar.info("왼쪽 버튼을 누르면 실시간 웹소켓 통신 파이프라인이 가동됩니다.")