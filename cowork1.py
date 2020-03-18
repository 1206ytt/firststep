# Script Name           : fileinfo.py
# Author                : pekki black(me)
# Created               : 2018
# Last Modified         :
# Version               :  1.0
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
