import numpy as np
import cv2
import random
import sys



def toku(index,cansame,text):
 r=[[2,0],[2,1],[2,2],[1,2],[0,2],[0,1],[0,0],[1,0]]
 #index=np.array([[0,3,2],[4,7,6],[1,8,5]])
 #cansame=[False,False,False,False,False,False,False,True,True]
 
 for i in range(3):
  memo=""
  for j in range(3):
   memo=memo+str(index[j,i])+","
  print(memo)
 
 print()
 textm=["R","D","L","U"]
 idm=[[1,0],[0,1],[-1,0],[0,-1]]
 #0 1
 #3 2
 sta1=[0,1,2,3]
 #3 4 5 6 7 8 +3?
 sta2=[2,1,1,0,0,3,2]
 
 ox=1
 oy=1
 
 
 def narabi(ox,oy,n,index,text):
  memo=index[ox,oy]
  index[ox,oy]=index[ox+idm[n][0],oy+idm[n][1]]#33
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
    for i in range(3):
     memo=""
     for j in range(3):
      memo=memo+str(index[j,i])+","
     print(memo)
    print(ox,oy)
    break
  
  for i in range(4):
   if index[r[i*2+1][0],r[i*2+1][1]]==0:
    i=i+2
    if i>=4:
     i=i-4
    ox,oy,index,text=narabi(ox,oy,i,index,text)
    for i in range(3):
     memo=""
     for j in range(3):
      memo=memo+str(index[j,i])+","
     print(memo)
    print(ox,oy)
    break
 
 
 for i in range(4):#1を真ん中列に持っていく
  if index[r[i*2][0],r[i*2][1]]==1:
   for j in range(4):
    n=i+3
    if n>=4:
     n=n-4
    n=n+j
    if n>=4:
     n=n-4
    ox,oy,index,text=narabi(ox,oy,n,index,text)#1
    for i in range(3):
     memo=""
     for j in range(3):
      memo=memo+str(index[j,i])+","
     print(memo)
    print(ox,oy)
   break 
 

 for i in range(4):#1を真ん中に持っていく
  if index[r[i*2+1][0],r[i*2+1][1]]==1:
   n=i
   ox,oy,index,text=narabi(ox,oy,n,index,text)#2
   break 

 for i in range(4):
  if index[r[i*2+1][0],r[i*2+1][1]]==0:
   for j in range(2*i+1):
    n=sta2[j+2*(3-i)]
    ox,oy,index,text=narabi(ox,oy,n,index,text)#3
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
 return index,text

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


text=""

ox=0
oy=0
for i1 in range(index.shape[0]):
 for i2 in range(index.shape[1]):
  if index[i1,i2,0]==index.shape[0]-2 and index[i1,i2,1]==index.shape[1]-2:
   ox=i1
   oy=i2
   break
tas=[[1,1],[0,2],[0,1],[0,0],[1,0],[2,0],[2,1],[2,2],[1,2]]
#for t2 in range(index.shape[1]):
 #for t1 in range(index.shape[0]):

for t2 in range(1):
 for t1 in range(1):
  terx=0
  tery=0
  for i1 in range(index.shape[0]):
   for i2 in range(index.shape[1]):
    if index[t1,t2,0]==i1 and index[t1,t2,1]==i2:
     terx=i1
     tery=i2
     break
  x_3_3=ox
  y_3_3=oy
  while not(terx-1<=ox and ox<=terx+1 and tery-1<=oy and oy<=tery+1):
  #for ggggg in range(1):
   w1=0
   if ox>terx:
    w1=-1
   elif ox<terx:
    w1=1
   x_3_3=ox+w1
   w2=0
   if oy>tery:
    w2=-1
   elif ox<terx:
    w2=1
   y_3_3=oy+w2
   ide=np.array([[3,4,5],[2,0,6],[1,8,7]])
   memo=ide[1,1]
   ide[1,1]=ide[1+w1,1+w2]
   ide[1+w1,1+w2]=memo
   can=[False,True,True,True,True,True,True,True,True]
   ide,text=toku(ide,can,text)


   for j1 in range(3):
    for j2 in range(3):
     memo=index[x_3_3+j1-1,y_3_3+j2-1].copy()
     index[x_3_3+j1-1,y_3_3+j2-1]=index[x_3_3+tas[ide[j1,j2]][0]-1,y_3_3+tas[ide[j1,j2]][1]-1].copy()
     index[x_3_3+tas[ide[j1,j2]][0]-1,y_3_3+tas[ide[j1,j2]][1]-1]=memo.copy()
   ox=x_3_3
   oy=y_3_3
  
  print("a")
  print(x_3_3,y_3_3)
  while not(t1==terx and t2==tery):
   u1=0 #o
   w1=0 #ter
   if (t1-terx)*(t1-terx)>(t1-ox)*(t1-ox):
    x_3_3=ox
    w1=terx-ox
   else:
    x_3_3=terx
    u1=ox-terx
      
   u2=0 #o
   w2=0 #ter
   if (t2-tery)*(t2-tery)>(t2-oy)*(t2-oy):
    y_3_3=oy
    w2=tery-oy
   else:
    y_3_3=tery
    u2=oy-tery
   
   
   ide=np.array([[3,4,5],[2,0,6],[1,8,7]])
   m1=0
   if x_3_3>t1:
    m1=-1
   elif x_3_3<t1:
    m1=1
   m2=0
   if y_3_3>t2:
    m2=-1
   elif y_3_3<t2:
    m2=1
   nun=ide[m1+1,m2+1]

   memo=ide[1,1]
   ide[1,1]=ide[1+w1,1+w2]
   ide[1+w1,1+w2]=memo
   if ide[1,1]==nun:
    memo=ide[1,1]
    ide[1,1]=ide[1+u1,1+u2]
    ide[1+u1,1+u2]=memo
   else:
    memo=ide[1+m1,1+m2]
    ide[1+m1,1+m2]=ide[1+u1,1+u2]
    ide[1+u1,1+u2]=memo
   
   can=[False,True,True,True,True,True,True,True,True]
   can[nun]=False
   print(ide)
   ide,text=toku(ide,can,text)
   for j1 in range(3):##ここまで
    for j2 in range(3):
     memo=index[x_3_3+j1-2,y_3_3+j2-1].copy()
     index[x_3_3+j1-1,y_3_3+j2-1]=index[x_3_3+tas[ide[j1,j2]][0]-1,y_3_3+tas[ide[j1,j2]][1]-1].copy()
     index[x_3_3+tas[ide[j1,j2]][0]-1,y_3_3+tas[ide[j1,j2]][1]-1]=memo.copy()
   ox=x_3_3
   oy=y_3_3
'''
'''
for i2 in range(index.shape[1]):
 memo=""
 for i1 in range(index.shape[0]):
  memo=memo+str(index[i1,i2,0])+","+str(index[i1,i2,1])+" "
 print(memo)


'''
index=np.array([[1,2,3],[4,5,6],[0,7,8]])
can=[False,False,True,False,False,False,False,True,True]
index,text=toku(index,can,text)
'''




print(text)
print(len(text))