from fastapi import FastAPI
import uvicorn
from fastapi.responses import HTMLResponse

app = FastAPI()

# 상태 데이터
data_store = {
    "temp": 0,
    "led": "OFF"
}

@app.post("/update")
async def update_data(data: dict):
    global data_store
    temp = data.get("temp", 0)
    data_store["temp"] = temp

    if temp >= 80:
        data_store["led"] = "ON"
    else:
        data_store["led"] = "OFF"
    
    print(f"현재 온도: {temp}도 -> 경고등 상태: {data_store['led']}")
    return {"status": "success"}

@app.get("/command")
async def get_command():
    return {"led": data_store["led"]}

@app.get("/status")
async def get_all_status():
    return data_store

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>엔진 온도 모니터링</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { font-family: sans-serif; text-align: center; background: #f4f7f6; padding: 20px; }
            .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            .status-display { font-size: 20px; margin: 20px; font-weight: bold; }
            .warning { color: #ff4757; animation: blink 1s infinite; }
            @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
            .progress-container { width: 80%; margin: 20px auto; background: #ddd; border-radius: 10px; height: 25px; overflow: hidden; }
            .progress-bar { width: 0%; height: 100%; background: #3498db; transition: 0.5s; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚜 실시간 엔진 온도 데이터</h1>
            <div id="alarm" class="status-display">상태: 정상</div>
            
            <canvas id="tempChart"></canvas>

            <hr>
            <div class="status-display">냉각 밸브(서보) 개방도: <span id="valveText">0</span>%</div>
            <div class="progress-container">
                <div id="valveBar" class="progress-bar"></div>
            </div>
        </div>

        <script>
            const ctx = document.getElementById('tempChart').getContext('2d');
            const tempChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: '엔진 온도 (°C)',
                        data: [],
                        borderColor: '#2ed573',
                        backgroundColor: 'rgba(46, 213, 115, 0.1)',
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: {
                    scales: { y: { min: 0, max: 100 } }
                }
            });

            async function updateChart() {
                try {
                    const res = await fetch('/status');
                    const data = await res.json();
                    
                    const now = new Date().toLocaleTimeString();
                    
                    // 1. 그래프 업데이트
                    if (tempChart.data.labels.length > 20) {
                        tempChart.data.labels.shift();
                        tempChart.data.datasets[0].data.shift();
                    }
                    tempChart.data.labels.push(now);
                    tempChart.data.datasets[0].data.push(data.temp);
                    
                    // 2. 밸브 바 업데이트 (온도 기반 계산: 30도 시작, 100도 끝)
                    const valvePercent = Math.min(100, Math.max(0, Math.round((data.temp - 30) * 1.43)));
                    document.getElementById('valveBar').style.width = valvePercent + "%";
                    document.getElementById('valveText').innerText = valvePercent;

                    // 3. 알람 및 색상 변경
                    const alarmEl = document.getElementById('alarm');
                    if (data.temp >= 80) {
                        tempChart.data.datasets[0].borderColor = '#ff4757';
                        alarmEl.innerText = "🔥 경고: 엔진 과열! 쿨링팬 작동 중";
                        alarmEl.className = "status-display warning";
                    } else {
                        tempChart.data.datasets[0].borderColor = '#2ed573';
                        alarmEl.innerText = "✅ 상태: 정상";
                        alarmEl.className = "status-display";
                    }
                    
                    tempChart.update();
                } catch (e) {
                    console.error("데이터 로드 실패", e);
                }
            }

            setInterval(updateChart, 1000);
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)