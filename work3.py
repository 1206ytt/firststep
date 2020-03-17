# Script Name           : fileinfo.py
# Author                : pekki black(me)
# Created               : 2018
# Last Modified         :
# Version               : 1.1(in fact, same as the fir.)
# Modification          : 

# Description           : Get mp3 from wangyi but in need of other files to construct GUI

# -*- coding: utf-8 -*-

from urllib import*
import urllib.request as ur
from lxml import etree
import json
import pygame,sys
import PIL.Image
import PIL.ImageTk
import requests as rep
from io import BytesIO
from bs4 import BeautifulSoup
import os
import time
from pygame.locals import *
from tkinter import *
from tkinter import ttk
import shutil

#决定歌单网页(临时编辑过程使用)
url="http://music.163.com/api/playlist/detail?id=2520739691 "
song="City"
global b,point
b=0#是否正在播放
point=''


def collect():
    for i in treeview.get_children():
        treeview.delete(i)
    playlistid=playlistid_entry.get()
    url="http://music.163.com/api/playlist/detail?id="+playlistid
    
#制表头
    global headers
    headers=("User-Agent",
         """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/
            537.36 (KHTML, like Gecko) Chrome/
            64.0.3282.140 Safari/537.36 Edge/17.17134""")

#读取页面信息
    opener=ur.build_opener()
    opener.addheaders=[headers]
    data=opener.open(url).read()


#转码
    page = json.loads(data)
    #print(page)


#收集歌曲信息id，歌手，唱片，时长,热度

    global songs_iddic,songs_artists,songs_duration,songs_album,songs_albumpic
    global songs_pops,list_playCount,list_coverimage,song_artists,songlist1
    songs_iddic={}
    songs_artists={}
    songs_duration={}
    songs_album={}
    songs_albumpic={}
    songs_pops={}
    list_playCount=page.get('result').get('playCount')#歌单播放量
    list_coverimage=page.get('result').get('coverImgUrl')#歌单封面
    list_name=page.get('result').get('name')#歌单名
    list_des=page.get('result').get('description')#歌单描述
    song_artists=[[]*i for i in range(len(page.get('result').get("tracks")))]

    songlist1=[]

    for i in range(len(page.get('result').get("tracks"))):
    
        song_name=page.get('result').get("tracks")[i].get("name")
        song_id=page.get('result').get("tracks")[i].get("id")
        song_album=page.get('result').get("tracks")[i].get("album").get("name")
        song_albumpic=page.get('result').get("tracks")[i].get("album").get("blurPicUrl")
        song_duration=page.get('result').get("tracks")[i].get("duration")/1000
        song_long='%.2f'%(song_duration/60)+'min'#+'%.2f'%(song_duration%60)+'sec'
        song_pops=page.get('result').get("tracks")[i].get("score")

    
        for j in range(len(page.get('result').get("tracks")[i].get("artists"))):
            song_artists_temp=page.get('result').get("tracks")[i].get("artists")[j].get("name")
            song_artists[i].append(song_artists_temp)
        
        temp=song_artists[i]
        songlist1.append(song_name)
        songs_artists[song_name]=temp
        songs_iddic[song_name]=song_id
        songs_duration[song_name]=song_long
        songs_album[song_name]=song_album
        songs_albumpic[song_name]=song_albumpic
        songs_pops[song_name]=song_pops
    #print(songs_iddic,song_artists,songs_duration)
    #print(songs_album)
    #print(list_playCount)
    #print(songs_pops)

    global cover1,text1
    text1='歌单名:'+str(list_name)+'\n'+'歌单播放量'+str(list_playCount)
    popular['text']=text1
    cover1=PIL.ImageTk.PhotoImage(cover())
    albumpic['image']=cover1

    for i in range(len(songlist1)):
        x=songlist1[i]
        treeview.insert('',i,values=(str(i+1),x,songs_artists[x],songs_album[x],
                                     songs_duration[x],songs_pops[x]))
        treeview.update()


    


