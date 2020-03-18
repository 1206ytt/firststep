# Script Name           : fileinfo.py
# Author                : pekki black(me)
# Created               : 2018
# Last Modified         :
# Version               :  1.2
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
