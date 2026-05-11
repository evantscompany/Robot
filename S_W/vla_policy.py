# vla_policy.py

import logging

# 로깅설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MetaPolicy:
    def __init__(self,confidence_threshold=0.6):
        # 임계값 0.6 이상
        self.threshold = confidence_threshold

    def decide_action(self, language_command, detections):
        """
        인식데이터(vision)와 사용자 명령(language)을 결합해 행동 결정
        """
        if not detections:
            return "No_Object_Detected", "주변을 탐색하며 작물을 찾습니다"

        action = []
        for det in detections:
            obj_name = det['class']
            conf = det['confidence']

            # 신뢰도 필터
            if conf < self.threshold:
                logger.warning(f"신뢰도 낮음({conf:.2f}):{obj_name} 인식을 무시합니다")
                continue

            # VLA 판단 로직 (명령어와 객체 매칭)
            if "수확" in language_command:
                if obj_name in ["apple","orange","strawberry"]:
                    action.append(f"{obj_name}  수확 시작 (엔드이펙터 구동)")
                elif obj_name == "cell phone":
                    action.append(f"주의 {obj_name}은 작물이 아닙니다. 작업을 건너뜁니다")
                else:
                    action.append(f"{obj_name}은 수확 대상이 아닙니다.")

            elif "예찰" in language_command:
                action.append(f"{obj_name}상태 기록 및 클라우드 전송")

        return "Success", action

if __name__ == "__main__":
    # 실무 시뮬레이션
    policy = MetaPolicy(confidence_threshold=0.5)

    mock_detections = [
        {"class":"cell phone","confidence":0.85},
        {"class":"apple","confidence":0.30} #신뢰도 낮음
    ]

    command = "잘 익은 작물만 수확해줘"
    status, final_actions = policy.decide_action(command,mock_detections)

    print(f"\n --- 로봇 최종 행동 지시(Status : {status})---")
    for a in final_actions:
        print(f"->{a}")