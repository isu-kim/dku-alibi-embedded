from scipy.spatial import distance as dist
from imutils import face_utils
import imutils
import dlib
import cv2
import torch
import numpy as np
from ultralytics import YOLO
import os
import time

def eye_aspect_ratio(eye):  # 눈의 비율을 계산하는 함수
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear # 리턴 ear

def lip_distance(shape):  # 하품을 감지하는 함수
    top_lip = shape[50:53]
    top_lip = np.concatenate((top_lip, shape[61:64]))
    low_lip = shape[56:59]
    low_lip = np.concatenate((low_lip, shape[65:68]))
    top_mean = np.mean(top_lip, axis=0)
    low_mean = np.mean(low_lip, axis=0)
    distance = abs(top_mean[1] - low_mean[1])
    return distance

# 눈 감김을 판단하는 임계값과 프레임 설정
thresh = 0.25
frame_check = 20
yawn_thresh = 20  # 하품을 판단하는 임계값

# 얼굴 검출기와 랜드마크 예측기 설정
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("C:\\yolov8\\dku-alibi-embedded\\sleepy\\models\\shape_predictor_68_face_landmarks.dat")
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

# 추가 얼굴 검출기와 랜드마크 예측기 설정 
detector = cv2.CascadeClassifier("C:\\yolov8\\dku-alibi-embedded\\sleepy\\yawn_models\\yawn_plus.xml")
predictor = dlib.shape_predictor("C:\\yolov8\\dku-alibi-embedded\\sleepy\\yawn_models\\shape_predictor_face_landmarks.dat")


cap = cv2.VideoCapture(0)

# YOLO 모델 로드
model = YOLO("C:\\yolov8\\dku-alibi-embedded\\doik\\yolov8n.pt") # best.pt로 수정 필요
students = ["doik", "IU", "shokhrukh", "zabo"]
classes_info = {
    0: {"name": "doik", "color": (0, 0, 255)},
    1: {"name": "IU", "color": (255, 0, 0)},
    2: {"name": "shokhrukh", "color": (255, 255, 0)},
    3: {"name": "zabo", "color": (0, 0, 0)},
    "Unknown": {"name": "Unknown", "color": (0, 255, 0)}
}
confidence_threshold = 0.9  # YOLO 모델 신뢰도 임계값

# 각 사람의 눈 감김 상태와 하품 횟수 딕셔너리 - 출력 대충 이렇게
detection_status = {name: {"flag": 0, "status": "Focusing", "yawn_count": 0} for name in students}
detection_status["Unknown"] = {"flag": 0, "status": "Focusing", "yawn_count": 0}

last_update_time = time.time()  # 마지막 상태 업데이트 시간을 기록

def use_result(results, frame):
    if results and results[0]:
        bboxes = np.array(results[0].boxes.xyxy.cpu(), dtype="int")
        classes = np.array(results[0].boxes.cls.cpu(), dtype="int")
        scores = np.array(results[0].boxes.conf.cpu())
        pred_box = zip(classes, bboxes, scores)
        
        detected_classes = set()
        for cls, bbox, score in pred_box:
            if score < confidence_threshold:
                class_info = classes_info["Unknown"]
                cls_name = "Unknown"
            else:
                detected_classes.add(cls)
                class_info = classes_info.get(cls, classes_info["Unknown"])
                cls_name = class_info["name"]
            (x, y, x2, y2) = bbox
            color = class_info["color"]
            cv2.rectangle(frame, (x, y), (x2, y2), color, 2)
            label = f"{class_info['name']}: {score:.2f}"
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        return detected_classes

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 프레임 크기 조정 및 그레이스케일 변환
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    subjects = detect(gray, 0)

    # YOLO 모델을 통해 얼굴 감지
    results = model(frame)
    detected_classes = use_result(results, frame)
    
    for subject in subjects:
        shape = predict(gray, subject)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        # 하품 감지
        distance = lip_distance(shape)
        lip = shape[48:60]
        cv2.drawContours(frame, [lip], -1, (0, 255, 0), 1)

        if ear < thresh:  # 눈을 감은 경우
            for cls in detected_classes:
                cls_name = classes_info.get(cls, {"name": "Unknown"})["name"]
                detection_status[cls_name]["flag"] += 1
                if detection_status[cls_name]["flag"] >= frame_check:
                    detection_status[cls_name]["status"] = "Sleeping"
        else:  # 눈을 뜬 경우
            for cls in detected_classes:
                cls_name = classes_info.get(cls, {"name": "Unknown"})["name"]
                detection_status[cls_name]["flag"] = 0
                detection_status[cls_name]["status"] = "Focusing"

        if distance > yawn_thresh:  # 하품을 한 경우
            for cls in detected_classes:
                cls_name = classes_info.get(cls, {"name": "Unknown"})["name"]
                detection_status[cls_name]["yawn_count"] += 1

    current_time = time.time()
    if current_time - last_update_time >= 3:  # 3초마다 상태 출력 - 일단 이렇게 출력
        status_list = [f"{name}: {info['status']} (yawn: {info['yawn_count']})" for name, info in detection_status.items()]
        print(status_list)
        last_update_time = current_time

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):  # 'q' 키를 누르면 종료
        break

cap.release()
cv2.destroyAllWindows()
