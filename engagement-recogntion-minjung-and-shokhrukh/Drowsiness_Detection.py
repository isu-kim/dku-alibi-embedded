"""
 Code by Kim Minjung and Shokhrukh Talatov
"""

from scipy.spatial import distance
from flask import Flask, request, jsonify
from imutils import face_utils
import imutils
import base64
import dlib
import cmake
import numpy as np
import cv2


app = Flask(__name__)

thresh = 0.25  # 눈을 감은 것을 판단하는 threshold 값
yawn_thresh = 20  # 하품을 판단하는 임계값
detect = dlib.get_frontal_face_detector()  # 얼굴 검출기 생성
predict = dlib.shape_predictor("./models/shape_predictor_68_face_landmarks.dat")
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
flag = 0  # 눈을 감은 프레임 수 초기화

detector = cv2.CascadeClassifier("./yawn_models/yawn_plus.xml")
predictor = dlib.shape_predictor("./yawn_models/shape_predictor_face_landmarks.dat")


def eye_aspect_ratio(eye):  # 눈의 특징적 비율을 계산하는 함수
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


def lip_distance(shape):  # 하품을 감지하는 함수
    top_lip = shape[50:53]
    top_lip = np.concatenate((top_lip, shape[61:64]))
    low_lip = shape[56:59]
    low_lip = np.concatenate((low_lip, shape[65:68]))
    top_mean = np.mean(top_lip, axis=0)
    low_mean = np.mean(low_lip, axis=0)
    distance = abs(top_mean[1] - low_mean[1])
    return distance


def base64_to_image(base64_string):
    decoded_data = base64.b64decode(base64_string)
    np_data = np.frombuffer(decoded_data, np.uint8)
    image = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

    return image


@app.route('/engagement', methods=['POST'])
def process_pixels():
    request_data = request.json

    pixels_b64 = request_data.get('pixels_b_64', '')
    frame = base64_to_image(pixels_b64)

    remote_ip = request.remote_addr
    print(f"Received pixels from {remote_ip}")

    detect_sleepiness(frame)
    detect_yawn(frame)

    return jsonify({'message': 'Received and processed pixels successfully'})


def detect_sleepiness(frame):
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 그레이스케일 이미지로 변환
    subjects = detect(gray, 0)  # 얼굴 검출

    for subject in subjects:  # 검출된 얼굴마다 반복
        shape = predict(gray, subject)  # 얼굴 랜드마크 예측
        shape = face_utils.shape_to_np(shape)  # NumPy 배열로 변환
		# 양쪽 눈 가로세로 비율
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0
        # 눈 모양 컨벡스 헐 그리기
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        if ear < thresh:  # 눈을 감은 경우
            print("sleeping")
        else:  # 눈을 뜬 경우
            print("focusing")


def detect_yawn(frame):
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 그레이스케일 이미지로 변환
    subjects = detect(gray, 0)  # 얼굴 검출

    for subject in subjects:  # 검출된 얼굴마다 반복
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

        if distance > yawn_thresh:  # 하품을 한 경우
            print("yawned!")


if __name__ == "__main__":
    app.run(debug=True)  # run api
