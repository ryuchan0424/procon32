import numpy as np
import cv2
import random
import sys



def toku(index,cansame,text,ter,x_3_3,y_3_3):
 r=[[2,0],[2,1],[2,2],[1,2],[0,2],[0,1],[0,0],[1,0]]
 textm=["R","D","L","U"]
 idm=[[1,0],[0,1],[-1,0],[0,-1]]
 #0 1
 #3 2
 sta1=[0,1,2,3]
 #3 4 5 6 7 8 +3?
 sta2=[2,1,1,0,0,3,2]
 
 ox=1
 oy=1
 
 
 def narabi(ox,oy,n,index,text,ter,x_3_3,y_3_3):
  memo=index[ox,oy]
  index[ox,oy]=index[ox+idm[n][0],oy+idm[n][1]]#33
  index[ox+idm[n][0],oy+idm[n][1]]=memo

  memo=ter[x_3_3-1+ox,y_3_3-1+oy].copy()
  ter[x_3_3-1+ox,y_3_3-1+oy]=ter[x_3_3-1+ox+idm[n][0],y_3_3-1+oy+idm[n][1]].copy()
  ter[x_3_3-1+ox+idm[n][0],y_3_3-1+oy+idm[n][1]]=memo.copy()
  
  ox=ox+idm[n][0]
  oy=oy+idm[n][1]
  
  text=text+textm[n]
  return ox,oy,index,text,ter
 
 if index[1,1]!=0:#0を真ん中に持っていく
  m=-1
  for i in range(4):
   if index[r[i*2][0],r[i*2][1]]==0:
    ox=r[i*2][0]
    oy=r[i*2][1]
    i=i+1
    if i>=4:
     i=i-4
    ox,oy,index,text,ter=narabi(ox,oy,i,index,text,ter,x_3_3,y_3_3)
    break
  
  for i in range(4):
   if index[r[i*2+1][0],r[i*2+1][1]]==0:
    ox=r[i*2+1][0]
    oy=r[i*2+1][1]
    
    i=i+2
    if i>=4:
     i=i-4
    ox,oy,index,text,ter=narabi(ox,oy,i,index,text,ter,x_3_3,y_3_3)
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
    ox,oy,index,text,ter=narabi(ox,oy,n,index,text,ter,x_3_3,y_3_3)#1
   break 
 

 for i in range(4):#1を真ん中に持っていく
  if index[r[i*2+1][0],r[i*2+1][1]]==1:
   n=i
   ox,oy,index,text,ter=narabi(ox,oy,n,index,text,ter,x_3_3,y_3_3)#2
   break 

 for i in range(4):
  if index[r[i*2+1][0],r[i*2+1][1]]==0:
   for j in range(2*i+1):
    n=sta2[j+2*(3-i)]
    ox,oy,index,text,ter=narabi(ox,oy,n,index,text,ter,x_3_3,y_3_3)#3
   break
  
 for j in range(4):
  n=j+3
  if n>=4:
   n=n-4
  ox,oy,index,text,ter=narabi(ox,oy,n,index,text,ter,x_3_3,y_3_3)

 order=[8,7,2,3,4,5,6,7,8]

 for h in range(len(order)):
  g=order[h]##入れ替え記録
  if h>=2:
   for i in range(4):
    if cansame[g] and cansame[index[r[i*2+1][0],r[i*2+1][1]]] :
     ii=0
     for h1 in range(9):
      if order[2+h1]==index[r[i*2+1][0],r[i*2+1][1]]:
       ii=2+h1
       break
     memo=order[h]
     order[h]=order[ii]
     order[ii]=memo
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
     
     ox,oy,index,text,ter=narabi(ox,oy,n,index,text,ter,x_3_3,y_3_3)
    break
  
  for i in range(4):#1を真ん中に持っていく
   if index[r[i*2+1][0],r[i*2+1][1]]==g:
    n=i
 
    ox,oy,index,text,ter=narabi(ox,oy,n,index,text,ter,x_3_3,y_3_3)
    break

  for i in range(4):
   if index[r[i*2+1][0],r[i*2+1][1]]==0:
    for j in range(7-2*(3-i)):
     n=sta2[2*(3-i)+j]
     ox,oy,index,text,ter=narabi(ox,oy,n,index,text,ter,x_3_3,y_3_3)
    break
  if h>=2:
   cansame[g]=False
 print("---")
 for i2 in range(3):
  memo=""
  for i1 in range(3):
   memo=memo+str(index[i1,i2])+""
  print(memo)
 return ter,text

