# app/main.py

from fastapi import FastAPI
import sqlite3
from datetime import datetime
# 아까 만든 hardware.py 파일에서 hardware_service라는 기술자를 데려옵니다.
from .services.hardware import hardware_service
from fastapi.responses import HTMLResponse

# FastAPI의 본체를 생성합니다. 이 객체가 서버 전체를 관리합니다.
app = FastAPI(
    title="ARM 제어 시스템 기초",
    description="하드웨어 제어를 위한 백엔드 API 서버입니다."
)

def init_db():
    # sensor_data.db 파일 생성 및 연결
    conn = sqlite3.connect("sensor_data.db")
    cursor = conn.cursor()
    # 테이블이 없으면 생성 (시간,온도,습도)
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS sensor_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME,
        temperature REAL,
        humidity REAL
        )
        ''')
    conn.commit()
    conn.close()
init_db() #서버 시작 시 데이터베이스 초기화

# @app.get("/")
# def read_root():
#     """
#     서버가 잘 살아있는지 확인하는 기본 주소 (http://localhost:8000/)
#     """
#     return {"message": "ARM Backend 서버가 정상 작동 중입니다."}

@app.post("/led/{status}")
def control_led(status: bool):
    """
    사용자가 'LED 켜줘'라고 요청하면 실행되는 함수
    :param status: URL에 들어가는 값 (True 또는 False)
    """
    # 접수된 요청을 하드웨어 기술자(hardware_service)에게 전달합니다.
    result = hardware_service.set_led(status)
    return result

@app.get("/sensor")
def read_sensor():
    """
    사용자가 '지금 센서값 어때?'라고 물어보면 실행되는 함수
    """
    # 기술자에게 센서 값을 읽어오라고 시키고 그 결과를 사용자에게 보여줍니다.
    data = hardware_service.get_sensor_data()
    return data

@app.post("/update-sensor")
async def update_sensor(data: dict):
    """
    ESP32 가 실제 센서값을 이쪽으로 씀 (POST요청)
    """
    temp = data.get("temperature")
    humi = data.get("humidity")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # DB에 저장
    conn = sqlite3.connect("sensor_data.db")
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO sensor_logs (timestamp, temperature, humidity)
        VALUES (?, ?, ?)
        ''',
        (timestamp, temp, humi)
    )
    conn.commit()
    conn.close()

    print(f"[DB 저장 완료] {timestamp} - 온도: {temp}도, 습도: {humi}%")
    return{"status":"success","message":"Data logged to DB"} 

    print(f"[현장 데이터 수신] 온도 : {temp}도, 습도:{humi}퍼센트")
    return {"status": "success","received":{"temp":temp, "humi": humi}}


# 저장된 데이터 확인용 엔드포인트
@app.get("/history")
def get_history():
    conn = sqlite3.connect("sensor_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_logs ORDER BY timestamp DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    
    # 보기 좋게 리스트로 반환
    history =[{"id": row[0], "timestamp": row[1], "temperature": row[2], "humidity": row[3]} for row in rows]
    return {"history": history}

@app.get("/", response_class=HTMLResponse)
async def read_dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>IoT 실시간 모니터링</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { font-family: 'Malgun Gothic', sans-serif; text-align: center; background: #f4f4f4; padding: 20px; }
            .container { width: 90%; max-width: 1000px; margin: auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            canvas { background: #fff; margin-top: 20px; max-height: 500px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚜 트랙터 실시간 데이터 관제창</h1>
            <p>2초마다 DB에서 최신 정보를 가져옵니다.</p>
            <canvas id="sensorChart"></canvas>
        </div>
        <script>
            const ctx = document.getElementById('sensorChart').getContext('2d');
            const sensorChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: '온도 (°C)',
                        data: [],
                        borderColor: '#ff6384',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        fill: true,
                        tension: 0.4
                    }, {
                        label: '습도 (%)',
                        data: [],
                        borderColor: '#36a2eb',
                        backgroundColor: 'rgba(54, 162, 235, 0.1)',
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { min: 0, max: 100 }
                    }
                }
            });

            async function updateChart() {
                try {
                    const response = await fetch('/history');
                    const result = await response.json();
                    
                    if (result.history && result.history.length > 0) {
                        // 최신순 데이터를 시간순(과거->현재)으로 반전
                        const history = result.history.reverse(); 

                        // 데이터 매핑 (사용자 데이터 필드명에 맞춤)
                        sensorChart.data.labels = history.map(row => row.timestamp.split(' ')[1]);
                        sensorChart.data.datasets[0].data = history.map(row => row.temperature);
                        sensorChart.data.datasets[1].data = history.map(row => row.humidity);
                        
                        sensorChart.update('none'); // 애니메이션 없이 부드럽게 업데이트
                    }
                } catch (e) {
                    console.error("차트 업데이트 에러:", e);
                }
            }

            setInterval(updateChart, 2000); // 2초마다 실행
            updateChart(); // 시작하자마자 한 번 실행
        </script>
    </body>
    </html>
    """