"""
 Code by Kim Doik
"""
import grpc
import numpy as np
from ultralytics import YOLO
import cv2
import os
import base64
import threading

import alibi_pb2
import alibi_pb2_grpc

# load YOLO models, setup camera
model = YOLO("./runs/detect/train/weights/best.pt")
cap = cv2.VideoCapture(0)

channel = None
stub: alibi_pb2_grpc.ImageUploadServiceStub

# class name, colors
classes_info = {
    0: {"name": "doik", "color": (0, 0, 255)},  # "doik"에 대한 빨간색
    1: {"name": "IU", "color": (255, 0, 0)},    # "IU"에 대한 파란색
    2: {"name": "minjung", "color": (0, 255, 0)},  # "minjung"에 대한 초록색
    3: {"name": "rose", "color": (255, 255, 0)}, # "rose"에 대한 노란색
    4: {"name": "shokhrukh", "color": (255, 0, 255)}, # "shokhrukh"에 대한 마젠타색
    5: {"name": "yeji", "color": (0, 255, 255)}, # "yeji"에 대한 시안색
    6: {"name": "isu", "color": (128, 0, 128)},  # "isu"에 대한 보라색
    7: {"name": "zabo", "color": (0, 128, 128)}, # "zabo"에 대한 청록색
    8: {"name": "jisoo", "color": (128, 128, 0)} # "jisoo"에 대한 올리브색
}

# 신뢰도 임계값
confidence_threshold = 0.6

# 새로운 클래스에 대한 카운터 초기화
detection_counter = {i: 0 for i in range(len(classes_info))}

capture_path = "./captures"  # 이미지 저장 경로
os.makedirs(capture_path, exist_ok=True) 


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
            detection_counter[cls] += 1

            (x, y, x2, y2) = bbox
            # print(f"bounding box ({x}, {y}, {x2}, {y2}) has class {cls}, which is {class_info['name']}, confidence score: {score:.2f}")
            color = class_info["color"]
            cv2.rectangle(frame, (x, y), (x2, y2), color, 2)
            
            # 이름과 신뢰도 점수를 함께 표시
            label = f"{class_info['name']}: {score:.2f}"
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # 탐지된 고유한 클래스 수 출력
        # print(f"Number of detected classes: {len(detected_classes)}")
        
        # 특정 횟수에 도달했을 때 이미지 저장
        for cls, count in detection_counter.items():
            if True:
                # 바운딩 박스를 기준으로 이미지를 잘라내기
                for cls, bbox in zip(classes, bboxes):
                    if cls in detected_classes:
                        (x, y, x2, y2) = bbox
                        cropped_image = frame[y:y2, x:x2]
                        cropped_filename = f"cropped_class_{cls}_capture.jpg"  # 이미지 파일 이름
                        cropped_filepath = os.path.join(capture_path, cropped_filename)
                        cv2.imwrite(cropped_filepath, cropped_image)
                        print(f"Captured and saved cropped image for class {cls} at {cropped_filepath}")
                        send_thread = threading.Thread(target=send_image, args=(cropped_filepath, cls))
                        send_thread.start()

                # 카운터 초기화
                detection_counter[cls] = 0
        
        scale_percent = 60  # 원래 크기의 백분율
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        frame_s = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow("Img", frame_s)
    return


def send_image(cropped_filepath: str, cls: int):
    global stub

    class_info = classes_info.get(cls)

    with open(cropped_filepath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

    req = alibi_pb2.StudentFaceRequest(detected_name=class_info["name"], image_data_b64=str(encoded_string))
    responses = stub.UploadImage(iter([req]))  # Use iter() for streaming requests

    print("[gRPC] Uploaded image " + str(responses))


def main():
    """
    Main function
    :return: None
    """
    global channel
    global stub

    channel = grpc.insecure_channel("220.149.231.241:9090")
    stub = alibi_pb2_grpc.ImageUploadServiceStub(channel)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        use_result(results, frame)

        key = cv2.waitKey(100)
        if key == 27:  # ESC 키
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
