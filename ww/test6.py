import multiprocessing 
import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import colors, Annotator
import tensorflow as tf
def stream(camera_index, window_name):
    with tf.device("gpu:0"):
        cap = cv2.VideoCapture(camera_index)
        model = YOLO("yolov8n.pt")
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
        # print(h)
        center_point = (-10, 480)
        while True:
            ret, frame = cap.read()
            if ret:
                annotator = Annotator(frame, line_width=2)
                results = model.track(frame, persist=True)
                boxes = results[0].boxes.xyxy.cpu()
                if results[0].boxes.id is not None:
                    track_ids = results[0].boxes.id.int().cpu().tolist()
                    for box, track_id in zip(boxes, track_ids):
                        annotator.box_label(box, label=str(track_id), color=colors(int(track_id)))
                        annotator.visioneye(box, center_point)
                cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
if __name__ == "__main__":
    camera1_index = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
    camera2_index = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
    camera3_index = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
    camera4_index = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
    camera5_index = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
    camera6_index = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
    camera7_index = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
    camera8_index = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
    window1_name = 'Camera 1'
    window2_name = 'Camera 2'
    window3_name = 'Camera 3'
    window4_name = 'Camera 4'
    window5_name = 'Camera 5'
    window6_name = 'Camera 6'
    window7_name = 'Camera 7'
    window8_name = 'Camera 8'
    p1 = multiprocessing.Process(target=stream, args=(camera1_index,window1_name, )) 
    p2 = multiprocessing.Process(target=stream, args=(camera2_index,window2_name, )) 
    p3 = multiprocessing.Process(target=stream, args=(camera3_index,window3_name, )) 
    p4 = multiprocessing.Process(target=stream, args=(camera4_index,window4_name, )) 
    p5 = multiprocessing.Process(target=stream, args=(camera4_index,window5_name, )) 
    p6 = multiprocessing.Process(target=stream, args=(camera4_index,window6_name, )) 
    p7 = multiprocessing.Process(target=stream, args=(camera4_index,window7_name, )) 
    p8 = multiprocessing.Process(target=stream, args=(camera4_index,window8_name, )) 
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()
    p1.join()
    # print('The CPU usage is: ', psutil.cpu_percent())
    p2.join()
    # print('The CPU usage is: ', psutil.cpu_percent())
    p3.join()
    # print('The CPU usage is: ', psutil.cpu_percent())
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    p8.join()
    # print('The CPU usage is: ', psutil.cpu_percent())
    print("sucess")