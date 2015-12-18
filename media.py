#!/usr/bin/python3
# -*- coding: utf8 -*-

from PyQt5.QtMultimedia import (QMediaPlayer, QMediaPlaylist, QMediaContent,QMediaMetaData)
from conf.conf import conf
from PyQt5.QtCore import QUrl,Qt
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QBrush
import os
import re

class Player():
  # 参数music是mainnwindow对象 
  def __init__(self,music):
    self.music = music
    self.music.player = QMediaPlayer()
    # print(dir(self.music.player))
    self.music.playlist = QMediaPlaylist()
    self.music.player.setPlaylist(self.music.playlist)

    self.init_list()
    self.music.playit = self.playit
    self.music.play_or_pause = self.play_or_pause
    self.music.nextone = self.nextone
    self.music.prevone = self.prevone


    self.music.player.metaDataChanged.connect(self.metaDataChanged)
    self.music.player.stateChanged.connect(self.stateChanged)

    # self.play_or_pause()
  def init_list(self):
    #读取配置歌曲目录里面的音乐文件
    listfile = os.listdir(conf['mp3dir'])
    x = 0
    for name in listfile:
      s = os.path.splitext(name)[1][1:]
      if(s.upper() == 'MP3'):
        x+=1
        item = QListWidgetItem("%02d  %s" % (x,name))
        self.music.songList.addItem(item)
        url = QUrl.fromLocalFile(os.path.join(conf['mp3dir'],name))
        self.music.playlist.addMedia(QMediaContent(url))
        
  def playit(self,eve):
    s = eve.text()
    p = re.compile(r'\d+')
    r = p.findall(s)
    self.music.playlist.setCurrentIndex(int(r[0])-1)
    self.music.player.play()

  def play_or_pause(self):
      if self.music.player.state() in (QMediaPlayer.StoppedState, QMediaPlayer.PausedState):
          self.music.player.play()
      elif self.music.player.state() == QMediaPlayer.PlayingState:
          self.music.player.pause()

  def nextone(self):
    self.music.playlist.next()
    self.music.player.play()
  def prevone(self):
    self.music.playlist.previous()
    self.music.player.play()

  def metaDataChanged(self):
    if self.music.player.isMetaDataAvailable(): 
      self.music.currentMusicName.setText(self.music.player.metaData(QMediaMetaData.Title))
      

  def stateChanged(self):
    if self.music.player.state() in (QMediaPlayer.StoppedState, QMediaPlayer.PausedState):
      self.setPlayBtn('play11')
    elif self.music.player.state() == QMediaPlayer.PlayingState:
      self.setPlayBtn('pause11')

  def setPlayBtn(self,stat):
    self.music.playBtn.setStyleSheet("QPushButton{ border-image:url(image/%s.png);border:none }" % stat)

  

if __name__ == "__main__":
    # listfile = os.listdir(conf['mp3dir'])
    # for name in listfile:
    #   print(os.path.join(conf['mp3dir'],name))
    m = Player()
    # print("oooo")
