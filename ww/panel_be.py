import cv2

# RTMP stream URL
rtmp_url = 'rtmp://122.200.18.78/live/cam2'

# Create a VideoCapture object
cap = cv2.VideoCapture(rtmp_url)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Unable to open RTMP stream.")
    exit()

# Set the resolution to 640x480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Loop to continuously read frames from the RTMP stream
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if the frame was successfully captured
    if not ret:
        print("Error: Unable to capture frame.")
        break

    # Display the frame
    cv2.imshow('RTMP Stream', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
