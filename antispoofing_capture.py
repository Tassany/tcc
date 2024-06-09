# import module
from datetime import datetime
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from ndvi.ndvi_processing import ndvi_calculate

max_mean = 0
min_mean = 255
# Saved frame count
count = 0
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
# allow the camera to warmup
time.sleep(0.1)

def is_attack(image):
    global max_mean, min_mean
    attack_threshold = 0
    # Split the channels
    _, _, r = cv2.split(image)
    
    ndvi = ndvi_calculate(image)

    x_start = int(r.shape[0]/2 - r.shape[0]/6)
    x_end = int(r.shape[0]/2 + r.shape[0]/6)
    y_start = int(r.shape[1]/2 - r.shape[1]/6)
    y_end = int(r.shape[1]/2 + r.shape[1]/6)

    mean = np.mean(ndvi[x_start:x_end, y_start:y_end])

    if mean > max_mean:
        max_mean = mean
    if mean < min_mean:
        min_mean = mean

    print(f'mean: {mean} | Attack: {mean < attack_threshold}')
    return mean < attack_threshold

def antispoofing_processing(image):
    if is_attack(image):
        print('Attack')
        return np.zeros(image.shape)
    else:
        print('Real')
        return image[:, :, 2]

# grab an image from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    image = antispoofing_processing(image)

    # show the frame
    x_start = int(image.shape[0]/2 - image.shape[0]/6)
    x_end = int(image.shape[0]/2 + image.shape[0]/6)
    y_start = int(image.shape[1]/2 - image.shape[1]/6)
    y_end = int(image.shape[1]/2 + image.shape[1]/6)
    rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    # mirror horizontally
    rotated = cv2.flip(rotated, 1)
    cv2.imshow("Frame", rotated)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    # elif key == ord("s"):
    #     cv2.imwrite(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png', image)
    #     print(f"Imagem salva: opencv{str(count)}.png")
    #     count += 1
