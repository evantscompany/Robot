# app/main.py
# 이번차는 LED 상태를 저장하고 전달하는 기능 구현

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# 일단 fastAPI 객체 생성
app = FastAPI()

# LED 상태 저장(메모리 저장방식)
led_status = {"state":"OFF"}

@app.get("/",response_class = HTMLResponse)
async def read_dashboard():
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>원격 장비 제어</title>
        <style>
            body {{ font-family: sans-serif; text-align: center; padding: 50px; background: #f0f2f5; }}
            .card {{ background: white; padding: 30px; border-radius: 20px; display: inline-block; shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            button {{ font-size: 20px; padding: 15px 30px; margin: 10px; cursor: pointer; border: none; border-radius: 10px; transition: 0.3s; }}
            .btn-on {{ background: #ff4757; color: white; }}
            .btn-off {{ background: #2f3542; color: white; }}
            button:hover {{ opacity: 0.8; transform: scale(1.05); }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>PR2 원격 제어판</h1>
            <p>현재 LED 상태: <strong id="statusText">확인 중...</strong></p>
            <button class="btn-on" onclick="sendControl('ON')">경고등 켜기 (ON)</button>
            <button class="btn-off" onclick="sendControl('OFF')">경고등 끄기 (OFF)</button>
        </div>

        <script>
            async function sendControl(state) {{
                await fetch('/control', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ "state": state }})
                }});
                updateStatus();
            }}

            async function updateStatus() {{
                const res = await fetch('/status');
                const data = await res.json();
                document.getElementById('statusText').innerText = data.state;
            }}
            
            setInterval(updateStatus, 1000); // 1초마다 상태 갱신
        </script>
    </body>
    </html>
    '''
# post 방식으로 LED 상태 변경
@app.post("/control")
async def control_led(data:dict): # 비동기 함수
    global led_status               # 전역 변수 사용
    led_status["state"] = data.get("state", "OFF")  # 상태 업데이트
    return led_status                               # 현재 상태 반환

# LED 상태 조회
@app.get("/status")
async def get_status():
    return led_status

@app.get("/get-led")
async def get_led():
    """Wokwi 기계(MicroPython)가 사용하는 데이터 경로"""
    return {"led": led_status["state"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
