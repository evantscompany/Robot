class SimpleKalman:
    def __init__(self):
        self.estimate = 0.0         #최종 예측값 (내가 원하는 깨끗한 데이터)
        self.error_est = 1.0        #예측 오차
        self.error_meas = 0.5       #센서 오차 (센서가 얼마나 믿을만한지)
        self.last_estimate = 0.0

    def update(self, measurement):
        # 1. 칼만 이득 계산 (어느 쪽을 더 믿을지 결정)
        kalman_gain = self.error_est / (self.error_est + self.error_meas)

        # 2. 현재 측정 값으로 최종 예측값 업데이트
        self.estimate = self.last_estimate + kalman_gain * (measurement - self.last_estimate)

        # 3. 예측 오차 업데이터 (다음 계산을 위해)
        self.error_est = (1.0-kalman_gain) * self.error_est
        self.last_estimate = self.estimate

        return self.estimate

# 실습 시뮬레이션

kf = SimpleKalman()
raw_data = [10.1,9.8,11.5,9.2,10.5] #지분거리는 센서 원본데이터

print("필터링 시작")
for val in raw_data:
    filtered = kf.update(val)
    print(f"센서값 : {val} >>> 필터링 된 값 : {filtered:.2f}")