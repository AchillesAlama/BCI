from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt5.QtWidgets import (QApplication, QAction, QLineEdit,
                            QLabel, QWidget, QMainWindow, QListWidget,
                           QGridLayout,QPushButton, QGroupBox,
                           QVBoxLayout, QToolButton, QHBoxLayout)
import pyqtgraph as pg
import numpy as np
import sys,os
from time import sleep
import random
import datetime
import threading
import controllers.trainingController


class StartNewTestGUI(QWidget):

    def delay(self,duration_in_seconds):
        current_time = datetime.datetime.now()
        end_time = current_time + datetime.timedelta(0,duration_in_seconds)
        while current_time < end_time:
            current_time = datetime.datetime.now()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(200, 0, 0))
        qp.setBrush(QColor(200, 0, 0))
        self.delay(2)
        qp.drawRect(500, 500, 100, 100)
        #self.delay(2)
        #qp.eraseRect(500, 500, 100, 100)
        qp.end()
