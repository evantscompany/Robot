# vision_ai.py
import cv2
import logging
from ultralytics import YOLO

# 1. 로깅 설정 (실무에서는 터미널 출력보다 로그 파일 남기는 것이 필수)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MetaVisionSystem:
    def __init__(self, model_path='yolov8n.pt'): # 기본값으로 나노 모델 사용
        """
        AI 모델 초기화 및 로드
        """
        try:
            # 실무 팁: 실제 농장에서는 '딸기', '토마토' 등 전용 커스텀 모델(.pt)을 경로로 지정합니다.
            self.model = YOLO(model_path)
            logger.info(f"모델 로드 성공: {model_path}")
        except Exception as e:
            logger.error(f"모델 로드 실패: {e}")
            raise

    def analyze_frame(self, frame):
        """
        단일 프레임을 분석하여 탐지된 객체 리스트 반환
        """
        results = self.model(frame, stream=False, verbose=False)
        detections = []

        for r in results:
            for box in r.boxes:
                # 데이터 구조화 (VLA나 클라우드로 보낼 핵심 정보)
                det_info = {
                    "class": r.names[int(box.cls)],
                    "confidence": float(box.conf),
                    "bbox": box.xyxy[0].tolist(), # [x1, y1, x2, y2]
                    "center": [
                        float((box.xyxy[0][0] + box.xyxy[0][2]) / 2),
                        float((box.xyxy[0][1] + box.xyxy[0][3]) / 2)
                    ]
                }
                detections.append(det_info)
        
        return detections

    def run_inference(self, source=0):
        """
        실시간 스트리밍 분석 (카메라 또는 영상 파일)
        """
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            logger.error("카메라를 열 수 없습니다.")
            return

        logger.info("실시간 분석 시작...")
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # AI 분석 수행
            detections = self.analyze_frame(frame)

            # 화면 시각화 (실무에서는 모니터링용으로 사용)
            for det in detections:
                x1, y1, x2, y2 = map(int, det["bbox"])
                label = f"{det['class']} {det['confidence']:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow("MetaFarmer Vision AI System", frame)
            
            # 분석 데이터 로그 출력 (이 데이터가 VLA로 전달됨)
            if detections:
                logger.info(f"탐지 데이터: {detections}")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # 실무 시뮬레이션: 카메라 0번으로 가동
    vision = MetaVisionSystem()
    vision.run_inference(source=0)
