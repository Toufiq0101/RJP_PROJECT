import cv2 
from ultralytics import YOLO 
import threading 
from ultralytics.utils.plotting import colors, Annotator
import subprocess

source_url_1 = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
source_url_2 = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
model1 = YOLO('yolov8n.pt')
model2 = YOLO('yolov8n.pt')

def run_tracker_in_thread(source_url, model, rtmp_url):    
    cap = cv2.VideoCapture(source_url)
    # Set the resolution to the maximum supported resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    print(w)
    print(h)
    command = ['ffmpeg',
               '-y',
               '-f', 'rawvideo',
               '-vcodec', 'rawvideo',
               '-pix_fmt', 'bgr24',
               '-s', "{}x{}".format(w, h),
               '-r', str(fps),
               '-i', '-',
               '-c:v', 'libx264',
               '-pix_fmt', 'yuv420p',
               '-preset', 'ultrafast',
               '-tune', 'zerolatency',  # Add this option to reduce latency
               '-f', 'flv',
               rtmp_url]
    print(command)
    center_point = (-10, h)
    p = subprocess.Popen(command, stdin=subprocess.PIPE)
    while True:
        ret, im0 = cap.read()
        if not ret:
            print("Video frame is empty or video processing has been successfully completed.")
            break
        # annotator = Annotator(im0, line_width=2)
        # results = model.track(im0, persist=True)
        # boxes = results[0].boxes.xyxy.cpu()
        # if results[0].boxes.id is not None:
        #     track_ids = results[0].boxes.id.int().cpu().tolist()
        #     for box, track_id in zip(boxes, track_ids):
        #         annotator.box_label(box, label=str(track_id), color=colors(int(track_id)))
        #         annotator.visioneye(box, center_point)
        # out.write(im0)
        p.stdin.write(im0.tobytes())

tracker_thread1 = threading.Thread(target=run_tracker_in_thread,
                                   args=(source_url_1, model1, 'rtmp://122.200.18.78/live/two'),
                                   daemon=True)

# tracker_thread2 = threading.Thread(target=run_tracker_in_thread,
#                                    args=(source_url_2, model2, 'rtmp://122.200.18.78/live/camthree'),
#                                    daemon=True)

tracker_thread1.start()
# tracker_thread2.start()
tracker_thread1.join()
# tracker_thread2.join()
cv2.destroyAllWindows()

