#!/usr/bin/python3
# -*- coding: utf8 -*-


import sys,ctypes,os
from PyQt5.QtWidgets import (QApplication,QWidget,QPushButton,QLabel,QProgressBar,QListWidget, QSystemTrayIcon,QMenu,QAction,QGraphicsDropShadowEffect,QGraphicsBlurEffect,QListWidgetItem,QSlider,QDialog)
from PyQt5.QtCore import Qt,QSize,QUrl,QThread,QPoint,pyqtSignal
from PyQt5.QtGui import ( QCursor,QIcon,QBrush,QDesktopServices,QLinearGradient,QLinearGradient,QFont,QPainter,QColor)
from PyQt5.QtMultimedia import (QMediaPlayer, QMediaPlaylist, QMediaContent)
from conf.conf import conf
from mywidget import *
from qss import *
from media import *
from singer import *

# ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
class Music(QWidget):
	def __init__(self):
		super().__init__()
		self.currentSonger = ''
		self.setWindowIcon(QIcon("image/tray.png"))
		self.setWindowTitle("SYL")
		self.setObjectName("box")
		# 窗口无边框
		self.setWindowFlags(Qt.FramelessWindowHint)
		# 窗口居于所有窗口的顶端 
		self.setWindowFlags(Qt.WindowOverridesSystemGestures)
		# 窗口居于所有窗口的顶端  针对部分X11
		self.setWindowFlags(Qt.X11BypassWindowManagerHint)
		# 初始化基本UI界面
		self.initUI()
		# 初始化播放核心
		self.initplayer()
		# 显示主界面
		self.show()
		
	def initUI(self):
		# 获取电脑屏幕宽高 让主界面初始化后处于屏幕中间
		wh = QApplication.desktop().screenGeometry()
		self.screen_w , self.screen_h = wh.width() ,wh.height()
		self.setGeometry(int((self.screen_w-300)/2),int((self.screen_h-600)/2),300,600)
		self.setWindowOpacity(0.97); 

		#当前播放歌曲的封面 
		songer_img = DragLabel(self)
		songer_img.setParent(self)
		songer_img.resize(300,200)

		self.picture = QLabel(songer_img)
		self.picture.resize(300,200)
		self.picture.setStyleSheet("QLabel{ background:#000;border-image:url(image/newimg/back.jpg)}")

		# syl = QLabel(songer_img)
		# syl.setGeometry(15,5,34,15)
		# syl.setStyleSheet("QLabel{ border-image:url(image/newimg/logo.png);}")

		# ================================
		songinfo = QLabel(songer_img)
		songinfo.setGeometry(0,30,300,80)
		songinfo.setStyleSheet("QLabel{ background:transparent;}")

		songpic = QLabel(songinfo)
		songpic.setGeometry(10,0,80,80)
		songpic.setStyleSheet("QLabel{ border-image:url(image/newimg/user.jpg);border-radius:2px;}")

		self.songname = QLabel("老鼠爱大米 - 香香",songinfo)
		self.songname.setGeometry(105,0,210,25)
		self.songname.setStyleSheet("QLabel{ color:#EEE;font-size:15px;}")
		uploaduser = QLabel("By 张三的歌",songinfo)
		uploaduser.move(105,25)
		uploaduser.setCursor(QCursor(Qt.PointingHandCursor))
		uploaduser.setStyleSheet("QLabel{ color:yellow;font-size:15px;} QLabel:hover{color:red}")

		fenshu = QLabel("评分 - 7.6",songinfo)
		fenshu.setGeometry(105,50,210,25)
		# self.picture.setGraphicsEffect(QGraphicsBlurEffect())
		fenshu.setStyleSheet("QLabel{ color:#EEE;font-size:15px;}")


		songtool = QLabel(songer_img)
		songtool.setGeometry(0,110,300,35)
		songtool.setStyleSheet("QLabel{ background:transparent;}")

		playmodel = QLabel(songtool)
		playmodel.setGeometry(20,10,25,25)
		# self.picture.setGraphicsEffect(QGraphicsBlurEffect())
		playmodel.setStyleSheet("QLabel{ border-image:url(image/newimg/kg_ic_player_liked.png);}")

		pinglun = QLabel(songtool)
		pinglun.setGeometry(50,5,33,33)
		# self.picture.setGraphicsEffect(QGraphicsBlurEffect())
		pinglun.setStyleSheet("QLabel{ border-image:url(image/newimg/pinglun.png);}")

		pingfen = QLabel("查看这首歌的更多资料",songtool)
		pingfen.move(100,10)
		pingfen.setCursor(QCursor(Qt.PointingHandCursor))
		pingfen.setStyleSheet("QLabel{ color:#BBB} QLabel:hover{color:pink}")


		# ======================================

		# 顶部工具栏
		# 隐藏
		btn = QPushButton("",self)
		btn.setGeometry(270,0,15,32)
		btn.setCursor(QCursor(Qt.PointingHandCursor))
		btn.setStyleSheet("QPushButton{ border:none;color:white;background:transparent;border-image:url(image/newimg/mini.png) } ")
		btn.clicked.connect(self.close)
		# 设置封面
		# btn = QPushButton("",self)
		# btn.setGeometry(230,-10,41,48)
		# btn.setCursor(QCursor(Qt.PointingHandCursor))
		# btn.setStyleSheet("QPushButton{ border:none;color:white;background:transparent;border-image:url(image/newimg/fengmian.png) } ")
		# btn.clicked.connect(self.setHeaderImg)
		# 开启/关闭歌词
		# btn = QPushButton("",self)
		# btn.setGeometry(200,0,30,30)
		# btn.setCursor(QCursor(Qt.PointingHandCursor))
		# btn.setStyleSheet("QPushButton{ border:none;color:white;background:transparent;border-image:url(image/newimg/geci.png) } ")
		# btn.clicked.connect(self.lrc)
		# 播放模式  单曲循环  整体循环  随机播放
		# self.btnmoshi = QPushButton("全部",self)
		# self.btnmoshi.setGeometry(170,0,40,20)
		# self.btnmoshi.setCursor(QCursor(Qt.PointingHandCursor))
		# self.btnmoshi.setStyleSheet("QPushButton{ border:none;color:white;background:transparent } ")
		# self.btnmoshi.clicked.connect(self.moshi)

		# 播放组件  ( 播放  前进 后退 播放时间 进度条 歌曲名 音量 )
		# 播放/暂停
		self.playBtn = QPushButton("",songer_img)
		self.playBtn.setGeometry(130,155,32,25)
		self.playBtn.setStyleSheet("QPushButton{ border-image:url(image/newimg/statusbar_btn_play.png);border:none } QPushButton:hover{ border-image:url(image/newimg/statusbar_btn_play.png)} ")
		# 下一首
		self.nextBtn = QPushButton("",songer_img)
		self.nextBtn.setGeometry(186,159,20,20)
		self.nextBtn.setStyleSheet("QPushButton{ border-image:url(image/newimg/statusbar_btn_next.png);border:none } QPushButton:hover{ border-image:url(image/newimg/statusbar_btn_next.png)}")
		# 播放模式
		self.prevBtn = QPushButton("",songer_img)
		self.prevBtn.setGeometry(236,159,20,20)
		self.prevBtn.setStyleSheet("QPushButton{ border-image:url(image/newimg/ic_player_menu_volume.png);border:none } QPushButton:hover{ border-image:url(image/newimg/ic_player_menu_volume.png)}")

		# 上一首
		self.prevBtn = QPushButton("",songer_img)
		self.prevBtn.setGeometry(85,159,20,20)
		self.prevBtn.setStyleSheet("QPushButton{ border-image:url(image/newimg/statusbar_btn_prev.png);border:none } QPushButton:hover{ border-image:url(image/newimg/statusbar_btn_prev.png)}")
		# 播放模式
		self.prevBtn = QPushButton("",songer_img)
		self.prevBtn.setGeometry(35,156,25,25)
		self.prevBtn.setStyleSheet("QPushButton{ border-image:url(image/newimg/ic_player_mode_single_default.png);border:none } QPushButton:hover{ border-image:url(image/newimg/ic_player_mode_single_default.png)}")

		# 当前播放时间
		self.songTime = QLabel("",self)
		self.songTime.setGeometry(220,180,80,20)
		self.songTime.setStyleSheet("QLabel{ color:#AAA;font-size:12px;}")
		self.songTime.setAlignment(Qt.AlignHCenter)
		# 音量
		# self.vol = QSlider(Qt.Horizontal,self)
		# self.vol.setGeometry(10,144,50,5)
		# self.vol.setValue(60)
		# self.vol.setStyleSheet(qss_vol)
		# 当前歌曲名   
		self.currentMusicName = QLabel("",songer_img)
		self.currentMusicName.setGeometry(0,180,200,20)
		self.currentMusicName.setStyleSheet("QLabel{ color:white ;font-weight:100;font-size:12px;margin-left:5px;}")
		# 歌曲进度条
		self.processSlider = QSlider(Qt.Horizontal,self)
		self.processSlider.setGeometry(0,193,300,7)
		# self.processSlider.setRange(1,100)
		# self.processSlider.setValue(0)
		self.processSlider.setStyleSheet(qss_process_slider)
		
		self.processSlider.setCursor(QCursor(Qt.UpArrowCursor))

		# 歌曲列表 ---------------------------
		listWgt = QWidget(self)
		listWgt.setGeometry(0, 200, 300,380)
		listWgt.setStyleSheet(qss_scrollbar)
		# 补白
		bu = QWidget(listWgt)
		bu.setGeometry(0,0,5,380)
		# bu.setStyleSheet("QWidget{ border-image:url(image/borderleft.png) }")

		bu2 = QWidget(listWgt)
		bu2.setGeometry(295,0,5,380)
		# bu2.setStyleSheet("QWidget{ border-image:url(image/borderright.png) }")

		#列表
		self.songList = QListWidget(listWgt)
		self.songList.setGeometry(5,0,235,380)   
		self.songList.setStyleSheet(qss_songlist)	
		# 列表添加右键菜单
		# self.songList.setContextMenuPolicy(Qt.CustomContextMenu)
		# self.songList.customContextMenuRequested.connect(self.rightMenuShow)

		#歌曲列表右边的功能列表
		funcList = QListWidget(listWgt)
		funcList.setGeometry(240,0,55,380)   
		funcList.setStyleSheet(qss_menu)
		btn = QPushButton("",funcList)
		btn.clicked.connect(self.newwindow)
		btn.setGeometry(15,10,30,30)
		btn.setStyleSheet("QPushButton{ border-image:url(image/home.png)} \
			QPushButton:hover{ border-image:url(image/homehover.png) }")
		btn.setCursor(QCursor(Qt.PointingHandCursor))
		btn = QPushButton("",funcList)
		btn.setGeometry(15,60,30,30)
		btn.setStyleSheet("QPushButton{ border-image:url(image/tuijian.png) } \
			QPushButton:hover{ border-image:url(image/tuijianhover.png) }")
		btn.setCursor(QCursor(Qt.PointingHandCursor))
		btn = QPushButton("",funcList)
		btn.setGeometry(15,100,30,30)
		btn.setStyleSheet("QPushButton{ border-image:url(image/shoucang.png) }\QPushButton:hover{ border-image:url(image/shoucanghover.png) }")
		btn.setCursor(QCursor(Qt.PointingHandCursor))

		btn = QPushButton("",funcList)
		btn.setGeometry(15,140,30,30)
		btn.setStyleSheet("QPushButton{ border-image:url(image/rizhi.png) }\
			QPushButton:hover{ border-image:url(image/rizhihover.png) }")
		btn.setCursor(QCursor(Qt.PointingHandCursor))

		btn = QPushButton("",funcList)
		btn.setGeometry(17,180,30,30)
		btn.setStyleSheet("QPushButton{ border-image:url(image/mv.png) }\
			QPushButton:hover{ border-image:url(image/mvhover.png) }")
		btn.setCursor(QCursor(Qt.PointingHandCursor))

		btn = QPushButton("",funcList)
		btn.setGeometry(15,225,33,33)
		btn.setStyleSheet("QPushButton{ border-image:url(image/settinghover.png) }\
			QPushButton:hover{ border-image:url(image/setting.png) }")
		btn.setCursor(QCursor(Qt.PointingHandCursor))

		# btn = QPushButton("日志",funcList).setGeometry(0,120,55,40)
		# btn = QPushButton("M V",funcList).setGeometry(0,160,55,40)
		# btn = QPushButton("关于",funcList).setGeometry(0,200,60,40)
		#底部状态栏
		wg = QWidget(self)
		wg.setGeometry(0, 580, 300,20)
		wg.setStyleSheet("QWidget{ background:#2D2D2D; } ")
		ql = QLabel(" <a style='color:grey;text-decoration:none;font-size:12px;'  href ='https://github.com/codeAB/music-player' >www.sylsong.com </a>",wg)
		ql.resize(300,20)
		ql.setAlignment(Qt.AlignRight)
		ql.linkActivated.connect(self.openurl)

		#设置托盘图标
		tray = QSystemTrayIcon(self)
		tray.setIcon(QIcon('image/tray.png'))
		self.trayIconMenu = QMenu(self)
		# preAction = QAction(u"上一曲 ", self,triggered=self.close)
		# pauseAction = QAction(u"暂停|播放 ", self,triggered=self.close)
		# nextAction = QAction(u"下一曲 ", self,triggered=self.close)
		# quitAction = QAction(u"退出 ", self,triggered=self.close)
		showAction = QAction(QIcon('image/tray.png'),u"显示主面板", self,triggered=self.show)
		self.trayIconMenu.addAction(showAction)
		# self.trayIconMenu.addAction(preAction)
		# self.trayIconMenu.addAction(pauseAction)
		# self.trayIconMenu.addAction(nextAction)
		# self.trayIconMenu.addAction(quitAction)
		tray.setContextMenu(self.trayIconMenu)
		tray.show()
		tray.activated.connect(self.dbclick_tray)
	# 重写两个方法实现拖动播放器到屏幕顶端自动隐藏
	def enterEvent(self,QMouseEvent):
		if self.y() < 1:
			self.setGeometry(self.x(),0,300,600) 
	def leaveEvent(self,QMouseEvent):
		if self.y() < 1:
			self.setGeometry(self.x(),0,300,1)
			# 窗口居于所有窗口的顶端 
			# self.setWindowFlags(Qt.WindowOverridesSystemGestures)
			#针对X11
			# self.setWindowFlags(Qt.X11BypassWindowManagerHint)
		# else:
			# self.setWindowFlags(Qt.FramelessWindowHint)
	#加载播放核心
	def initplayer(self):
		#play_song_list用来方便的维护列表,主要用来记录当前播放列表
		# self.play_song_list = {}
		self.p = Player(self)
		# self.songList.itemDoubleClicked.connect(self.playit)
		self.playBtn.clicked.connect(self.play_or_pause)
		self.nextBtn.clicked.connect(self.nextone)
		self.prevBtn.clicked.connect(self.prevone)
		# self.lrc()
		# self.vol.valueChanged.connect(self.)
	#双击托盘图标
	def dbclick_tray(self,event):
		if event==QSystemTrayIcon.DoubleClick:
			# self.show()
			if self.isVisible():
				self.hide()
			else:
				self.show()
	#打开音乐窗
	def newwindow(self):
		if not hasattr(self,'widget1'):
			self.widget1 = index()
			self.widget1.setParent(self)
			# 获取屏幕宽高
			wh = QApplication.desktop().screenGeometry()
			self.screen_w , self.screen_h = wh.width() ,wh.height()
			self.move(int((self.screen_w-900)/2),int((self.screen_h-600)/2))
			self.widget1.show()
		else:
			self.widget1.show()
		self.resize(900,600)
		
	#创建右键菜单
	# def rightMenuShow(self,point):
	# 	self.current_context_item = self.songList.itemAt(point)
	# 	if self.current_context_item is None:
	# 		return False
	# 	rightMenu = QMenu(self.songList)
	# 	removeAction = QAction(u"播放", self, triggered=self.deleteSongItem)
	# 	addAction = QAction(u"删除", self, triggered=self.deleteSongItem)    
	# 	addAction = QAction(u"重命名", self, triggered=self.deleteSongItem)    
	# 	rightMenu.addAction(removeAction)
	# 	rightMenu.addAction(addAction)
	# 	rightMenu.exec_(QCursor.pos())
	# def deleteSongItem(self):
	# 	item = self.current_context_item
	# 	# index = item.text()
	# 	x = self.songList.row(self.current_context_item)
	# 	self.newSort(int(x))
		# 获取当前鼠标右键点击的歌曲名
		# songname = self.current_context_item.text()
		# p = re.compile(r'\d+')
		# r = p.findall(songname)
		# item = int(r[0]) - 1;
		# mp3path = conf['mp3dir']
		# i = 0
		# for filename in os.listdir(mp3path):
		# 	if i == item:
		# 		# 删除列表item
		# 		self.songList.takeItem(self.songList.row(self.current_context_item))
		# 		# 删除播放队列item
		# 		self.playlist.removeMedia(item)
		# 		# 删除文件
		# 		os.remove(os.path.join(mp3path, filename))
		# 		break
		# 	i = i+1
	# 当删除或者新增歌曲时更新列表
	# def newSort(self,index,flag = 'del'):
	# 	# 删除歌曲
	# 	if flag == 'del':
	# 		v = self.songList.findChildren(QPushButton,'',Qt.FindChildrenRecursively)
	# 		self.songList.removeItemWidget(self.current_context_item)
	# 		# print(len(v))
	# 		# v[index].parent().remove()
	# 		# print(v[index].parent().hide())
	# 		self.songList.update()
	# 		print(self.songList.count())
	def openurl(self):
		QDesktopServices.openUrl(QUrl("http://sylsong.com"))
	def myclose(self):
		if hasattr(self,'widget1'):
			self.widget1.close() and self.close()
		else:
			self.close()
	def setHeaderImg(self):
		cs = self.currentSonger
		# print(cs)
		# cs = cs.split("-")
		# print(len(cs))
		if len(cs) > 1:
			# print("ooo")
			self.s = Singer(cs,self)
			# self.s.setParent(self)
			self.show()
	def lrc(self):
		if hasattr(self,'lrctext'):
			if self.lrctext.isVisible():
				self.lrctext.setVisible(False)
				self.p.showgeci(1)
			else:
				self.lrctext.setVisible(True)
				self.p.showgeci()
		else:
			self.lrctext = DLabel(self)
			self.p.showgeci()
	def moshi(self):
		ct = self.btnmoshi;
		if ct.text() == '全部':
			ct.setText(str("随机"))
			self.playlist.setPlaybackMode(QMediaPlaylist.Random)
			return False
		if ct.text() == '随机':
			ct.setText(str("单曲"))
			self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
			return False
		if ct.text() == '单曲':
			ct.setText(str("全部"))
			self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
			return False

if __name__ == '__main__':
	app = QApplication(sys.argv)
	music = Music()
	sys.exit(app.exec_())