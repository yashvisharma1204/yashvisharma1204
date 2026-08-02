# scripts/prep_photo.py
import cv2
import numpy as np
from rembg import remove
from PIL import Image

# 1. Remove background
input_img = Image.open('image.png')
output_img = remove(input_img)
output_img.save('no_bg.png')

# 2. Apply CLAHE contrast adjustment on grayscale
img = cv2.imread('no_bg.png', cv2.IMREAD_UNCHANGED)
alpha = img[:, :, 3]
gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
equalized = clahe.apply(gray)

# Composite over white background
white_bg = np.ones_like(equalized) * 255
final_img = np.where(alpha > 0, equalized, white_bg)
cv2.imwrite('source-prepped.png', final_img)