import cv2
import matplotlib.pyplot as plt 
import numpy as np
import math
import binascii
from PIL import Image

def main():
    while True:
        print("\n1. Encode (tekst als bits in afbeelding verstoppen)\n2. Decode (bits extracten en de encodeerde tekst ophalen)")
        choice = input("Kies 1 of 2: ")
        if (choice == "1" or choice == "2"):
            break
        else:
            continue
        
    if (choice == "1"):
        print()
        encode()
    elif(choice == "2"):
        print()
        decode()

def encode():
    while True:
        print("Wat is de naam van de afbeelding waar je een geheime tekst in wilt stoppen? (met file extention)")
        filename = input("Bestandsnaam: ")
        print("\nWat is de geheime tekst die je wilt verbergen in de afbeelding?")
        secret_text = input("Geheime tekst: ")

        all_bits = np.array([])
        for char in secret_text:
            char_bin = bin(ord(char)).replace("0b", "0")
            for bit in char_bin:
                all_bits = np.append(all_bits, bit[0])

        for n in range(8):
            all_bits = np.append(all_bits, 1)
        pixels_needed = math.ceil(len(all_bits) / 3)

        img = cv2.imread(filename)
        h, w = img.shape[:2]

        current_pixel_w = 0
        current_pixel_h = 0
        current_color = 0

        if (pixels_needed < h * w):
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
                    img[current_pixel_h][current_pixel_w] = (b, g, r)
                    current_color = 1
                elif (current_color == 1):
                    if (bit == "1"):
                        g = g | 1
                    else:
                        g = g & ~1
                    img[current_pixel_h][current_pixel_w] = (b, g, r)
                    current_color = 2
                elif (current_color == 2):
                    if (bit == "1"):
                        r = r | 1
                    else:
                        r = r & ~1
                    img[current_pixel_h][current_pixel_w] = (b, g, r)
                    if (current_pixel_w != w - 1):
                        current_pixel_w = current_pixel_w + 1
                    else:
                        current_pixel_w = 0
                        current_pixel_h = current_pixel_h + 1
                    current_color = 0
                
                print(f"NEW: {b, g, r}\n")
            break
        else:
            print(f"\nDe geheime tekst is te groot voor deze afbeelding, kies een afbeeding van minstens {pixels_needed} pixels, of neem een kleinere tekst.")
            continue

    print(img)
    newimg = cv2.imwrite("encoded_" + filename, img)
    print(f"Gelukt! De encoded afbeelding zit in dezelfde map als encoded_{filename}")

def decode():
    print("Wat is de naam van de afbeelding waar je de tekst wilt extracten? (met file extention)")
    filename = input("Bestandsnaam: ")

    img = cv2.imread(filename)
    h, w = img.shape[:2]

    collected_bits = np.array([])
    collected_chunks = np.empty([0, 8])
    index=0
    for current_pixel_h in range(h):
        for current_pixel_w in range(w):
            (b, g, r) = img[current_pixel_h][current_pixel_w]
            colors = [b, g, r]
            for color in colors:
                lsb = color & 1
                collected_bits = np.append(collected_bits, lsb)
                if(np.array_equal(collected_bits[-8:], np.array([1, 1, 1, 1, 1, 1, 1, 1]))):
                    break
                elif(len(collected_bits) == 8 and not np.array_equal(collected_bits[-8:], np.array([1, 1, 1, 1, 1, 1, 1, 1]))):
                    collected_chunks = np.append(collected_chunks, [collected_bits], axis=0)
                    index = index+1
                    collected_bits = np.array([])
                elif(len(collected_bits <= 7)):
                    continue
            else:
                continue
            break
        else:
            continue
        break
    
    all_bits = ""
    # print(all_bits)
    for chunk in collected_chunks:
        for bit in chunk:
            all_bits = all_bits + str(bit).replace(".0", "")
    # characters = ''.join(chr(int(all_bits[i*8:i*8+8])) for i in range(len(all_bits)//8))
    # print(characters)
    # n = int(all_bits, len(collected_chunks))
    print(collected_chunks)
    all_bits=int(all_bits, 2)
    
    total_bytes = (all_bits.bit_length() +7) // 8
    bits_to_bytes = all_bits.to_bytes(total_bytes, "big")
    decoded_text = bits_to_bytes.decode('ascii')
    print(decoded_text)
main()