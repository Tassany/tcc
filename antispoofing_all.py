import os
from datetime import datetime
import time
import cv2
import numpy as np
from ndvi.ndvi_processing import ndvi_calculate

max_mean = 0
min_mean = 255
# Saved frame count
count = 0
# allow the camera to warmup
time.sleep(0.1)

def is_attack(image):
    global max_mean, min_mean
    # attack_threshold = 0
    attack_threshold_min = 0.01
    attack_threshold_max = 0.09
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

    print(f'mean: {mean} | Attack: {mean < attack_threshold_min or mean > attack_threshold_max}')
    return mean < attack_threshold_min or mean > attack_threshold_max, mean

def antispoofing_processing(image):
    if is_attack(image):
        print('Attack')
        return np.zeros(image.shape)
    else:
        print('Real')
        return image[:, :, 2]

if __name__ == "__main__":
    # Path to the directory containing images
    # image_dir = "Imagens/detected_faces/grande_filtro/"
    image_dir = "Imagens/detected_faces/falsos/falso_papel_com_filtro-IPHONE/"
    # image_dir = "Imagens/detected_faces/falsos/foto_tela/"

    # Iterate over all files in the directory
    for filename in os.listdir(image_dir):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
            image_path = os.path.join(image_dir, filename)
            image = cv2.imread(image_path)

            if image is not None:
                print(f'Processing file: {filename}')
                image = antispoofing_processing(image)

                x_start = int(image.shape[0]/2 - image.shape[0]/6)
                x_end = int(image.shape[0]/2 + image.shape[0]/6)
                y_start = int(image.shape[1]/2 - image.shape[1]/6)
                y_end = int(image.shape[1]/2 + image.shape[1]/6)
                rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
                rotated = cv2.flip(rotated, 1)
                # cv2.imshow("Frame", rotated)
                key = cv2.waitKey(0) & 0xFF

                if key == ord("q"):
                    cv2.destroyAllWindows()
            else:
                print(f"Erro ao carregar a imagem: {image_path}")
