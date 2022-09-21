### afbeelding inladen
### van de afbeelding de eerste pixel aanpassen (RGB)
### binaire waarde van eerste pixel
### lSB van een waarde in een pixel aanpassen
### LSB van alle waardes van alle pixels aanpassen
### tekst opvragen en converten naar ascii waardes
### ascii waardes omzetten in binaire getallen
# eerste letter in eerste pixel zetten

# check max bits

# all bits
# w, h
# rbg/bgr

import cv2
from PIL import Image
import matplotlib.pyplot as plt 
import numpy as np
import math

#

# print("Wat is de naam van de afbeelding waar je een geheime tekst in wilt stoppen? (met file extention)")
# filename = input()
# print("Wat is de geheime tekst die je wilt verbergen in de afbeelding?")
secret_text = "az"

all_bits = np.array([])
for char in secret_text:
    char_bin = bin(ord(char)).replace("0b", "0")
    for bit in char_bin:
        all_bits = np.append(all_bits, 0)
pixels_needed = math.ceil(len(all_bits) / 3)

img = cv2.imread("f.png")
h, w = img.shape[:2]


current_pixel_w = 0
current_pixel_h = 0
current_color = 0
pixel_count = 0
current_color = 0


print(all_bits)
print(img[0])
for bit in all_bits:
    (b, g, r) = img[current_pixel_h][current_pixel_w]
    print(current_pixel_h, current_pixel_w, current_color, bit)
    print(f"OLD: {b, g, r}")
    if (current_color == 0):
        if (bit == "1"):
            b = b | 1
        else:
            b = b & ~1
        current_color = 1
    elif (current_color == 1):
        if (bit == "1"):
            g = g | 1
        else:
            g = g & ~1
        current_color = 2
    elif (current_color == 2):
        if (bit == "1"):
            r = r | 1
        else:
            r = r & ~1
        
        img[current_pixel_h][current_pixel_w] = (b, g, r)
        if (current_pixel_w != w):
            current_pixel_w = current_pixel_w + 1
        else:
            current_pixel_w = 0
            current_pixel_h = current_pixel_h + 1
        current_color = 0
        
    
    print(f"NEW: {b, g, r}\n")

# for h in range(10):
#     for w in range(10):
#         (b, g, r) = img[h][w]
#         # print(f"OLD {h, w}")
#         # print(r, g, b)
#         r = r | 1
#         g = g | 1
#         b = b | 1

#         img[h][w] = (b, g, r)
#         # print("NEW")
#         # print(r, g, b)
#         # print("\n")
print(img[0])
newimg = cv2.imwrite("testf.png", img)