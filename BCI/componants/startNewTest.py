from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtWidgets import (QApplication, QAction, QLineEdit,
                            QLabel, QWidget, QMainWindow, QListWidget,
                           QGridLayout,QPushButton, QGroupBox,
                           QVBoxLayout, QToolButton, QHBoxLayout)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QPixmap
import pyqtgraph as pg
import numpy as np
import sys,os
import time
import random
import threading

path = 'C:\\Users\\alama\\Desktop\\pic'

class startNewTestGUI(QWidget):
    def initWindow(self):
        fileNames = os.listdir(path)
        x = random.randint(0,4)
        label = QLabel(self)
        pixmap = QPixmap(path + '\\' + fileNames[x])
        label.setPixmap(pixmap)

    def __init__(self):
        QWidget.__init__(self)
        self.initWindow()
        threading.Timer(5.0, self.initWindow()).start() 
        self.show()

