### afbeelding inladen
### van de afbeelding de eerste pixel aanpassen (RGB)
### binaire waarde van eerste pixel
### lSB van een waarde in een pixel aanpassen
### LSB van alle waardes van alle pixels aanpassen
### tekst opvragen en converten naar ascii waardes
### ascii waardes omzetten in binaire getallen

import cv2
from PIL import Image
import matplotlib.pyplot as plt 

# print("Wat is de naam van de afbeelding waar je een geheime tekst in wilt stoppen? (met file extention)")
# filename = input()
print("Wat is de geheime tekst die je wilt verbergen in de afbeelding?")
secret_text = input()

for char in secret_text:
    char_bin = bin(ord(char)).replace("0b", "")
    for bit in char_bin:
        print(bit)

# img = cv2.imread(filename)
# height, width = img.shape[:2]

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

        
# n = 23
# print(bin(n))
# n = (n & ~1) | 1
# print(n)
# print(bin(n))


# print(r, g, b)

# r = (r & ~1) | 1
# g = (g & ~1) | 1
# b = (b & ~1) | 1
# print(r, g, b)


# newimg = cv2.imwrite("test.png", img)