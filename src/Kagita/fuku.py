import numpy as np
import cv2
import random
import sys


#手動でいじるところ######################################################################################
sx=0
sy=0
#クルッと回したあとにx方向にいくつ移動？y方向にいくつ移動？
########負解像度　大きくなるほど粗くなる
kaitensuu=0
kaizou=2
bairitu=1
########################################################################################

#img = cv2.imread('fuck image3.png', cv2.IMREAD_COLOR)
img = cv2.imread('problem.ppm', cv2.IMREAD_COLOR)

chimg=img

file=open('problem.ppm', 'rb')
memo=file.read()[0:32].decode(encoding='utf-8').split("\n")[1].split(" ")
print(memo)
file.close()


m=int(memo[2])
n=int(memo[1])
im=np.zeros((m,n,int(img.shape[0]/m), int(img.shape[1]/n),3), dtype='uint8')#もとの画像データ

for nun1 in range(m):
   for nun2 in range(n):
      im[nun1,nun2]=img[nun1*int(img.shape[0]/m):nun1*int(img.shape[0]/m)+int(img.shape[0]/m),nun2*int(img.shape[1]/n):nun2*int(img.shape[1]/n)+int(img.shape[1]/n)].copy()#画像の分割


#0右　1下　2左 3上(時計回りに読み上げる)
#縦　横　回転　位置　色
boundary_right=np.zeros((m,n,4,int(img.shape[0]/m),3), dtype='uint8')#比べる用の変数の準備

for nun1 in range(m):
   for nun2 in range(n):
    for q in range(4):
     for p in range(int(img.shape[0]/m)):
      if q==0:
       boundary_right[nun1,nun2,q,p]=im[nun1,nun2,p,int(img.shape[0]/m)-1].copy()
      elif q==1:
       boundary_right[nun1,nun2,q,p]=im[nun1,nun2,int(img.shape[0]/m)-1,int(img.shape[1]/n)-1-p].copy()
      elif q==2:
       boundary_right[nun1,nun2,q,p]=im[nun1,nun2,int(img.shape[0]/m)-1-p,0].copy()
      elif q==3:
       boundary_right[nun1,nun2,q,p]=im[nun1,nun2,0,p].copy()

def rot(d,r):#多分左回転
 c1=d+r
 if c1>=4:
  c1=c1-4
 return c1
def get_fragment(q1,u,v,ran):#そのピースの指定した方向にran番会いそうなピースを返す
 kan=150##計算のがんばり具合（大きいと遅くなるが、ちゃんと計算してくれる）
 distan=5
 sabo=1
 atu=2
 sums=[kan]*(ran)#0が一番近い（小さい)
 datas=[[0,0,4] for j in range(ran)]

 for nun1 in range(m):
  for nun2 in range(n):
   for q2 in range(4):
    sum=0
    if nun1==u and nun2==v and q2==q1:
     sum=kan
    for p1 in range(int(img.shape[0]/m/sabo)-(atu-1)):
     for p2 in range(3):
      #色の差
      rr=(float(boundary_right[nun1,nun2,q2,(p1)*sabo,p2])-float(boundary_right[u,v,q1,int(img.shape[0]/m)-1-(p1)*sabo,p2]))
      rr=rr*rr/255
      for zzz in range(atu):
       memo=(float(boundary_right[nun1,nun2,q2,(p1)*sabo,p2])-float(boundary_right[u,v,q1,int(img.shape[0]/m)-1-(p1+zzz)*sabo,p2]))
       memo=memo*memo/255
       if memo<rr:
        rr=memo
      if sum<kan-rr*rr:
       sum=sum+rr*rr
      else:
       sum=kan
       break
     if sum==kan:
      break
    #print(sum)
    if sum<kan:
     flag=True
     for i in range(len(sums)):
      if sum<sums[i]:
       for q in range(len(sums)-1-i):
        datas[-q][0]=datas[-(q+1)][0]
        datas[-q][1]=datas[-(q+1)][1]
        datas[-q][2]=datas[-(q+1)][2]
        sums[-q]=sums[-(q+1)]
       datas[i][0]=nun1
       datas[i][1]=nun2
       datas[i][2]=q2
       sums[i]=sum
       flag=False
       break
 print(sums)
 return datas,sums

#m*n の 3*3 の3データ
fragment=np.zeros((m,n,3,3,3), dtype='uint8')
start_x=-1
start_y=-1
used=[[False]*fragment.shape[1] for g in range(fragment.shape[0])]