##################
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
    if index[i1,i2,0]==t1 and index[i1,i2,1]==t2:
     terx=i1
     tery=i2
     break
  x_3_3=ox
  y_3_3=oy
  while not(terx-1<=ox and ox<=terx+1 and tery-1<=oy and oy<=tery+1):
   idux=0
   if terx>ox:
    idux=1
   elif terx<ox:
    idux=-1
   x_3_3=ox+idux
   if x_3_3==0 or x_3_3==index.shape[0]-1:
    x_3_3=ox
    idux=0

   iduy=0
   if tery>oy:
    iduy=1
   elif tery<oy:
    iduy=-1
   y_3_3=oy+iduy
   if y_3_3==0 or y_3_3==index.shape[1]-1:
    y_3_3=oy
    idux=0

   ide=np.array([[3,4,5],[2,0,6],[1,8,7]])
   
   memo=ide[1,1]
   ide[1,1]=ide[1-idux,1-iduy]
   ide[1-idux,1-iduy]=memo
   
   can=[False,True,True,True,True,True,True,True,True]
   index,text=toku(ide,can,text,index,x_3_3,y_3_3)
     

   ox=x_3_3
   oy=y_3_3
  
  for i1 in range(index.shape[0]):
   for i2 in range(index.shape[1]):
    if index[i1,i2,0]==t1 and index[i1,i2,1]==t2:
     terx=i1
     tery=i2
     break

  print(ox,oy,terx,tery)
  #while not(terx==t1 and tery==t2):
  for ggggg in range(2):
   if terx-t1<ox-t1:
    x_3_3=ox
   else:
    x_3_3=terx
   
   if tery-t2<oy-t2:
    y_3_3=oy
   else:
    y_3_3=tery
   
   idux=0
   if terx>t1:
    idux=-1
   else:
    idux=1

   iduy=0
   if tery>t2:
    iduy=-1
   else:
    iduy=1

   ide=np.array([[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]])
   moto=np.array([[3,4,5],[2,0,6],[1,8,7]])
   nun=moto[idux+1,iduy+1]
   print()
   print(nun)
     
   
   can=[True,True,True,True,True,True,True,True,True]
   can[0]=False
   ide[ox-x_3_3,oy-y_3_3]=0
   can[nun]=False
   ide[terx-x_3_3,tery-y_3_3]=nun
   
   nex=0
   for i1 in range(3):
    for i2 in range(3):
     while nex<9 and not(can[nex]):
      nex=nex+1
     if (ide[i1,i2]==-1):
      ide[i1,i2]=nex
      nex=nex+1
   print("--")
   for i2 in range(3):
    memo=""
    for i1 in range(3):
     memo=memo+str(ide[i1,i2])+""
    print(memo)
   print(ox,oy,terx,tery,x_3_3,y_3_3,)
   index,text=toku(ide,can,text,index,x_3_3,y_3_3)
   

   ox=x_3_3
   oy=y_3_3
   
   for i1 in range(index.shape[0]):
    for i2 in range(index.shape[1]):
     if index[i1,i2,0]==t1 and index[i1,i2,1]==t2:
      terx=i1
      tery=i2
      break
   
   for i2 in range(index.shape[1]):
    memo=""
    for i1 in range(index.shape[0]):
     memo=memo+str(index[i1,i2,0])+","+str(index[i1,i2,1])+" "
    print(memo)


'''
for i in range(1):
 text=""
 print("==")
 index=np.random.permutation(np.array([[1,2,0],[4,5,6],[8,7,3]]))
 can=[False,False,False,False,True,True,True,True,True]
 for i2 in range(3):
  memo=""
  for i1 in range(3):
   memo=memo+str(index[i1,i2])+" "
  print(memo)
 print()
 index,text=toku(index.copy(),can,text,index.copy(),1,1)
 for i2 in range(3):
  memo=""
  for i1 in range(3):
   memo=memo+str(index[i1,i2])+" "
  print(memo)
'''