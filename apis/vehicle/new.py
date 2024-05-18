from ultralytics import YOLO
import cv2
import numpy as np
from sort.sort import *
from util import get_car, read_license_plate, write_csv

def process_video(yolo_coco_model_path, yolo_license_plate_model_path, video_path):
    results = {}
    mot_tracker = Sort()

    coco_model = YOLO(yolo_coco_model_path)
    license_plate_detector = YOLO(yolo_license_plate_model_path)

    cap = cv2.VideoCapture(video_path)
    vehicles = [2, 3, 5, 7]
    frame_nmr = -1
    ret = True

    while ret:
        frame_nmr += 1
        ret, frame = cap.read()
        if ret:
            results[frame_nmr] = {}
            
            detections = coco_model(frame)[0]
            detections_ = []
            for detection in detections.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = detection
                if int(class_id) in vehicles:
                    detections_.append([x1, y1, x2, y2, score])

            track_ids = mot_tracker.update(np.asarray(detections_))

            license_plates = license_plate_detector(frame)[0]
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate

                xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

                if car_id != -1:
                    license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]

                    license_plate_crop_gray = cv2.cvtColor(
                        license_plate_crop, cv2.COLOR_BGR2GRAY
                    )
                    _, license_plate_crop_thresh = cv2.threshold(
                        license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV
                    )

                    license_plate_text, license_plate_text_score = read_license_plate(
                        license_plate_crop_thresh
                    )

                    if license_plate_text is not None:
                        if license_plate_text=='RJ14CV0002':
                            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                            time.sleep(10)
                        results[frame_nmr][car_id] = {
                            "car": {"bbox": [xcar1, ycar1, xcar2, ycar2]},
                            "license_plate": {
                                "bbox": [x1, y1, x2, y2],
                                "text": license_plate_text,
                                "bbox_score": score,
                                "text_score": license_plate_text_score,
                            },
                        }

    write_csv(results, "D:/Rajasthan_Project/apis/vehicle/test.csv")

# Usage of the function
yolo_coco_model_path = "D:/Rajasthan_Project/apis/vehicle/yolov8n.pt"
yolo_license_plate_model_path = "D:/Rajasthan_Project/apis/vehicle/license_plate_detector.pt"
video_path = "rtsp://192.168.29.56:8080/h264_ulaw.sdp"

process_video(yolo_coco_model_path, yolo_license_plate_model_path, video_path)