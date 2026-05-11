class PIDController:
    def __init__(self,Kp,Ki,Kd):
        self.Kp = Kp    #비례 이득
        self.Ki = Ki    #적분 이득
        self.Kd = Kd    #미분 이득

        self.prev_error = 0
        self.integral = 0

    def calculate(self, target , current, dt):
        error = target - current

        # P항 : 현재 오차
        P_out = self.Kp * error

        # I항 : 오차의 누적 (미세 오차 제거)
        self.integral += error * dt
        I_out = self.Ki * self.integral

        # D항 : 오차의 변화율 (급격한 변화 방지)
        derivative = (error - self.prev_error) / dt
        D_out = self.Kd * derivative

        self.prev_error

        # 최종 출력값 (모터에 전달할 힘)
        return P_out + I_out + D_out