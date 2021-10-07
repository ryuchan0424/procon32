import numpy as np
import cv2
import random
import sys
#img = cv2.imread('fuck image3.png', cv2.IMREAD_COLOR)
img = cv2.imread('problem.ppm', cv2.IMREAD_COLOR)

chimg=img

file=open('problem.ppm', 'rb')
memo=file.read()[0:32].decode(encoding='utf-8').split("\n")[1].split(" ")
print(memo)
file.close()
print(img.shape)
print(img.shape[0]/int(memo[2]))