from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import asyncio
import uvicorn

app = FastAPI()

# =========================================
# ECU 상태
# =========================================

state = {
    "is_running": False,
    "input_mode": "WEB",

    "accel_pos": 0,

    "rpm": 0,
    "speed": 0,

    "engine_temp": 25.0,
    "fan_speed": 0,

    "emergency_stop": False,
    "overheat_timer": 0
}

# 그래프 기록용
history = {
    "rpm": [],
    "temp": []
}

MAX_HISTORY = 30

# =========================================
# 엔진 물리 연산
# =========================================

async def engine_physics():

    while True:

        if state["is_running"] and not state["emergency_stop"]:

            # 목표 RPM
            target_rpm = state["accel_pos"] * 25

            # RPM 변화
            state["rpm"] += (
                target_rpm - state["rpm"]
            ) * 0.2

            # 속도 계산
            state["speed"] = state["rpm"] * 0.04

            # 발열 계산
            heat_gain = (
                state["rpm"] / 2500
            ) * 0.5

            # 자동 팬 제어
            if state["engine_temp"] >= 80:

                state["fan_speed"] = 255

            elif state["engine_temp"] >= 50:

                state["fan_speed"] = 128

            else:

                state["fan_speed"] = 0

            # 냉각 계산
            cool_loss = (
                (state["fan_speed"] / 255) * 0.3
            ) + 0.05

            # 온도 반영
            state["engine_temp"] += (
                heat_gain - cool_loss
            )

            # 과열 체크
            if state["engine_temp"] >= 100:

                state["overheat_timer"] += 1

                if state["overheat_timer"] >= 10:

                    state["is_running"] = False
                    state["emergency_stop"] = True

                    print("!!! ENGINE OVERHEAT !!!")

            else:

                state["overheat_timer"] = 0

        else:

            # 시동 OFF

            state["rpm"] *= 0.8
            state["speed"] *= 0.8

            if state["engine_temp"] > 25:

                state["engine_temp"] -= 0.1

        # 최소 온도 제한
        state["engine_temp"] = max(
            25.0,
            state["engine_temp"]
        )

        # 그래프 데이터 저장
        history["rpm"].append(
            int(state["rpm"])
        )

        history["temp"].append(
            int(state["engine_temp"])
        )

        # 길이 제한
        if len(history["rpm"]) > MAX_HISTORY:

            history["rpm"].pop(0)

        if len(history["temp"]) > MAX_HISTORY:

            history["temp"].pop(0)

        await asyncio.sleep(1)

# =========================================
# 서버 시작
# =========================================

@app.on_event("startup")
async def startup_event():

    asyncio.create_task(
        engine_physics()
    )

# =========================================
# WOKWI 동기화
# =========================================

@app.post("/tractor/sync")
async def sync_tractor(data: dict):

    if state["input_mode"] == "WOKWI":

        state["accel_pos"] = data.get(
            "temp",
            0
        )

    return {

        "fan_speed": state["fan_speed"],

        "stop": (
            state["emergency_stop"]
            or
            not state["is_running"]
        ),

        "server_temp": int(
            state["engine_temp"]
        )
    }

# =========================================
# WEB 엑셀
# =========================================

@app.get("/control/accel")
async def set_accel(value: int):

    if state["input_mode"] == "WEB":

        value = max(
            0,
            min(100, value)
        )

        state["accel_pos"] = value

    return state

# =========================================
# 입력 모드
# =========================================

@app.get("/control/input")
async def set_input_mode(mode: str):

    if mode in ["WEB", "WOKWI"]:

        state["input_mode"] = mode

    return state

# =========================================
# 시동 제어
# =========================================

@app.get("/control/engine")
async def control_engine(action: str):

    if action == "start":

        state["is_running"] = True
        state["emergency_stop"] = False

    elif action == "stop":

        state["is_running"] = False

    return state

# =========================================
# 리셋
# =========================================

@app.get("/control/reset")
async def reset_emergency():

    state["emergency_stop"] = False

    return state

# =========================================
# 상태 조회
# =========================================

@app.get("/status")
async def get_status():

    return {
        "state": state,
        "history": history
    }

# =========================================
# 프론트
# =========================================

