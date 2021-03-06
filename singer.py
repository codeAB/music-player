#!/usr/bin/python3
# -*- coding: utf8 -*-

"""
	抓取歌手头像
"""

import sys
import os
import urllib.parse
import urllib.request
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QLabel)
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5.QtCore import Qt, QUrl, pyqtSlot,QTimer
from PyQt5.QtGui import ( QCursor)


class Singer(QWidget):
    
    # def __init__(self,singer,music):
    def __init__(self,singer):
        super().__init__()
        # 窗口居于所有窗口的顶端 
        self.setWindowFlags(Qt.WindowOverridesSystemGestures)
        #针对X11
        self.setWindowFlags(Qt.X11BypassWindowManagerHint)
        self.singer = singer
        # self.music = music
        self.initUI()
        self.show()
        
    def initUI(self):      

        self.w= QWidget(self)
        self.setGeometry(300,100,1000,600)
        l = QLabel("实用说明,搜索需要的图片，在搜索结果页面点击选择的图片即可设置。。双击此处退出",self)
        l.move(0,0)
        self.web = QWebView(self)
        self.web.loadFinished.connect(self.test)
        
        self.web.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.web.page().linkClicked.connect(self.linkClicked)

        self.web.setGeometry(0, 30, 1000, 570)
        # self.btn = QPushButton("测试",self);
        # self.btn.clicked.connect(self.test)
        # self.btn.move(300,550)
        self.web.load(QUrl("http://image.baidu.com/"))
        
    def test(self):
        print("jiazaijieshu")
        frame = self.web.page().currentFrame()
        searchinput = frame.findFirstElement('#kw')
        d = frame.findFirstElement('.img_area_container_box')
        d.removeAllChildren()
        searchinput.setAttribute("value",self.singer)
        # searchinput.setAttribute("readonly","readonly")
    def linkClicked(self,url):
        # print(url.toString())
        url = url.toString()
        pattern = re.compile(r'&word=(.*?)&')
        s = pattern.findall(url)
        k = {'word': s[0]}
        kv = urllib.parse.urlencode(k)
        url = url.replace("word="+s[0], kv)

        res = urllib.request.urlopen(url).read().decode("utf8")
        pattern = re.compile(r'currentImg(.*)<div>',re.S)
        s = pattern.findall(res)
        print(s)
        src="http://img3.imgtn.bdimg.com/it/u=673176467,634723054&amp;fm=21&amp;gp=0.jpg"
        pattern = re.compile(r'src="(.*?)"')
        s = pattern.findall(s[0])
        img_url = s[0].replace("&amp;","&")

        local = os.path.join('./cache/', self.singer+'.jpg')
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'
        req = urllib.request.Request(img_url)
        req.add_header('Referer', 'http://music.baidu.com/?from=new_mp3')
        req.add_header('User-Agent', user_agent)
        f = urllib.request.urlopen(req)
        data = f.read() 
        with open(local, "wb") as code:     
            code.write(data)
            # self.music.picture.setStyleSheet("QLabel{ background:#9B0069;border-image:url("+local+")}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_flag = True
            # if hasattr(self.window, 'widget1'):
            #     self.begin_position2 = event.globalPos() - \
            #         self.window.widget1.pos()
            self.begin_position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.drag_flag:
            # if hasattr(self.window, 'widget1'):
            #     self.window.widget1.move(
            #         QMouseEvent.globalPos() - self.begin_position2)
            #     self.window.move(QMouseEvent.globalPos() - self.begin_position)
            # else:
            self.move(QMouseEvent.globalPos() - self.begin_position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.drag_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
    # def leaveEvent(self,QMouseEvent):
    #     self.close()
    def mouseDoubleClickEvent(self,e):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    s = Singer("张杰")
    sys.exit(app.exec_())
