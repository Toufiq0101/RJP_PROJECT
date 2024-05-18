# python ./yolov5/detect.py --source rtsp://192.0.0.4:8080/h264_ulaw.sdp

import asyncio
import multiprocessing
import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import colors, Annotator
import tensorflow as tf
import os
from . import fr1
# import fr1
# from f2 import face_recognition_on_video

async def stream(camera_url, img_list, camera_id,return_dict):
    with tf.device("gpu:0"):
        ws = websocket.create_connection("ws://127.0.0.1:5669/fsr_ws")
        res = fr1.srch_face(img_list, camera_url)
        print(res)
        if res:
            found, img_name = res
            if found == True:
                response_data = {
                    "found":True,
                    "img_name":img_name
                }
                return_dict[f"{camera_id}"] = response_data
                ws.send(f"{response_data}")
                print("found_sucessfull===0000")

def stream_process_func(camera_url, img_list, camera_id,return_dict):
    asyncio.run(stream(camera_url, img_list, camera_id,return_dict))
def api_call(cam_list: list, img_list: list, cam_id: list):
    # camera1_url = "rtsp://192.168.29.56:8080/h264_ulaw.sdp"
    # camera2_url = "rtsp://192.168.29.150:8080/h264_ulaw.sdp"
    # camera3_url = "rtsp://192.168.29.56:8080/h264_ulaw.sdp"
    # camera4_url = "rtsp://192.168.29.56:8080/h264_ulaw.sdp"
    # print(cam_list)
    # print(cam_id)
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    p1 = multiprocessing.Process(target=stream_process_func, args=(cam_list[0],img_list, cam_id[0],return_dict))
    p2 = multiprocessing.Process(target=stream_process_func, args=(cam_list[1],img_list, cam_id[1],return_dict))
    p3 = multiprocessing.Process(target=stream_process_func, args=(cam_list[2],img_list, cam_id[2],return_dict))
    p4 = multiprocessing.Process(target=stream_process_func, args=(cam_list[3],img_list, cam_id[3],return_dict))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    return return_dict


if __name__ == "__main__":
    camera1_url = [
        "rtsp://192.168.29.56:8080/h264_ulaw.sdp",
        "rtsp://192.168.29.150:8080/h264_ulaw.sdp",
        "rtsp://192.168.29.150:8080/h264_ulaw.sdp",
        "rtsp://192.168.29.150:8080/h264_ulaw.sdp",
    ]
    face_img_list = [
        # "D:/Rajasthan_Project/apis/face_searching/fr/known_people/Sagar_Shukla.jpg",
        # "D:/Rajasthan_Project/apis/face_searching/fr/known_people/Chandresh.jpg",
        # "D:/Rajasthan_Project/apis/face_searching/fr/known_people/Marcus_Michael.jpg",
        "D:/Rajasthan_Project/apis/face_searching/fr/known_people/Toufiq.png",
    ]
    cam_id_list = ["cam1","cam2","cam3",'cam4']
    api_call(cam_list=camera1_url, img_list=face_img_list, cam_id=cam_id_list)