@app.get("/", response_class=HTMLResponse)
async def dashboard():

    return """

<!DOCTYPE html>
<html>

<head>

<title>TRACTOR ECU</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

body{
    background:#111;
    color:#0f0;
    font-family:Arial;
    padding:30px;
}

.card{
    border:2px solid #0f0;
    border-radius:10px;
    padding:20px;
    margin-bottom:20px;
    width:600px;
}

.title{
    font-size:36px;
    margin-bottom:20px;
}

.data{
    font-size:24px;
    margin:10px 0;
}

button{
    padding:15px 20px;
    font-size:18px;
    margin:5px;
    cursor:pointer;
}

.slider{
    width:400px;
}

canvas{
    background:#222;
    padding:10px;
}

</style>

</head>

<body>

<div class="title">
 TRACTOR ECU SIMULATOR
</div>

<div class="card">

<div class="data">
MODE :
<span id="mode">
WEB
</span>
</div>

<div class="data">
ENGINE :
<span id="engine">
OFF
</span>
</div>

<div class="data">
RPM :
<span id="rpm">
0
</span>
</div>

<div class="data">
SPEED :
<span id="speed">
0
</span> km/h
</div>

<div class="data">
TEMP :
<span id="temp">
25
</span> °C
</div>

<div class="data">
FAN :
<span id="fan">
0
</span>
</div>

<div class="data">
ACCEL :
<span id="accel">
0
</span> %
</div>

<div class="data">
EMERGENCY :
<span id="emg">
FALSE
</span>
</div>

</div>

<div class="card">

<div class="data">
ACCEL PEDAL
</div>

<input
type="range"
min="0"
max="100"
value="0"
class="slider"
id="accelSlider"
oninput="setAccel(this.value)"
>

<div class="data">
PEDAL :
<span id="pedalValue">
0
</span> %
</div>

</div>

<button onclick="engineStart()">
ENGINE START
</button>

<button onclick="engineStop()">
ENGINE STOP
</button>

<button onclick="resetEmergency()">
RESET EMERGENCY
</button>

<br><br>

<button onclick="setMode('WEB')">
WEB MODE
</button>

<button onclick="setMode('WOKWI')">
WOKWI MODE
</button>

<br><br>

<div class="card">

<canvas id="rpmChart"></canvas>

</div>

<div class="card">

<canvas id="tempChart"></canvas>

</div>

<script>

const rpmCtx =
document.getElementById('rpmChart')

const tempCtx =
document.getElementById('tempChart')

const rpmChart =
new Chart(rpmCtx, {

    type:'line',

    data:{
        labels:[],
        datasets:[{
            label:'RPM',
            data:[]
        }]
    }
})

const tempChart =
new Chart(tempCtx, {

    type:'line',

    data:{
        labels:[],
        datasets:[{
            label:'TEMP',
            data:[]
        }]
    }
})

async function updateStatus(){

    const res =
    await fetch('/status')

    const data =
    await res.json()

    const s = data.state
    const h = data.history

    document.getElementById(
        'mode'
    ).innerText =
        s.input_mode

    document.getElementById(
        'rpm'
    ).innerText =
        parseInt(s.rpm)

    document.getElementById(
        'speed'
    ).innerText =
        parseInt(s.speed)

    document.getElementById(
        'temp'
    ).innerText =
        parseInt(s.engine_temp)

    document.getElementById(
        'fan'
    ).innerText =
        s.fan_speed

    document.getElementById(
        'accel'
    ).innerText =
        s.accel_pos

    document.getElementById(
        'engine'
    ).innerText =
        s.is_running
        ? "ON"
        : "OFF"

    document.getElementById(
        'emg'
    ).innerText =
        s.emergency_stop
        ? "TRUE"
        : "FALSE"

    document.getElementById(
        'accelSlider'
    ).value =
        s.accel_pos

    document.getElementById(
        'pedalValue'
    ).innerText =
        s.accel_pos

    // RPM 그래프
    rpmChart.data.labels =
        h.rpm.map((_,i)=>i)

    rpmChart.data.datasets[0].data =
        h.rpm

    rpmChart.update()

    // TEMP 그래프
    tempChart.data.labels =
        h.temp.map((_,i)=>i)

    tempChart.data.datasets[0].data =
        h.temp

    tempChart.update()
}

async function setAccel(value){

    await fetch(
        `/control/accel?value=${value}`
    )
}

async function engineStart(){

    await fetch(
        '/control/engine?action=start'
    )
}

async function engineStop(){

    await fetch(
        '/control/engine?action=stop'
    )
}

async function resetEmergency(){

    await fetch(
        '/control/reset'
    )
}

async function setMode(mode){

    await fetch(
        `/control/input?mode=${mode}`
    )
}

setInterval(
    updateStatus,
    1000
)

updateStatus()

</script>

</body>
</html>

"""

# =========================================
# 실행
# =========================================

if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )