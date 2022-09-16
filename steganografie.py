### afbeelding inladen
### van de afbeelding de eerste pixel aanpassen (RGB)
### binaire waarde van eerste pixel
# lSB van een waarde in een pixel aanpassen
# LSB van alle waardes van alle pixels aanpassen
# tekst opvragen en converten naar ascii waardes
# ascii waardes omzetten in binaire getallen

import cv2
from PIL import Image
import matplotlib.pyplot as plt 

print("Wat is de naam van de afbeelding waar je een geheime tekst in wilt stoppen? (met file extention)")
filename = input()

img = cv2.imread(filename)
height, width = img.shape[:2]


print(f"{r, g, b}")

# for h in range(height):
#     for w in range(width):
        

(b, g, r) = img[0][0]
r = bin(r).replace("0b", "")
b = bin(b).replace("0b", "")
g = bin(g).replace("0b", "")
print(f"r={(r, g, b)}")


newimg = cv2.imwrite("test.jpg", img)

