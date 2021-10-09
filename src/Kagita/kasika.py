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

img = cv2.imread('./procon_main/problem.ppm', cv2.IMREAD_COLOR)

file=open('./procon_main/problem.ppm', 'rb')
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

n=int(memo[1])
m=int(memo[2])
im=np.zeros((n,m,int(img.shape[1]/n),int(img.shape[0]/m),3), dtype='uint8')#もとの画像データ
print(im.shape)
print(img.shape)
for nun1 in range(n):
 for nun2 in range(m):
  im[nun1,nun2]=img[nun2*int(img.shape[0]/m):nun2*int(img.shape[0]/m)+int(img.shape[0]/m),nun1*int(img.shape[1]/n):nun1*int(img.shape[1]/n)+int(img.shape[1]/n)].copy()#画像の分割

ful=np.zeros((int(img.shape[0]/kaizou),int(img.shape[1]/kaizou),3), dtype='uint8')
for nun1 in range(index.shape[0]):
 for nun2 in range(index.shape[1]):
  for p1 in range(int(img.shape[1]/n/kaizou)):
   for p2 in range(int(img.shape[0]/m/kaizou)):
    x=index[nun1,nun2,0]
    y=index[nun1,nun2,1]
    r=index[nun1,nun2,2]
    if r==0:#回転なし
     ful[(nun2)*int(img.shape[1]/n/kaizou)+p2,(nun1)*int(img.shape[0]/m/kaizou)+p1]=im[x,y,p2*kaizou,p1*kaizou].copy()
    elif r==1:#右１周り
     ful[(nun2)*int(img.shape[1]/n/kaizou)+p2,(nun1)*int(img.shape[0]/m/kaizou)+p1]=im[x,y,int(img.shape[1]/n)-1-p1*kaizou,p2*kaizou].copy()
    elif r==2:#右２周り
     ful[(nun2)*int(img.shape[1]/n/kaizou)+p2,(nun1)*int(img.shape[0]/m/kaizou)+p1]=im[x,y,int(img.shape[0]/m)-1-p2*kaizou,int(img.shape[1]/n)-1-p1*kaizou].copy()
    elif r==3:#右３周り
     ful[(nun2)*int(img.shape[1]/n/kaizou)+p2,(nun1)*int(img.shape[0]/m/kaizou)+p1]=im[x,y,p1*kaizou,int(img.shape[0]/m)-1-p2*kaizou].copy()
cv2.imshow('fimage', ful)
cv2.waitKey(0)







