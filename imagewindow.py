from PyQt5 import QtWidgets, QtCore

class ImageWindow(QtWidgets.QMainWindow):

    def __init__(self,n):
        QtWidgets.QMainWindow.__init__(self)
        self.N = n # тип окна
        self.initUI()

    def initUI(self):
        #положение компонентов, размеры окна и положение
        self.setWindowFlags(QtCore.Qt.Window)
        if self.N == 0:
            self.setGeometry(140, 200, 100, 100)
            self.setWindowTitle('OpenNI color frames')
        else:
            self.setGeometry(30, 200, 100, 100)
            self.setWindowTitle('OpenNI depth frames')

        self.pixmap = QtWidgets.QGraphicsPixmapItem()
        graphicsView = QtWidgets.QGraphicsView()

        scene = QtWidgets.QGraphicsScene()
        self.pixmap = QtWidgets.QGraphicsPixmapItem()
        scene.addItem(self.pixmap)
        graphicsView.setScene(scene)

        self.widget = QtWidgets.QWidget(self)
        if self.N == 0:
            self.widget.setGeometry(0,0,self.width(),self.height())
        else:
            self.widget.setGeometry(0,0,self.width()/2,self.height()/2)

        self.grid = QtWidgets.QGridLayout(self.widget)
        self.grid.addWidget(graphicsView,0,0)
        self.grid.setColumnMinimumWidth(0, 0)
        self.widget.setLayout(self.grid)

    def resizeEvent(self, event):
        #изменение размера
        self.widget.setGeometry(0,0,self.width(),self.height())
        self.grid.setColumnMinimumWidth(0, self.widget.width())
        QtWidgets.QMainWindow.resizeEvent(self, event)

    def loadpixmap(self,pixmap,tick):
        if tick ==0:
            #при первом тике менем размеры согласно изображению
            if self.N == 0:
                self.resize(pixmap.width(), pixmap.height())
            else:
                self.resize(pixmap.width()/2, pixmap.height()/2)

            if self.N == 0:
                self.widget.setGeometry(0,0,pixmap.width(),pixmap.height())
            else:
                self.widget.setGeometry(0,0,pixmap.width()/2,pixmap.height()/2)

            self.grid.setColumnMinimumWidth(0, self.widget.width())
        #загрузка изображения
        self.pixmap.setPixmap(pixmap)
