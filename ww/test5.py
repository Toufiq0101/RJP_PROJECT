import multiprocessing 
import cv2
import psutil

print('The CPU usage is: ', psutil.cpu_percent())
def stream(camera_index, window_name): 
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    while True:
        ret, frame = cap.read()
        if ret:
            # output_queue.put((window_name, frame))
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