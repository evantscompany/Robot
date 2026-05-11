# l1 = 첫번째 팔의 길이 (어깨-팔꿈치)
# l2 = 두번째 팔의 길이 (팔꿈치-손끝)
# theta1,theta2 = 각 관절의 각도

import math

class RobotArmIK:
    def __init__(self,l1,l2):
        self.l1 = l1 #첫번째 팔길이
        self.l2 = l2 #두번째 팔길이

    def calculate_angles(self, x,y):
        """좌표 (x,y)를 주면 관절 각도 theta1,theta2를 반환"""
        try:
            # 1. 손끝까지의 거리 계산 (피타고라스)
            d_sq = x**2+y**2
            d = math.sqrt(d_sq)

            # 2. 코사인 법칙을 이용해서 theta2(팔꿈치) 계산
            cos_theta2 = (d_sq - self.l1**2-self.l2**2) / (2 * self.l1 * self.l2)
            # 물리적으로 닿을 수 없는 거리면 에러 발생
            if not(-1<=cos_theta2<=1):
                return None, "거리가 너무 멉니다."
            
            theta2 = math.acos(cos_theta2) # 라디안 값

            # 3. theta1(어깨) 계산
            alpha = math.atan2(y,x)
            beta = math.atan2(self.l2*math.sin(theta2), self.l1 + self.l2*math.cos(theta2))
            theta1 = alpha - beta

            # 4. 라디안을 -> 도(degree)로 변환
            deg1 = math.degrees(theta1)
            deg2 = math.degrees(theta2)

            return (round(deg1,2),round(deg2,2)), "계산 성공"

        except Exception as e :
            return None, str(e)


# 시뮬레이션
# 팔길이 100, 100인 로봇팔 생성
arm = RobotArmIK(100,100)

# 목표좌표(100,100)으로 가려면?
target_x, target_y = 120,50
angles, message = arm.calculate_angles(target_x,target_y)

if angles:
    print(f"목표 좌표: ({target_x}, {target_y})")
    print(f"관절1(어깨): {angles[0]}°")
    print(f"관절2(팔꿈치): {angles[1]}°")
    print(f"이 각도값을 CAN ID 0x200에 실어 보내면 로봇이 움직입니다!")
else:
    print(f"경고: {message}")
