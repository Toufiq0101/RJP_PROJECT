# python ./yolov5/detect.py --source rtsp://192.0.0.4:8080/h264_ulaw.sdp

import multiprocessing
import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import colors, Annotator
import tensorflow as tf
import os
def stream(camera_url, window_name, camera_id):
	with tf.device("gpu:0"):
		os.system(f'python ./yolov5/detect.py --source {camera_url} --cam_id {camera_id}')
if __name__ == "__main__":
    camera1_url = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
    camera2_url = 'rtsp://192.168.29.150:8080/h264_ulaw.sdp'
    camera3_url = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
    camera4_url = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
    camera5_url = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
    camera6_url = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
    camera7_url = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
    camera8_url = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
    cam_id1 = 'cam1'
    cam_id2 = 'cam2'
    cam_id3 = 'cam3'
    cam_id4 = 'cam4'
    cam_id5 = 'cam5'
    cam_id6 = 'cam6'
    cam_id7 = 'cam7'
    cam_id8 = 'cam8'
    window1_name = 'Camera 1'
    window2_name = 'Camera 2'
    window3_name = 'Camera 3'
    window4_name = 'Camera 4'
    window5_name = 'Camera 5'
    window6_name = 'Camera 6'
    window7_name = 'Camera 7'
    window8_name = 'Camera 8'
    p1 = multiprocessing.Process(target=stream, args=(camera1_url,window1_name,cam_id1))
    p2 = multiprocessing.Process(target=stream, args=(camera2_url,window2_name,cam_id2))
    p3 = multiprocessing.Process(target=stream, args=(camera3_url,window3_name,cam_id3))
    p4 = multiprocessing.Process(target=stream, args=(camera4_url,window4_name,cam_id4))
    # p5 = multiprocessing.Process(target=stream, args=(camera4_url,window5_name,cam_id5))
    # p6 = multiprocessing.Process(target=stream, args=(camera4_url,window6_name,cam_id6))
    # p7 = multiprocessing.Process(target=stream, args=(camera4_url,window7_name,cam_id7))
    # p8 = multiprocessing.Process(target=stream, args=(camera4_url,window8_name,cam_id8))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    # p5.start()
    # p6.start()
    # p7.start()
    # p8.start()


    p1.join()
    # print('The CPU usage is: ', psutil.cpu_percent())
    p2.join()
    # print('The CPU usage is: ', psutil.cpu_percent())
    p3.join()
    # print('The CPU usage is: ', psutil.cpu_percent())
    p4.join()
    # p5.join()
    # p6.join()
    # p7.join()
    # p8.join()
    # print('The CPU usage is: ', psutil.cpu_percent())
    print("sucess")