hani=1
Edge_distanc_rank=np.zeros((m,n,4,hani,3), dtype='uint8')
Edge_distanc_sums=np.zeros((m,n,4,hani))
for g1 in range(m):
 for h1 in range(n):
  for i1 in range(4):
   memo1,memo2=get_fragment(i1,g1,h1,hani)
   Edge_distanc_rank[g1,h1,i1]=np.array(memo1)
   Edge_distanc_sums[g1,h1,i1]=np.array(memo2)
   if Edge_distanc_rank[g1,h1,i1,0,2]==4:
    print(str(g1)+"*"+str(h1)+"*"+str(i1))
#6 7 0
#5 8 1
#4 3 2
kai=[[0,2],[1,2],[2,2],[2,1],[2,0],[1,0],[0,0],[0,1]]

for g in range(m):
 for h in range(n):
  for o in range(8):
   fragment[g,h,kai[o][0],kai[o][1],2]=4
  fragment[g,h,1,1,0]=g
  fragment[g,h,1,1,1]=h 
  fragment[g,h,1,1,2]=3
  for o in range(4):
   memon=Edge_distanc_rank[g,h,rot(o,rot(3-fragment[g,h,1,1,2],1)),0].copy()
   if memon[2]!=4:
    memo=Edge_distanc_rank[memon[0],memon[1],memon[2],0].copy()
    print(Edge_distanc_rank[g,h,rot(o,rot(3-fragment[g,h,1,1,2],1))])
    print(Edge_distanc_rank[memon[0],memon[1],memon[2]])
    memon[2]=rot(3-memon[2],3)
    memon[2]=rot(memon[2],o)   
   if memo[0]!=g or memo[1]!=h:
    memon[2]=4
   else:
    print(str(memon[0])+","+str(memon[1])+"|"+str(g)+","+str(h))
    
   fragment[g,h,kai[2*o+1][0],kai[2*o+1][1]]=memon.copy()

  for o in range(4):
   i1=o*2-1
   i2=o*2+1
   i3=o*2
   
   r1=o
   r2=o+1+2
   if r2>=4:
    r2=r2-4
   memo1=Edge_distanc_rank[fragment[g,h,kai[i1][0],kai[i1][1],0],fragment[g,h,kai[i1][0],kai[i1][1],1],rot(r1,rot(3-fragment[g,h,kai[i1][0],kai[i1][1],2],1)),0].copy()
   if memo1[2]!=4:
    memo=Edge_distanc_rank[memo1[0],memo1[1],memo1[2],0].copy()
    memo1[2]=rot(3-memo1[2],3)
    memo1[2]=rot(memo1[2],r1)
   if fragment[g,h,kai[i1][0],kai[i1][1],2]==4 or (memo[0]!=fragment[g,h,kai[i1][0],kai[i1][1],0] or memo[1]!=fragment[g,h,kai[i1][0],kai[i1][1],1]):
    memo1[2]=4

   memo2=Edge_distanc_rank[fragment[g,h,kai[i2][0],kai[i2][1],0],fragment[g,h,kai[i2][0],kai[i2][1],1],rot(r2,rot(3-fragment[g,h,kai[i2][0],kai[i2][1],2],1)),0].copy()
   if memo2[2]!=4:   
    memo=Edge_distanc_rank[memo2[0],memo2[1],memo2[2],0].copy()
    memo2[2]=rot(3-memo2[2],3)
    memo2[2]=rot(memo2[2],r2)
   if fragment[g,h,kai[i2][0],kai[i2][1],2]==4 or (memo[0]!=fragment[g,h,kai[i2][0],kai[i2][1],0] or memo[1]!=fragment[g,h,kai[i2][0],kai[i2][1],1]):
    memo2[2]=4

   if memo1[0]==memo2[0] and memo1[1]==memo2[1] and memo1[2]==memo2[2] and (memo1[2]!=4 and memo2[2]!=4):
    fragment[g,h,kai[i3][0],kai[i3][1]]=memo2.copy()
    print(str(g)+"*"+str(h))
    
for g in range(m):
 for h in range(n):
  fla=True
  for o in range(4):
   if fragment[g,h,kai[o*2][0],kai[o*2][1],2]==4 and fragment[g,h,kai[o*2-2][0],kai[o*2-2][1],2]==4:
    fragment[g,h,kai[o*2][0],kai[o*2-1][1],2]=4
    fla=False
  if fla and start_x==-1:
   start_x=g
   start_y=h

fulset=[[np.zeros((3), dtype='uint8')]]#比べる用の変数の準備
yoyaku=[[start_x,start_y,0,0,kaitensuu]]##ここでも一応回転はいじれる
used=np.full((fragment.shape[0], fragment.shape[1]), 0)
used[start_x,start_y]=1

