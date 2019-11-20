from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtWidgets import (QApplication, QAction, QLineEdit,
                            QLabel, QWidget, QMainWindow, QListWidget,
                           QGridLayout,QPushButton, QGroupBox,
                           QVBoxLayout, QToolButton, QHBoxLayout)
import pyqtgraph as pg
import numpy as np
import sys,os
import time
import random
import threading
import controllers.trainingController


class StartNewTestGUI(QWidget):
    def initWindow(self):
        p = controllers.trainingcontroller.trainingController
        path = p.pathFinder(self)
        fileNames = p.scanFolder(self,path)
        picID = []
        arraySize = (len(fileNames)-1)
        for i in range(0,arraySize):
            x = random.randint(0,arraySize)
            if x not in picID:
                picID[i] = x

        print(picID)
        

    def __init__(self):
        QWidget.__init__(self)
        self.initWindow()
        self.show()

        