# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QBasicTimer
import tools
import imagewindow


class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.frColor = []
        self.frDepth = []
        self.tick = 0
        self.timer = QBasicTimer()
        self.btnPlay = QtWidgets.QPushButton()
        self.initUI()
        
    def initUI(self):
        self.setWindowFlags(QtCore.Qt.Window|
                QtCore.Qt.MSWindowsFixedSizeDialogHint|
                QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(30, 30, 600, 110)
        self.setWindowTitle('OpenNI')   
        openFile = QtWidgets.QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.triggered.connect(self.fileDialog)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openFile)
        
        self.btnPlay = QtWidgets.QPushButton('Play', self)
        self.btnPlay.clicked.connect(self.player)
        self.btnPlay.move(130, 30)
        
        self.btnR = QtWidgets.QPushButton('>', self)
        self.btnL = QtWidgets.QPushButton('<', self)
        self.btnR.move(230, 30)
        self.btnL.move(30, 30)

        self.btnR.clicked.connect(self.stepFrame)
        self.btnL.clicked.connect(self.stepFrame) 
        
        self.countframe = QtWidgets.QLabel("0/0", self)
        self.countframe.move(430, 30)
        self.countframe.resize(100, 30)
        self.countframe.show()
        
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider.setGeometry(30, 70, 550, 30)
        self.slider.sliderReleased.connect(self.change)
        self.slider.sliderPressed.connect(self.change)
        self.slider.sliderMoved.connect(self.change) 
        self.window1 = imagewindow.ImageWindow(0)
        self.window2 = imagewindow.ImageWindow(1)
        
    def closeEvent(self,event):
        #диалог выхода
        result = QtWidgets.QMessageBox.question(self,
                      "Выход",
                      "Вы точно хотите выйти?",
                      QtWidgets.QMessageBox.Yes| QtWidgets.QMessageBox.No)
        event.ignore()

        if result == QtWidgets.QMessageBox.Yes:
            sys.exit()
    
    def stepFrame(self):
        #функционал перемотки
        if len(self.frColor)<1:
            return 
        
        sender = self.sender()
        if sender.text() == '>':
            self.play()
            self.slider.setValue(self.tick)
        else:
            if self.tick != 1:
                self.tick -= 2
                self.play()
                self.slider.setValue(self.tick)
            
    def tickPosition(self):
        self.slider.setValue(self.tick)
        
    def timerEvent(self, *args, **kwargs):
        self.play()
        self.tickPosition()
            
    def change(self):
        self.tick = self.slider.value()
        self.play()
    
    def player(self):
        #кнопка play
        if len(self.frColor)<1:
            return
        
        if self.timer.isActive():
            self.timer.stop()
            self.btnPlay.setText('Play')
        else:
            self.timer.start(28, self)            
            self.slider.setRange(0, len(self.frColor))
            #шаг слайдера
            if self.slider.maximum() > self.slider.width():
                step = int(self.slider.maximum()/self.slider.width())
                self.slider.setPageStep(step)                
            self.btnPlay.setText('Stop')
    
    def fileDialog(self):  
        #сброс
        self.frColor.clear()
        self.frDepth.clear()
        self.window1.hide()
        self.window2.hide()
        self.countframe.setText("0/0")
        self.tick = 0
        self.slider.setValue(self.tick)
        #выбор файла
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '*.oni')[0]
        if fileName != '':            
            splash = QtWidgets.QSplashScreen(QtGui.QPixmap("loading.jpg"))
            splash.showMessage("Загрузка фрейма ",QtCore.Qt.AlignHCenter|
                    QtCore.Qt.AlignBottom, QtCore.Qt.black)
            splash.show()
            self.hide()
            QtWidgets.qApp.processEvents()
            self.frColor, self.frDepth = tools.getFrames(str.encode(fileName),splash)
            splash.finish(self)
            self.show()            
            self.play()
            
    def play(self):
        # проигрывание фреймов
        if len(self.frColor)<1:
            return
        
        if self.tick >= len(self.frColor)-1:
            self.timer.stop()
            self.btnPlay.setText('Play')
            
        if self.tick >= len(self.frColor):
            return
        #отображаем данные о позиции
        s = "{0}/{1}".format(self.tick,len(self.frColor))
        self.countframe.setText(s)
        image = self.frColor[self.tick]
        depth = self.frDepth[self.tick]        
        bytesPerLine = 3*640
        
        cImg = QtGui.QImage(image.data, image.width, image.height, bytesPerLine, QtGui.QImage.Format_RGB888)
        
        #ddImg = QtGui.QImage(depth.data, depth.width, depth.height, bytesPerLine, QtGui.QImage.Format_Indexed8)
                
        dImg = tools.NP2QI(depth)   #преобразование nparray to QImage     
        
        pixmap01 = QtGui.QPixmap.fromImage(cImg)
        pixmap02 = QtGui.QPixmap.fromImage(dImg)
        pixmap02z = pixmap02.scaled(dImg.width(), dImg.height()*2)
        
        #pixmap02z = QtGui.QPixmap.fromImage(ddImg)
        
        #показ окон с изображениями
        if self.tick == 0:
            self.window1.setGeometry(pixmap02z.width()/2+40, 200, pixmap01.width(), pixmap01.height())
            self.window2.setGeometry(30, 200, pixmap02z.width()/2, pixmap02z.height()/2)
        
        self.window2.loadpixmap(pixmap02z,self.tick)
        self.window1.loadpixmap(pixmap01,self.tick)
        
        self.window1.show()
        self.window2.show()
        
        self.tick += 1


def run():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    sys.exit()    

if __name__ == '__main__': 
    run()