while len(yoyaku)>=1:
#for qq in range(9):
 fulset[yoyaku[0][2]][yoyaku[0][3]]=fragment[yoyaku[0][0],yoyaku[0][1],1,1].copy()
 memoa=fulset[yoyaku[0][2]][yoyaku[0][3]][2]
 fulset[yoyaku[0][2]][yoyaku[0][3]][2]=rot(fulset[yoyaku[0][2]][yoyaku[0][3]][2],yoyaku[0][4])

 if yoyaku[0][2]==0:
  fulset.insert(0,[np.array([0,0,4], dtype='uint8') for b in range(len(fulset[yoyaku[0][2]]))])
  for y in range(len(yoyaku)):
   yoyaku[y][2]=yoyaku[y][2]+1
  
 if yoyaku[0][3]==0:
  for b in range(len(fulset)):
   fulset[b].insert(0,np.array([0,0,4], dtype='uint8'))
  for y in range(len(yoyaku)):
   yoyaku[y][3]=yoyaku[y][3]+1

 if yoyaku[0][2]==len(fulset)-1:
  fulset.append([np.array([0,0,4], dtype='uint8') for b in range(len(fulset[yoyaku[0][2]]))])
  
 if yoyaku[0][3]==len(fulset[yoyaku[0][2]])-1:
  for b in range(len(fulset)):
   fulset[b].append(np.array([0,0,4], dtype='uint8'))

 for o in range(8):
  p=o+yoyaku[0][4]*2
  if p >= 8:
   p=p-8

  i1=yoyaku[0][2]+kai[p][0]-1
  i2=yoyaku[0][3]+kai[p][1]-1
  if not(used[fragment[yoyaku[0][0],yoyaku[0][1],kai[o][0],kai[o][1],0],fragment[yoyaku[0][0],yoyaku[0][1],kai[o][0],kai[o][1],1]]>=1):
   u=fragment[yoyaku[0][0],yoyaku[0][1],kai[o][0],kai[o][1],0]
   v=fragment[yoyaku[0][0],yoyaku[0][1],kai[o][0],kai[o][1],1]
   if fulset[i1][i2][2]==4 and fragment[yoyaku[0][0],yoyaku[0][1],kai[o][0],kai[o][1],2]!=4:
    yoyaku.append([0,0,0,0,4])
    yoyaku[-1][0]=u
    yoyaku[-1][1]=v
    
    yoyaku[-1][2]=i1
    yoyaku[-1][3]=i2

    yoyaku[-1][4]=rot(fragment[yoyaku[0][0],yoyaku[0][1],kai[o][0],kai[o][1],2],rot(yoyaku[0][4],rot(3-memoa,1)))
    used[u,v]=used[u,v]+1
 
 del yoyaku[0]



index=np.full((m*bairitu,n*bairitu,3),np.array([0,0,4], dtype='uint8'))
used=np.full((fragment.shape[0], fragment.shape[1]), 0)

for mm in range(index.shape[0]):
 if mm+sy+1>=0 and len(fulset[0])>mm+sy+1:
  for mmm in range(index.shape[1]):
   if len(fulset)-1-(mmm-sx+1)>=0 and len(fulset)>len(fulset)-1-(mmm-sx+1):
    index[mm,mmm]=fulset[len(fulset)-1-(mmm-sx+1)][(mm+sy+1)].copy()
    if index[mm,mmm,2]!=4:
     index[mm,mmm,2]=rot(index[mm,mmm,2],1)
     used[index[mm,mmm,0],index[mm,mmm,1]]=2

#ダメ押し
yoyaku=[]
for ii in range(m):
 for jj in range(n):
  if 1<=used[index[ii,jj,0],index[ii,jj,1]]:
   if ii+1<m:
    if index[ii+1,jj,2]==4:
     yoyaku.append([index[ii,jj,0],index[ii,jj,1],ii,jj,rot(index[ii,jj,2],1)])
   if ii-1>=0:
    if index[ii-1,jj,2]==4:
     yoyaku.append([index[ii,jj,0],index[ii,jj,1],ii,jj,rot(index[ii,jj,2],1)])
   if jj+1<n:
    if index[ii,jj+1,2]==4:
     yoyaku.append([index[ii,jj,0],index[ii,jj,1],ii,jj,rot(index[ii,jj,2],1)])
   if jj-1>=0:
    if index[ii,jj-1,2]==4:
     yoyaku.append([index[ii,jj,0],index[ii,jj,1],ii,jj,rot(index[ii,jj,2],1)])
 
