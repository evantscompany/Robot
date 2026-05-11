import time

class RobotFSM:
    def __init__(self):
        # 로봇의 현재 상태 정의
        self.state = "IDLE" # 초기 상태 : 대기
        print(f"시스템 시작 : 현재상태는 [{self.state}]")

    def update(self, event=None):
        """상태전환로직"""

        if self.state == "IDLE":
            if event == "TARGET_RECEIVED":
                print("\n[IDLE -> CALCULATING] 좌표를 받았음. 역운동학 계산을 시작합니다. ")
                self.state = "CALCULATING"
                self.process_calculating()
        
        elif self.state == "CALCULATING":
            # 역운동학 계산이 끝났다고 가정
            print("[CALCULATING -> MOVING] 계산 완료. CAN ID 0x200 으로 각도 데이터를 전송합니다.")
            self.state = "MOVING"
            self.process_moving()

        elif self.state == "MOVING":
            # 실제 모터가 이동 중인 상태
            print("[MOVING -> COMPLETED] 로봇 팔이 목표 지점에 도착했습니다.")
            self.state = "COMPLETED"
            self.process_completed()
        
        elif self.state == "COMPLETED":
            print("[COMPLETED -> IDLE] 작업을 마치고 다음 명령을 위해 대기 상태로 복귀합니다.")
            self.state = "IDLE"

    def process_calculating(self):
        time.sleep(1) # 계산 중인 척 하는 시간
        self.update()

    def process_moving(self):
        time.sleep(2) # 로봇이 스윽 움직이는 시간
        self.update()

    def process_completed(self):
        time.sleep(1)
        self.update()

# --- 실행 시뮬레이션 ---
robot = RobotFSM()

# 사용자가 마우스로 좌표를 클릭했다고 가정 (이벤트 발생)
print("\n--- 작업 시작: 마우스 클릭됨 ---")
robot.update("TARGET_RECEIVED")