import numpy as np
import cv2
import random
import sys

kaizou=2

def rot(d,r):#回転計算関数
 c1=d+r
 if c1>=4:
  c1=c1-4
 return c1

img = cv2.imread('problem.ppm', cv2.IMREAD_COLOR)

file=open('problem.ppm', 'rb')
memo=file.read()[0:32].decode(encoding='utf-8').split("\n")[1].split(" ")
print(memo)
file.close()

filet=open('problem.txt', 'r',encoding='utf-8').read()

y_wari=filet.split("\n")
x_wari=y_wari[0].split("\t")
data=x_wari[0].split(",")

index=np.zeros((len(x_wari),len(y_wari),len(data)), dtype='uint8')

y_wari=filet.split("\n")
for i2 in range(len(y_wari)):
 x_wari=y_wari[i2].split("\t")
 for i1 in range(len(x_wari)):
  data=x_wari[i1].split(",")
  for i3 in range(len(data)):
   index[i1,i2,i3]=int(data[i3])
print(index.shape)

text=""
for i2 in range(len(y_wari)):
 for i1 in range(len(x_wari)):
  text=text+str(index[i1,i2,2])

text=text+"\n1\n00\n2\nDU\n"
print(text)






