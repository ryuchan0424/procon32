import numpy as np
import cv2
import random
import sys


r=[[2,0],[2,1],[2,2],[1,2],[0,2],[0,1],[0,0],[1,0]]
index=np.array([[0,3,2],[4,7,6],[1,8,5]])
mokuhyo=np.array([[3,2,1],[4,0,8],[5,6,7]])
cansame=[False,False,False,False,False,False,False,True,True]

for i in range(3):
 memo=""
 for j in range(3):
  memo=memo+str(index[j,i])+","
 print(memo)

print()
textm=["R","D","L","U"]
idm=[[1,0],[0,1],[-1,0],[0,-1]]
text=""
#0 1
#3 2
sta1=[0,1,2,3]
#3 4 5 6 7 8 +3?
sta2=[2,1,1,0,0,3,2]

ox=1
oy=1

def narabi(ox,oy,n,index,text):
 memo=index[ox,oy]
 index[ox,oy]=index[ox+idm[n][0],oy+idm[n][1]]
 index[ox+idm[n][0],oy+idm[n][1]]=memo
 
 ox=ox+idm[n][0]
 oy=oy+idm[n][1]
 
 text=text+textm[n]
 return ox,oy,index,text

if index[1,1]!=0:#0を真ん中に持っていく
 m=-1
 for i in range(4):
  if index[r[i*2][0],r[i*2][1]]==0:
   ox=r[i*2][0]
   oy=r[i*2][1]
   i=i+1
   if i>=4:
    i=i-4
   ox,oy,index,text=narabi(ox,oy,i,index,text)
   break

 for i in range(4):
  if index[r[i*2+1][0],r[i*2+1][1]]==0:
   i=i+2
   if i>=4:
    i=i-4
   ox,oy,index,text=narabi(ox,oy,i,index,text)
   break


for i in range(4):#1を真ん中列に持っていく
 if index[r[i*2][0],r[i*2][1]]==1:
  for j in range(4):
   n=j+3
   if n>=4:
    n=n-4
   n=n+i
   if n>=4:
    n=n-4
   ox,oy,index,text=narabi(ox,oy,n,index,text)
  break

for i in range(4):#1を真ん中に持っていく
 if index[r[i*2+1][0],r[i*2+1][1]]==1:
  n=i
  ox,oy,index,text=narabi(ox,oy,n,index,text)
  break

for i in range(4):
 if index[r[i*2+1][0],r[i*2+1][1]]==0:
  for j in range(7-2*(3-i)):
   n=sta2[2*(3-i)+j]
   ox,oy,index,text=narabi(ox,oy,n,index,text)
  break
 
for j in range(4):
 n=j+3
 if n>=4:
  n=n-4
 ox,oy,index,text=narabi(ox,oy,n,index,text)

order=[8,7,2,3,4,5,6,7,8]
buf=[0,1,2,3,4,5,6,7,8]

for h in range(len(order)):
 g=buf[order[h]]##入れ替え記録
 if h>=2:
  for i in range(4):
   if cansame[g] and cansame[index[r[i*2+1][0],r[i*2+1][1]]] :
    memo=buf[g]
    buf[g]=index[r[i*2+1][0],r[i*2+1][1]]
    buf[index[r[i*2+1][0],r[i*2+1][1]]]=memo
    g=index[r[i*2+1][0],r[i*2+1][1]]
 for i in range(4):#1を真ん中列に持っていく
  if index[r[i*2][0],r[i*2][1]]==g:
   for j in range(4):
    n=j+3
    if n>=4:
     n=n-4
    n=n+i
    if n>=4:
     n=n-4
    
    ox,oy,index,text=narabi(ox,oy,n,index,text)
   break
 
 for i in range(4):#1を真ん中に持っていく
  if index[r[i*2+1][0],r[i*2+1][1]]==g:
   n=i

   ox,oy,index,text=narabi(ox,oy,n,index,text)
   break

 for i in range(4):
  if index[r[i*2+1][0],r[i*2+1][1]]==0:
   for j in range(7-2*(3-i)):
    n=sta2[2*(3-i)+j]
    ox,oy,index,text=narabi(ox,oy,n,index,text)
   break
 if h>=2:
  print(g)
  print(buf)
  cansame[g]=False

for i in range(3):
 memo=""
 for j in range(3):
  memo=memo+str(index[j,i])+","
 print(memo)
print() 

print(ox)
print(oy)

print(text)