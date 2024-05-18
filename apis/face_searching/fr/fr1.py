import face_recognition
import cv2
import numpy as np
import random

def srch_face(imgs: list, cam: str):
    found = ""
    video_capture = cv2.VideoCapture(cam)

    # sagar_image = face_recognition.load_image_file('D:/Rajasthan_Project/apis/face_searching/fr/known_people/Sagar_Shukla.jpg')
    # sagar_face_encoding = face_recognition.face_encodings(sagar_image)[0]

    # chandresh_image = face_recognition.load_image_file('D:/Rajasthan_Project/apis/face_searching/fr/known_people/Chandresh.jpg')
    # chandresh_face_encoding = face_recognition.face_encodings(chandresh_image)[0]

    # marcus_image = face_recognition.load_image_file('D:/Rajasthan_Project/apis/face_searching/fr/known_people/Marcus_Michael.jpg')
    # marcus_face_encoding = face_recognition.face_encodings(marcus_image)[0]

    # toufiq_image = face_recognition.load_image_file('D:/Rajasthan_Project/apis/face_searching/fr/known_people/Toufiq.png')
    # toufiq_face_encoding = face_recognition.face_encodings(toufiq_image)[0]

    known_face_encodings = []
    known_face_names = []

    for img in imgs:
        face_image = face_recognition.load_image_file(img)
        face_encoding = face_recognition.face_encodings(face_image)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append("suspects")

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations
        )

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding
            )
            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding
            )
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                found += "1"
                name = known_face_names[best_match_index]

            face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(
                frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
            )
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(
                frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1
            )
        cv2.imshow("Video", frame)
        if found == "111111111":
            name = f"D:/Rajasthan_Project/apis/output/{random.randrange(1,1000)}.jpg"
            cv2.imwrite(name,frame)
            return True, name

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    video_capture.release()
    cv2.destroyAllWindows()


# face_img_list = [
#     "D:/Rajasthan_Project/apis/face_searching/fr/known_people/Sagar_Shukla.jpg",
#     "D:/Rajasthan_Project/apis/face_searching/fr/known_people/Chandresh.jpg",
#     "D:/Rajasthan_Project/apis/face_searching/fr/known_people/Marcus_Michael.jpg",
#     "D:/Rajasthan_Project/apis/face_searching/fr/known_people/Toufiq.png",
# ]
# print(srch_face(face_img_list,'rtsp://192.168.29.56:8080/h264_ulaw.sdp'))

