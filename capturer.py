

# import module
from datetime import datetime
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os

count = 0

face_detector = cv2.CascadeClassifier("/home/bezerril/antispoofing/haarcascade_frontalface_default.xml")

cv2.startWindowThread()

camera = PiCamera()
camera.resolution = (1280, 720)
raw_capture = PiRGBArray(camera, size=(1280, 720))

# Create a directory to store detected faces
output_directory = "detected_faces"
os.makedirs(output_directory, exist_ok=True)

time.sleep(0.1)  # Allow the camera to warm up

for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    im = frame.array

    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(grey, 1.1, 5)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0))

        # Generate a unique filename using timestamp for every saved image
        timestamp = int(time.time())
        filename = os.path.join(output_directory, f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png')
        cv2.imwrite(filename, im[y:y+h, x:x+w])  # Save only the detected face portion

    cv2.imshow("Camera", im)
    key = cv2.waitKey(1) & 0xFF

    # Clear the stream in preparation for the next frame
    raw_capture.truncate(0)

    if key == ord("q"):
        break
    elif key == ord("c"):
        filename = os.path.join(output_directory, f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png')
        cv2.imwrite(filename, im)
        print(f"Imagem salva: opencv{str(count)}.png")
        count += 1

cv2.destroyAllWindows()
    

    
