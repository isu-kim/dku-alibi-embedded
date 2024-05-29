import torch
import numpy as np
from ultralytics import YOLO
import cv2

# YOLO 모델 로드
model = YOLO("C:/Users/doik0/Desktop/yolo/runs/detect/train3/weights/best.pt")
cap = cv2.VideoCapture(0)
["doik", "IU", "shokhrukh", "zabo"]
# 클래스 이름과 해당 색상
classes_info = {
    0: {"name": "doik", "color": (0, 0, 255)},  # "doik"에 대한 빨간색
    1: {"name": "IU", "color": (255, 0, 0)},   # "IU"에 대한 파란색
    2: {"name": "shokhrukh", "color": (255, 255, 0) }, # shokhrukh에 대한 노란색
    3: {"name": "zabo", "color": (0, 0, 0) } # zabo에 대한 검은색
}

# 신뢰도 임계값
confidence_threshold = 0.75

def use_result(results, frame):
    if results and results[0]:
        bboxes = np.array(results[0].boxes.xyxy.cpu(), dtype="int")
        classes = np.array(results[0].boxes.cls.cpu(), dtype="int")
        scores = np.array(results[0].boxes.conf.cpu())  # 신뢰도 점수 가져오기
        pred_box = zip(classes, bboxes, scores)
        
        detected_classes = set()
        for cls, bbox, score in pred_box:
            if score < confidence_threshold:
                class_info = {"name": "Unknown", "color": (0, 255, 0)}  # Default color green for unknown classes
            else:
                detected_classes.add(cls)
                class_info = classes_info.get(cls, {"name": "Unknown", "color": (0, 255, 0)})  # Default color green for unknown classes
            
            (x, y, x2, y2) = bbox
            print(f"bounding box ({x}, {y}, {x2}, {y2}) has class {cls}, which is {class_info['name']}, confidence score: {score:.2f}")
            color = class_info["color"]
            cv2.rectangle(frame, (x, y), (x2, y2), color, 2)
            cv2.putText(frame, class_info["name"], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        # 탐지된 고유한 클래스 수 출력
        print(f"Number of detected classes: {len(detected_classes)}")

        scale_percent = 60  # 원래 크기의 백분율
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        frame_s = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow("Img", frame_s)
    return

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    results = model(frame)
    use_result(results, frame)

    key = cv2.waitKey(1)
    if key == 27:  # ESC 키
        break

cap.release()
cv2.destroyAllWindows()
