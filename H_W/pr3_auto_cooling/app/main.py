from fastapi import FastAPI
import uvicorn
from fastapi.responses import HTMLResponse
import sqlite3
from datetime import datetime

app = FastAPI()

# --- 1. DB 설정 (정비 장부 초기화) ---
def init_db():
    conn = sqlite3.connect("tractor_log.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temp_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temp INTEGER,
            led_status TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# 실시간 상태 메모리 저장
data_store = {"temp": 0, "led": "OFF"}

# --- 2. 데이터 수신 및 DB 저장 ---
@app.post("/update")
async def update_data(data: dict):
    global data_store
    temp = data.get("temp", 0)
    
    # 상태 판단
    led_status = "ON" if temp >= 80 else "OFF"
    data_store = {"temp": temp, "led": led_status}

    # DB에 기록 기입
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("tractor_log.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO temp_logs (timestamp, temp, led_status) VALUES (?, ?, ?)", 
                   (now, temp, led_status))
    conn.commit()
    conn.close()

    print(f"[{now}] 온도: {temp}도 -> DB 저장 완료")
    return {"status": "success"}

# --- 3. 명령 및 상태 조회 API ---
@app.get("/command")
async def get_command():
    return {"led": data_store["led"]}

@app.get("/status")
async def get_all_status():
    return data_store

@app.get("/history")
async def get_history():
    conn = sqlite3.connect("tractor_log.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, temp, led_status FROM temp_logs ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    # 텐키리스 리스트 반환
    return [{"time": r[0], "temp": r[1], "status": r[2]} for r in rows]

# --- 4. 웹 대시보드 ---
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>엔진 온도 모니터링 시스템</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { font-family: sans-serif; text-align: center; background: #f4f7f6; padding: 20px; }
            .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            .status-display { font-size: 20px; margin: 20px; font-weight: bold; }
            .warning { color: #ff4757; animation: blink 1s infinite; }
            @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
            .progress-container { width: 80%; margin: 10px auto; background: #ddd; border-radius: 10px; height: 20px; overflow: hidden; }
            .progress-bar { width: 0%; height: 100%; background: #3498db; transition: 0.5s; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1> 트랙터 엔진 실시간 진단기</h1>
            <div id="alarm" class="status-display">상태: 정상</div>
            <canvas id="tempChart"></canvas>

            <hr>
            <div class="status-display">냉각 밸브 개방도: <span id="valveText">0</span>%</div>
            <div class="progress-container"><div id="valveBar" class="progress-bar"></div></div>

            <hr>
            <div id="history-table"><h3>최근 10개 정비 기록 로딩 중...</h3></div>
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
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: { scales: { y: { min: 0, max: 100 } } }
            });

            async function updateDashboard() {
                try {
                    // 1. 실시간 차트 및 밸브 업데이트
                    const res = await fetch('/status');
                    const data = await res.json();
                    const now = new Date().toLocaleTimeString();

                    if (tempChart.data.labels.length > 20) {
                        tempChart.data.labels.shift();
                        tempChart.data.datasets[0].data.shift();
                    }
                    tempChart.data.labels.push(now);
                    tempChart.data.datasets[0].data.push(data.temp);
                    
                    const valvePercent = Math.min(100, Math.max(0, Math.round((data.temp - 30) * 1.43)));
                    document.getElementById('valveBar').style.width = valvePercent + "%";
                    document.getElementById('valveText').innerText = valvePercent;

                    const alarmEl = document.getElementById('alarm');
                    if (data.temp >= 80) {
                        tempChart.data.datasets[0].borderColor = '#ff4757';
                        alarmEl.innerText = " 경고: 엔진 과열! 쿨링팬 작동 중";
                        alarmEl.className = "status-display warning";
                    } else {
                        tempChart.data.datasets[0].borderColor = '#2ed573';
                        alarmEl.innerText = " 상태: 정상";
                        alarmEl.className = "status-display";
                    }
                    tempChart.update();
                } catch (e) { console.error(e); }
            }

            async function updateHistory() {
                try {
                    const res = await fetch('/history');
                    const logs = await res.json();
                    let html = "<h3> 최근 10개 정비 이력 (DB)</h3><table><tr><th>시간</th><th>온도</th><th>상태</th></tr>";
                    logs.forEach(log => {
                        html += `<tr><td>${log.time}</td><td>${log.temp}℃</td><td>${log.status}</td></tr>`;
                    });
                    html += "</table>";
                    document.getElementById('history-table').innerHTML = html;
                } catch (e) { console.error(e); }
            }

            setInterval(updateDashboard, 1000);
            setInterval(updateHistory, 5000); // 기록은 5초마다 갱신
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)