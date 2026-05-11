import network, urequests, utime, machine
from machine import Pin, ADC, PWM

# 1. 하드웨어 설정 (GPIO 1: 가변저항/엑셀, GPIO 2: 초록LED, GPIO 3: 빨강LED)
# 가속 페달 (Potentiometer)
accel_pedal = ADC(Pin(1))
accel_pedal.atten(ADC.ATTN_11DB)

# 대시보드 상태 LED (RGB의 R, G핀 활용)
led_g = PWM(Pin(2), freq=1000)
led_r = PWM(Pin(3), freq=1000)

# 2. WiFi 연결 (Wokwi 가상 WiFi)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Wokwi-GUEST", "")

print("WiFi 연결 중...")
while not wlan.isconnected():
    utime.sleep(0.5)
print("WiFi 연결 완료!")

# 3. 서버 설정 (본인의 ngrok http 주소를 넣으세요)
# 주의: https가 아닌 http 주소를 사용해야 mbedtls 에러를 방지할 수 있습니다.
SERVER_URL = "http://bulb-plural-lushly.ngrok-free.dev/tractor/sync"

# ngrok 보안 페이지 우회 및 JSON 통신용 헤더
custom_headers = {
    "User-Agent": "ESP32-Tractor-ECU",
    "ngrok-skip-browser-warning": "1",
    "Content-Type": "application/json"
}

print("--- 트랙터 시스템 가동 (물리 엔진 모드) ---")

while True:
    try:
        # 가변저항 값을 읽어서 0~100 사이의 엑셀 개도로 변환
        raw_val = accel_pedal.read()
        accel_pos = int((raw_val / 4095) * 100)
        
        # 서버(ECU)에 현재 엑셀 위치 보고
        payload = {"temp": accel_pos} # 기존 키값 유지
        res = urequests.post(SERVER_URL, json=payload, headers=custom_headers)
        
        if res.status_code == 200:
            data = res.json()
            
            # 서버 물리 엔진이 계산한 결과값들
            server_temp = data.get("server_temp", 25) # 서버가 계산한 가상 수온
            is_halt = data.get("stop", False)        # 시동 꺼짐 또는 비상 정지 여부
            
            # 터미널에 실시간 상태 출력
            print(f"[현황] 엑셀: {accel_pos}% | 가상수온: {server_temp}C | 시동상태: {'OFF' if is_halt else 'ON'}")

            # --- 대시보드 LED 제어 로직 ---
            if is_halt:
                # 시동이 꺼졌거나 비상 정지 시: 빨간불 고정
                led_g.duty(0)
                led_r.duty(1023)
            elif server_temp >= 80:
                # 수온 80도 이상 경고: 빨간불 점등
                led_g.duty(0)
                led_r.duty(1023)
            else:
                # 정상 작동: 수온이 높을수록 초록색 LED가 밝아지게 설정 (시각적 피드백)
                brightness = int((server_temp / 80) * 1023)
                led_g.duty(max(100, brightness)) # 최소 밝기 100 유지
                led_r.duty(0)
            
            res.close()
            
    except Exception as e:
        print("서버 통신 에러 (정비 필요):", e)
        # 통신 에러 발생 시 적색 LED 깜빡임 (비상 모드)
        led_g.duty(0)
        led_r.duty(512)
        utime.sleep(0.5)
        led_r.duty(0)

    # 1초 주기로 서버와 동기화
    utime.sleep(1)