#下载音乐到本地(应补充自定义文件夹）
def download():

    global point,file,enter3,save
    
    save=str(point)
    
    top2=Toplevel()
    top2.title('下载')
    top2.geometry('400x150')
    label2=Label(top2,text='请输入保存路径:')
    label3=Label(top2,text='请输入名称（默认为歌曲名）:')
    label4=Label(top2,text='.mp3')
    entry2=Entry(top2,width=32)
    entry3=Entry(top2,)
    label2.place(x=10,y=30)
    entry2.place(x=120,y=30)
    label3.place(x=10,y=60)
    entry3.place(x=200,y=60)
    label4.place(x=350,y=60)#仅支持mp3


#下载的弹窗部分，点确认下载
    def ok():
        global save,enter3,file
        file=entry2.get()
        enter3=entry3.get()
        
        if enter3!='':
            save=enter3
        print(file)
        print(save)
        isExists=os.path.exists(str(file))
        if not isExists:
            os.makedirs(str(file))
        opener=ur.build_opener()
        opener.addheaders=[headers]
        urlmusic="http://music.163.com/song/media/outer/url?id="+str(songs_iddic[point])+".mp3"
        download=open(str(file)+'/'+str(save)+".mp3","wb")
        download.write(opener.open(urlmusic).read())
        download.close()
        top2.destroy()
#download(input())


    button2=Button(top2,text='确认',command=ok)
    button3=Button(top2,text='取消',command=top2.destroy)
    button2.place(x=100,y=100)
    button3.place(x=250,y=100)



#加载专辑封面图片
def getalbumpic():
    global point
    urlmusic="http://music.163.com/song/media/outer/url?id="+str(point)+".mp3"
    urlpic=songs_albumpic[point]
    response = rep.get(urlpic)
    image = PIL.Image.open(BytesIO(response.content))
    image1=image.resize((75,75))
    return image

def cover():
    urlpic=list_coverimage
    response = rep.get(urlpic)
    image = PIL.Image.open(BytesIO(response.content))
    image1=image.resize((75,75))
    return image1
    
#我曾经想用pygame把他完成
#pygame.init()
#pygame.mixer.init()
#screen=pygame.display.set_mode([1000,700])
#screen.fill((255,255,240))
#ico=pygame.image.load(r'C:\Users\赵旭\Desktop\新建文件夹\favicon.bmp').convert_alpha()
#pygame.display.set_icon(ico)
#pygame.display.set_caption('网易云音乐播放')
#pygame.time.delay(1000)
#gamefont1=pygame.font.SysFont('SimHei',24)
#gametext1=gamefont1.render("欢迎使用",True,(255,150,0))
#screen.blit(gametext1,(100,100))
#pygame.display.update()






#歌曲播放
def broadcast(song_name):
    global b,cover1
    isExists=os.path.exists('D:/Music_temp/')
    if not isExists:
        os.makedirs('D:/Music_temp/')
    urlmusic="http://music.163.com/song/media/outer/url?id="+str(songs_iddic[song_name])+".mp3"
    downloads=open("D:/Music_temp/"+str(song_name)+".mp3","wb")
    opener=ur.build_opener()
    opener.addheaders=[headers]
    cover1=PIL.ImageTk.PhotoImage(getalbumpic())
    albumpic['image']=cover1
    downloads.write(opener.open(urlmusic).read())
    downloads.close()
    pygame.mixer.init()
    pygame.time.delay(1000)
    pygame.mixer.music.load("D:/Music_temp/"+str(song_name)+".mp3")
    pygame.mixer.music.play(loops=-1)
    b=1
    #time.sleep()
    
#播放停止
def broadcast_shut():
    global point,b
    pygame.mixer.music.stop()
    b=0
    pygame.mixer.quit()
    #pygame.quit()
    #time.sleep()
    
    #os.remove("D:/Music_temp/"+str(point)+".mp3")
