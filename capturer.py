# import module
from datetime import datetime
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
# Saved frame count
count = 0
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
# allow the camera to warmup
time.sleep(0.1)
# grab an image from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    elif key == ord("s"):
        cv2.imwrite(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png', image)
        print(f"Imagem salva: opencv{str(count)}.png")
        count += 1
