# import module
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

if __name__ == "__main__":
    # Load image instead of using the camera
    image_path = "tcc/Imagens/detected_faces/grande_filtro/2024-06-09_12-38-58.png"  # Certifique-se de que o caminho para a imagem está correto
    # image_path = '/tcc/Imagens/detected_faces/verdadeiros/grande_filtro/2024-06-09_12-38-37.png'
    # image_path= "tcc/Imagens/2024-06-07_14-31-38.png"
    # image_path = "tcc/Imagens/detected_faces/falsos/foto_tela_filtro/2024-06-09_16-22-52.png"
    image = cv2.imread(image_path)

    if image is not None:
        image = antispoofing_processing(image)

        x_start = int(image.shape[0]/2 - image.shape[0]/6)
        x_end = int(image.shape[0]/2 + image.shape[0]/6)
        y_start = int(image.shape[1]/2 - image.shape[1]/6)
        y_end = int(image.shape[1]/2 + image.shape[1]/6)
        rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        rotated = cv2.flip(rotated, 1)
        cv2.imshow("Frame", rotated)
        key = cv2.waitKey(0) & 0xFF

        if key == ord("q"):
            cv2.destroyAllWindows()
    else:
        print(f"Erro ao carregar a imagem: {image_path}")