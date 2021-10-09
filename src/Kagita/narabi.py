import numpy as np
import cv2
import random
import sys

index=np.array([[2,3,0],[4,7,6],[3,8,1]])
mokuhyo=np.array([[3,2,1],[4,0,8],[5,6,7]])


r=[[2,1],[2,2],[1,2],[0,2],[0,1],[0,0],[1,0],[2,0]]
textm=["R\n","D\n","L\n","U\n"]
idm=[[1,0],[0,1],[-1,0],[0,-1]]
text=""
#0 1
#3 2
sta1=[0,1,2,3]
#3 4 5 6 7 8 +3?
sta2=[2,1,1,0,0,3,2]


ox=1
oy=1

if index[1,1]!=0:
 m=-1
 for i in range(4):
  if index[r[i*2+1][0],r[i*2+1][1]]==0:
   ox=r[i*2+1][0]
   oy=r[i*2+1][1]
   
   i=i+2
   if i>=4:
    i=i-4
   
   memo=index[ox,oy]
   index[ox,oy]=index[ox+idm[i][0],oy+idm[i][1]]
   index[ox+idm[i][0],oy+idm[i][1]]=memo
   
   ox=ox+idm[i][0]
   oy=oy+idm[i][1]
   
   text=text+textm[i]
   break
 for i in range(4):
  if index[r[i*2][0],r[i*2][1]]==0:
   i=i+2
   if i>=4:
    i=i-4
   
   memo=index[ox,oy]
   index[ox,oy]=index[ox+idm[i][0],oy+idm[i][1]]
   index[ox+idm[i][0],oy+idm[i][1]]=memo
   
   ox=ox+idm[i][0]
   oy=oy+idm[i][1]
   
   text=text+textm[i]
    


for g in range(4):
 if index[r[g*2+1][0],r[g*2+1][1]]==1:
  g=g+3
  for j in range(4):
   g=g+1
   if g>=4:
    g=g-4
   
   memo=index[ox,oy]
   index[ox,oy]=index[ox+idm[g][0],oy+idm[g][1]]
   index[ox+idm[g][0],oy+idm[g][1]]=memo
   
   ox=ox+idm[g][0]
   oy=oy+idm[g][1]
   
   text=text+textm[g]
    

'''

for g in range(4):
 if index[r[g*2][0],r[g*2][1]]==1:
  memo=index[ox,oy]
  index[ox,oy]=index[ox+idm[g][0],oy+idm[g][1]]
  index[ox+idm[g][0],oy+idm[g][1]]=memo
  
  ox=ox+idm[g][0]
  oy=oy+idm[g][1]
   
  text=text+textm[g]
  
  print()
  print(g)

  for j in range(7-(3-g)*2):
   n=sta2[j+(3-g)*2]
   print(n)
   memo=index[ox,oy]
   index[ox,oy]=index[ox+idm[n][0],oy+idm[n][1]]
   index[ox+idm[n][0],oy+idm[n][1]]=memo
   
   ox=ox+idm[n][0]
   oy=oy+idm[n][1]
   
   text=text+textm[n]


for i in range(1):
 for g in range(4):
  if index[r[g*2+1][0],r[g*2+1][1]]==i+1:
   g=g+3
   for j in range(4):
    g=g+1
    if g>=4:
     g=g-4
    
    memo=index[ox,oy]
    index[ox,oy]=index[ox+idm[g][0],oy+idm[g][1]]
    index[ox+idm[g][0],oy+idm[g][1]]=memo
    
    ox=ox+idm[g][0]
    oy=oy+idm[g][1]
    
    text=text+textm[g]
'''

for i in range(3):
 memo=""
 for j in range(3):
  memo=memo+str(index[i,j])+","
 print(memo)
 
print(ox)
print(oy)

print(text)
   
   
    