#broadcast(input())

#while True:
    #for event in pygame.event.get():
        #if event.type == QUIT:
            #pygame.quit()
            #sys.exit()
#窗口外观            
top1=Tk()

top1.iconbitmap(r'favicon.bmp')
top1.title('网易云音乐播放')
top1.geometry('300x500')
top1.columnconfigure(0,weight=1)
top1.rowconfigure(0,weight=1)

#设置暂停
def puase():
    global b,point
    if b==0:
        broadcast(point)
        b=1
    elif b==1:
        pygame.mixer.music.pause()
        b=2
    else:
        pygame.mixer.music.unpause()
        b=1
        
    
pausepic=PhotoImage(file='暂停状态图标.png')
pausebutton=Button(top1,bg='RoyalBlue',command=puase)
pausebutton['image']=pausepic
pausebutton.place(x=0,y=400)
#搜索框
frame1=Frame(top1,bg='red',height=40,width=300)
frame1.place(x=0,y=0)

var1=StringVar()
playlistid_label=Label(frame1,bg='red',text='请键入歌单id:',height=1,width=10)
playlistid_entry=Entry(frame1,textvariable=var1)
playlistid_label.place(x=0,y=10)
playlistid_entry.place(x=80,y=10)

search=Button(top1,text='搜索',bg='yellow',command=collect)
search.place(x=250,y=6)

#唱片图片
cover1=PhotoImage(file='blank.gif')
albumpic=Label(top1,bg='Ivory',image=cover1,height=75,width=75)
albumpic.place(x=0,y=43)
popular=Label(top1,bg='Ivory',height=4,width=30)
popular.place(x=90,y=45)
#中间列表

frame2=Frame(top1,bg='Ivory',height=300,width=280)
frame2.place(x=0,y=150)
frame2.columnconfigure(0,weight=1)
frame2.rowconfigure(0,weight=1)

canvas=Canvas(frame2,height=180,width=280,scrollregion=(0,0,1000,50000))
cv_frame1=Frame(canvas)
cv_frame2=canvas.create_window(0,0,window=cv_frame1,anchor='nw',width=1500,height=15000)



columns=('序号','歌曲名','歌手','专辑名','时长','热度')
treeview = ttk.Treeview(cv_frame1,height=180,show='headings',columns=columns)
#treeview浏览歌曲
treeview.column('序号',width=40)
treeview.heading('序号',text='序号')
for i in range(1,6):
    treeview.column(columns[i])
    treeview.heading(columns[i],text=columns[i])



#放置滚动条
xbar=Scrollbar(frame2,orient=HORIZONTAL)
xbar.config(command=canvas.xview)
canvas.configure(xscrollcommand=xbar.set)
ybar=Scrollbar(frame2,orient=VERTICAL)
ybar.config(command=canvas.yview)
canvas.configure(yscrollcommand=ybar.set)

treeview.place(x=0,y=0)
xbar.pack(side=BOTTOM,fill=X)
ybar.pack(side=RIGHT,fill=Y)
canvas.pack(side=LEFT)

#点击选中
def treeviewClick(event):
    global point
    for item in treeview.selection():
        song_name=treeview.item(item,'values')
        point=song_name[1]
#下载功能的图标按钮
downloadpic=PhotoImage(file='下载.png')
downloadbutton=Button(top1,image=downloadpic,command=download)
downloadbutton.place(x=100,y=400)

stopbutton=Button(top1,text='停止播放',command=broadcast_shut)
stopbutton.place(x=200,y=400)

def clean():    
    shutil.rmtree("D:/Music_temp")
cleanbutton=Button(top1,text='清除缓存',command=clean)
cleanbutton.place(x=200,y=450)

treeview.bind('<ButtonRelease-1>',treeviewClick)

top1.mainloop()




