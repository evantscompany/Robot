# 순서 흐름도 : 
# 객체 생성 -> DB 생성(필요시) -> 상태 변수 설정 -> 기계와 통신할 함수 및 api 설정

from fastapi import FastAPI
import uvicorn
from fastapi.responses import HTMLResponse

app = FastAPI()

# 시스템 상태 관리 변수

system_state = {
    "engine_temp":0,        #실시간 엔진 온도
    "fan_speed" : 0,        #쿨링팬 속도(0~255)
    "emergency_stop":False,  #비상정지상태
    "control_mode":"AUTO"   #AUTO 또는 MANUAL 
}

# 기계용 API - 트랙터가 서버에 데이터를 보고하고 명령을 받아감.
@app.post("/tractor/sync")
async def sync_tractor(data:dict):
    global system_state

    # 1. 트랙터로부터 온도 수신
    system_state["engine_temp"] = data.get("temp",0) #temp 값없을때 0으로 기본사용. 예외처리

    # 2. 자동 모드일 경우 서버가 로직 판단
    if system_state['control_mode']=="AUTO":
        if system_state['engine_temp']>=80:
            system_state['fan_speed'] = 255 #팬 풀가동 조지기
        elif system_state["engine_temp"]>=50:
            system_state["fan_speed"] = 128 #대략 뭐 절반? 가동
        else:
            system_state["fan_speed"] = 0   #정지. 또는 최소 회전
    
    # 3. 트랙터에 내릴 명령
    return{
        "fan_speed" : system_state["fan_speed"],
        "stop" : system_state["emergency_stop"]
    }

# 사용자용 API - 대시보드에서 수동제어 
@app.get('/control/{command}')
async def set_control(command:str, value: int = 0):
    global system_state
    if command =='mode':
        system_state["control_mode"] = "MANUAL" if value ==1 else "AUTO"
    elif command == "fan":
        system_state['fan_speed'] = value
    elif command == "stop":
        system_state["emergency_stop"] = bool(value)

    return {"status":"command_received","current":system_state}

# 대시보드용 API - 현재 전체 상태 조회
@app.get("/status")
async def get_status():
    return system_state

if __name__ =="__main__":
    uvicorn.run(app,host="0.0.0.0", port=8000)