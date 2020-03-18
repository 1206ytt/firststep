# Script Name           : fileinfo.py
# Author                : pekki black(me)
# Created               : 2018
# Last Modified         :
# Version               :  1.1
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
