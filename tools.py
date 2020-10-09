from primesense import openni2 as OP2
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
import cv2

def getFrames(file_name,splash):
    #получение данных фреймов из файла oni в массивы
    OP2.initialize('C:\\Program Files\\OpenNI2\\Redist\\') #путь к dll OpenNI2
    frColor = []
    frDepth = []
    file = OP2.Device(file_name)
    file.set_depth_color_sync_enabled
    colorStream = OP2.VideoStream(file,OP2.SENSOR_COLOR)#цветной поток
    depthStream = OP2.VideoStream(file, OP2.SENSOR_DEPTH)#глубина поток
    colorStream.start()
    depthStream.start()
    len_frames = colorStream.get_number_of_frames()
    for i in range(len_frames):
        #наполняем массивы
        frColor.append(colorStream.read_frame())
        frDepth.append(depthStream.read_frame())
        QtWidgets.qApp.processEvents()
        splash.showMessage("Загрузка фрейма {0}/{1}".format(i,len_frames),
                           QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom,
                           QtCore.Qt.black)
    colorStream.stop()
    depthStream.stop()
    return frColor, frDepth

def NP2QI(frame):
    #преобразование nparray to QImage
    frame_data = frame.get_buffer_as_uint16()
    img = np.frombuffer(frame_data, dtype=np.uint16)
    #bytesPerLine = 3*640
    img.shape = (1, frame.height, frame.width) #изменяем размерность массива точек
    img = np.concatenate((img, img, img), axis=0) #объединение массивов вдоль оси axis=0
    img = np.swapaxes(img, 0, 2) #обмен осями 0,2
    img = np.swapaxes(img, 0, 1) #обмен осями 0,1
    height, width, channel = img.shape #получаем данные о размерности
    width2 = img.strides[0] #кол-во offsset байт
    cvRGBImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #преобразование изображений из одного цветового пространства в GRAY
    qimage = QtGui.QImage(cvRGBImg.data, width2, height,  width2,
                          QtGui.QImage.Format_Indexed8)
    return qimage
