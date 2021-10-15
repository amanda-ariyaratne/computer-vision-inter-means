import os
import math
import glob
import cv2
import numpy as np # numpy is only used to feed the final image to cv2.imwrite method

def convert_to_grayscale(img):
    """
    Convert color image to grayscale
    G = 0.299R + 0.587G + 0.114B
    """
    height = len(img)
    width = len(img[0])

    grayscale_img = []

    for i in range(height):
        row = []
        for j in range(width):
            row.append((0.299 * img[i][j][0]) + (0.587 * img[i][j][1]) + (0.114 * img[i][j][2]))
        grayscale_img.append(row)

    return grayscale_img


# MAIN FUNCTION

base_path = os.getcwd()
ext_list = ['jpg', 'jpeg', 'png', 'bmp']
files = []
[files.extend(glob.glob(base_path + '/*.' + e)) for e in ext_list]

for file in files:
    img = cv2.imread(file)
    img = convert_to_grayscale(img)

    height = len(img)
    width = len(img[0])

    T = 0
    for i in range(height):
        T += sum(img[i])
    T = T / (height * width)

    converge_diff = 0.1
    iterations = 100
    it = 0
    old_T = T

    while (it == 0) or (abs(old_T - T) > converge_diff and it < iterations):
        old_T = T
        R1_sum = R2_sum = 0
        R1_count = R2_count = 0
        for i in range(height):
            for j in range(width):
                if img[i][j] < T:
                    R1_sum += img[i][j]
                    R1_count += 1
                else:
                    R2_sum += img[i][j]
                    R2_count += 1
        T = 0.5 * ((R1_sum/R1_count)+ (R2_sum/R2_count))

    segmented = [[0 if img[i][j] < T else 1 for j in range(width)] for i in range(height)]
    filename, ext = os.path.splitext(file)
    cv2.imwrite(filename + "_segmented" + ext, np.array(segmented))