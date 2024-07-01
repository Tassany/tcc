import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
imput_images_folder = './imagens/detected_faces/falsos/foto_tela_filtro/'
output_images_folder = './imagens/simagens_processadas/'+imput_images_folder


# Get the name of all images in the folder
def get_filenames_from_folder(folder_path):
    return os.listdir(folder_path)

# Check if a folder exists and create it if not
def check_and_create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

# Calculate the NDVI of an image
def ndvi_calculate(image):
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom == 0] = 0.01
    ndvi = (r.astype(float) - b) / bottom  # THIS IS THE CHANGED LINE
    return ndvi

# Receive an image path and return the image as a numpy array
def process_image(image_path):
    image = cv2.imread(image_path)
    ndvi = ndvi_calculate(image)
    ndvi = ndvi * 255
    #make the image a range from 0 to 255 to blue to red
    ndvi = cv2.applyColorMap(ndvi.astype(np.uint8), cv2.COLORMAP_JET)
    ndvi = ndvi.astype('uint8')
    return ndvi

if __name__ == "__main__":
    images_to_process = get_filenames_from_folder(imput_images_folder)
    check_and_create_folder(output_images_folder)
    for image_name in images_to_process:
        image_path = imput_images_folder + image_name
        ndvi = process_image(image_path)
        output_image_path = output_images_folder + image_name
        cv2.imwrite(output_image_path, ndvi)
        print('Processada a imagem: ' + image_name)
