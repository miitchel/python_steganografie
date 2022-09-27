import cv2
import matplotlib.pyplot as plt 
import numpy as np
import math

def main():
    # gebruiker optie geven om te encoderen of decoderen
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

# functie voor het encoderen
def encode():
    while True:
        print("Wat is de naam van de afbeelding waar je een geheime tekst in wilt stoppen? (met file extention)")
        filename = input("Bestandsnaam: ")
        print("\nWat is de geheime tekst die je wilt verbergen in de afbeelding?")
        secret_text = input("Geheime tekst: ")

        # alle bits van de binary waarde van elke character in de geheime tekst in een array plaatsen
        all_bits = np.array([])
        for char in secret_text:
            char_bin = format(ord(char), '08b')
            for bit in char_bin:
                all_bits = np.append(all_bits, bit[0])

        # delimiter (111111111) toevoegen aan t einde van de array met bits van geheime tekst
        # en berekenen hoeveel pixels de afbeelding moet zijn
        for n in range(8):
            all_bits = np.append(all_bits, 1)
        pixels_needed = math.ceil(len(all_bits) / 3)

        # afbeelding inladen en hoogte en breedte ophalen
        img = cv2.imread(filename)
        h, w = img.shape[:2]

        current_pixel_w = 0
        current_pixel_h = 0
        current_color = 0

        # check of de afbeelding groot genoeg is
        if (pixels_needed < h * w):
            # langs elke bit gaan
            for bit in all_bits:
                # BGR kleuren ophalen (de module Open-CV werkt met BGR en Height Width)
                (b, g, r) = img[current_pixel_h][current_pixel_w]

                #kleur b
                if (current_color == 0):
                    if (bit == "1"):

                        # zet LSB (Least Significant Bit) van kleurwaarde om naar 1
                        b = b | 1
                    else:

                        # zet LSB van kleurwaarde om naar 0
                        b = b & ~1
                    # de kleur opslaan in de afbeelding
                    img[current_pixel_h][current_pixel_w] = (b, g, r)

                    # naar de volgende kleur
                    current_color = 1

                # kleur g
                elif (current_color == 1):
                    if (bit == "1"):
                        g = g | 1
                    else:
                        g = g & ~1
                    img[current_pixel_h][current_pixel_w] = (b, g, r)
                    current_color = 2

                # kleur r
                elif (current_color == 2):
                    if (bit == "1"):
                        r = r | 1
                    else:
                        r = r & ~1
                    img[current_pixel_h][current_pixel_w] = (b, g, r)

                    # checken of je aan t einde van de breedte zit, als dat zo is, start weer op w0 en ga omlaag in de hoogte
                    if (current_pixel_w == w - 1):
                        current_pixel_w = 0
                        current_pixel_h = current_pixel_h + 1
                    else:
                        current_pixel_w = current_pixel_w + 1

                    # start weer bij kleur b
                    current_color = 0
            break
        else:
            # als afbeelding te klein is voor de tekst
            print(f"\nDe geheime tekst is te groot voor deze afbeelding, kies een afbeeding van minstens {pixels_needed} pixels, of neem een kleinere tekst.")
            continue

    # nieuwe afbeelding opslaan als "encoded_filename.png"
    cv2.imwrite("encoded_" + filename, img)
    print(f"Gelukt! De encoded afbeelding zit in dezelfde map als encoded_{filename}")

# functie voor het decoderen
def decode():
    print("Wat is de naam van de afbeelding waar je de tekst wilt extracten? (met file extention)")
    filename = input("Bestandsnaam: ")

    # afbeelding inladen en hoogte en breedte ophalen
    img = cv2.imread(filename)
    h, w = img.shape[:2]

    # collected_bits array aanmaken en een 2D array collected_chunks, zullen chunks van 8 worden
    collected_bits = np.array([])
    collected_chunks = np.empty([0, 8])

    # langs elke pixel in de afbeelding gaan
    for current_pixel_h in range(h):
        for current_pixel_w in range(w):

            # BGR waarde ophalen
            (b, g, r) = img[current_pixel_h][current_pixel_w]
            colors = [b, g, r]

            # langs elke kleur gaan
            for color in colors:

                # LSB waarde ophalen van de kleur (de bit die dus is toegevoegd in de encode functie) en voeg die aan collected_bits array
                lsb = color & 1
                collected_bits = np.append(collected_bits, lsb)

                # checken of collected_bits vol met 11111111 zit en als dat zo is, stop dan met lezen van bits
                if(np.array_equal(collected_bits[-8:], np.array([1, 1, 1, 1, 1, 1, 1, 1]))):
                    break

                # als het vol zit met bits maar ze zijn niet 11111111, voeg ze dan toe als chunk bij de 2D collected_chunks array
                elif(len(collected_bits) == 8 and not np.array_equal(collected_bits[-8:], np.array([1, 1, 1, 1, 1, 1, 1, 1]))):
                    collected_chunks = np.append(collected_chunks, [collected_bits], axis=0)
                    collected_bits = np.array([])

                # als de collected_bits nog kleiner dan 8 is, ga dan gewoon verder
                elif(len(collected_bits <= 7)):
                    continue
            else:
                continue
            break
        else:
            continue
        break
    
    all_bits = ""

    # ga langs elke chunk en maak een hele string van bits en maak dat een int die kan starten met 0
    for chunk in collected_chunks:
        for bit in chunk:
            all_bits = all_bits + str(bit).replace(".0", "")
    all_bits=int(all_bits, 2)
    
    # het decoderen van all_bits door het alle bits om te zetten naar bytes en die bites om te zetten naar ASCII characters
    total_bytes = (all_bits.bit_length() +7) // 8
    bits_to_bytes = all_bits.to_bytes(total_bytes, "big")
    decoded_text = bits_to_bytes.decode('ascii')
    print(f" De geheime tekst is: {decoded_text}")
main()