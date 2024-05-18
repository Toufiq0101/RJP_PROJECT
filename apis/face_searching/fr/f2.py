import cv2
import os
import numpy as np
import face_recognition

def face_recognition_on_video(reference_image_path, video_path):


    # Load the reference image and encode the face
    reference_image = cv2.imread(reference_image_path)
    reference_encoding = face_recognition.face_encodings(reference_image)[0]

    # Load the video
    video_capture = cv2.VideoCapture('rtsp://192.168.29.56:8080/h264_ulaw.sdp')

    while True:
        # Read the current frame
        ret, big_frame = video_capture.read()
        frame = cv2.resize(big_frame, (0, 0), fx=0.25, fy=0.25)


        # Find faces in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Iterate over the detected faces
        for face_location, face_encoding in zip(face_locations, face_encodings):
            # Compare the face encoding with the reference encoding
            match = face_recognition.compare_faces([reference_encoding], face_encoding)

            # If there is a match, draw a red rectangle around the face
            if match[0]:
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            else:
                # If there is no match, draw a green rectangle around the face
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow("test",frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close the windows
    video_capture.release()
    cv2.destroyAllWindows()
    cv2.destroyAllWindows()

# Example usage
reference_image_path = "D:/Rajasthan_Project/apis/face_searching/fr/known_people/Toufiq.png"
video_path = 'rtsp://192.168.29.56:8080/h264_ulaw.sdp'
face_recognition_on_video(reference_image_path, video_path)
