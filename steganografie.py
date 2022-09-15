import cv2
import string
import os

dict1 = {}
dict2 = {}

for i in range(256):
    dict1[chr(i)]=i
    dict2[i]=chr(i)

print(dict1)
print(dict2)

img = cv2.imread("test_img.jpg")

height = img.shape[0]
width = img.shape[1]
channels = img.shape[2]

print(f"Height: {height}, Width: {width}, Number of channels: {channels}")