while len(yoyaku)>=1:
#for qq in range(1):
 index[yoyaku[0][2],yoyaku[0][3]]=fragment[yoyaku[0][0],yoyaku[0][1],1,1].copy()
 memoa=index[yoyaku[0][2],yoyaku[0][3],2]
 index[yoyaku[0][2],yoyaku[0][3],2]=rot(index[yoyaku[0][2],yoyaku[0][3],2],yoyaku[0][4])
 
 for o in range(8):
  p=o+yoyaku[0][4]*2
  if p >= 8:
   p=p-8
  
  i1=yoyaku[0][2]+kai[p][0]-1
  i2=yoyaku[0][3]+kai[p][1]-1
  if m>i1 and i1>=0 and n>i2 and i2>=0:
   if not(used[fragment[yoyaku[0][0],yoyaku[0][1],kai[o][0],kai[o][1],0],fragment[yoyaku[0][0],yoyaku[0][1],kai[o][0],kai[o][1],1]]>=1):
    u=fragment[yoyaku[0][0],yoyaku[0][1],kai[o][0],kai[o][1],0]
    v=fragment[yoyaku[0][0],yoyaku[0][1],kai[o][0],kai[o][1],1]
    
    if index[i1,i2,2]==4 and fragment[yoyaku[0][0],yoyaku[0][1],kai[o][0],kai[o][1],2]!=4:
     yoyaku.append([0,0,0,0,4])
     yoyaku[-1][0]=u
     yoyaku[-1][1]=v
     
     yoyaku[-1][2]=i1
     yoyaku[-1][3]=i2
     
     yoyaku[-1][4]=rot(fragment[yoyaku[0][0],yoyaku[0][1],kai[o][0],kai[o][1],2],rot(yoyaku[0][4],rot(3-memoa,1)))
     used[u,v]=used[u,v]+1
 
 del yoyaku[0]

for hh1 in range(m):
 for hh2 in range(n):
  if index[hh1,hh2,2]==4:
   flg=False
   for ii1 in range(used.shape[0]):
    if not(flg):
     for ii2 in range(used.shape[1]):
      if used[ii1,ii2]<1 and not(flg):
       used[ii1,ii2]=2
       index[hh1,hh2]=fragment[ii1,ii2,1,1].copy()
       flg=True


for tt1 in range(used.shape[0]):
 text=""
 for tt2 in range(used.shape[1]):
  text=text+" "+str(used[tt1,tt2])
 print(text)
  

cv2.imshow('fuck image', img)


ful=np.zeros((int(img.shape[0]/m/kaizou)*index.shape[0],int(img.shape[1]/n/kaizou)*index.shape[1],3), dtype='uint8')
for nun1 in range(index.shape[0]):
 for nun2 in range(index.shape[1]):
  for p1 in range(int(img.shape[0]/m/kaizou)):
   for p2 in range(int(img.shape[1]/n/kaizou)):
    x=index[nun1,nun2,0]
    y=index[nun1,nun2,1]
    r=index[nun1,nun2,2]
    if r==0:#回転なし
     ful[(nun1)*int(img.shape[0]/m/kaizou)+p1,(nun2)*int(img.shape[1]/n/kaizou)+p2]=im[x,y,p1*kaizou,p2*kaizou].copy()
    elif r==1:#右１周り
     ful[(nun1)*int(img.shape[0]/m/kaizou)+p1,(nun2)*int(img.shape[1]/n/kaizou)+p2]=im[x,y,int(img.shape[0]/m)-1-p2*kaizou,p1*kaizou].copy()
    elif r==2:#右２周り
     ful[(nun1)*int(img.shape[0]/m/kaizou)+p1,(nun2)*int(img.shape[1]/n/kaizou)+p2]=im[x,y,int(img.shape[1]/n)-1-p1*kaizou,int(img.shape[0]/m)-1-p2*kaizou].copy()
    elif r==3:#右３周り
     ful[(nun1)*int(img.shape[0]/m/kaizou)+p1,(nun2)*int(img.shape[1]/n/kaizou)+p2]=im[x,y,p2*kaizou,int(img.shape[1]/n)-1-p1*kaizou].copy()
cv2.imshow('fimage', ful)

cv2.waitKey(0)

savefile=open('problem.txt', 'w', encoding='UTF-8')
text=""

for i1 in range(index.shape[0]):
 for i2 in range(index.shape[1]):
  for i3 in [1,0,2]:
   text=text+str(index[i1,i2,i3])
   if i3<index.shape[2]-1:
    text=text+","
  if i2<index.shape[1]-1:
   text=text+"\t"
 if i1<index.shape[0]-1:
  text=text+"\n"
savefile.write(text)
savefile.close()







