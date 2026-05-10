import time
import random

# 1. CAN 버스 (공용 도로 역할 하는 클래스)

class CANBus:
    def __init__(self):
        self.subscribers = [] # 연결된 장치들
    
    def connect(self, device):
        self.subscribers.append(device)
    
    def broadcast(self,sender_name,can_id,data):
        """도로에 뿌리면 일단 모든 장치가 일단 다 들음"""
        # 실제 CAN 통신처럼 ID가 낮을수록 우선순위가 높다고 가정(시뮬레이션용)
        print(f"\n[BUS]{sender_name}가 ID{hex(can_id)}로 데이터를 뿌립니다 : {data}")

        for device in self.subscribers:
            # 보낸 놈 빼고 나머지에게 전달
            if device.name!=sender_name:
                device.receive(can_id,data)

# 2. CAN 장치 (ECU, 로봇 모터 등등)
class CANDevice:
    def __init__(self,name,interested_ids):
        self.name = name
        self.interested_ids = interested_ids

    def receive(self,can_id,data):
        """데이터를 수신했을때, 내가 관심있는 ID 인지 필터링 """
        if can_id in self.interested_ids:
            print(f"      ㄴ[{self.name}] 수신 성공 -> 데이터 처리중 : {data}")
        else:
            #관심없는 ID 는 하드웨어 수준에서 무시 (filtering)
            pass


# 3. 실험 시작

# 공용 도로 건설
tractor_bus = CANBus()

# 장치들 연결 (이름표 약속 : 0x100 = 엔진, 0x200 = 로봇팔 , 0x300 = 작업기)
engine_ecu = CANDevice("엔진 ECU",interested_ids=[0x200])           #로봇팔(0x200)의 피드백을 기다림
robot_arm = CANDevice("로봇관절_1",interested_ids=[0x100])           #엔진 (0x100)의 피드백을 기다림 
dashboard = CANDevice("계기판",interested_ids=[0x100,0x200,0x300])   #모든 데이터를 모니터링

tractor_bus.connect(engine_ecu)
tractor_bus.connect(robot_arm)
tractor_bus.connect(dashboard)

# 데이터 전송 시뮬레이션
for _ in range(3):
    # 엔진이 현재 상태를 방송 (id 0x100)
    tractor_bus.broadcast("엔진_ECU",0x100,{"RPM":2200,"TEMP":85})
    time.sleep(1)

    # 로봇팔이 현재 각도를 방송 (ID 0x200)
    tractor_bus.broadcast("로봇관절_1",0x200,{"Angle":45.5})
    time.sleep(1)