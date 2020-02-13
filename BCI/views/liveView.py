<<<<<<< Updated upstream
from PyQt5.QtWidgets import (QApplication, QAction,
                            QLabel, QWidget, QMainWindow,
                           QGridLayout,QPushButton, QGroupBox,
                           QVBoxLayout, QToolButton, QHBoxLayout)
=======
from PyQt5.QtWidgets import (QWidget, QGridLayout)
from PyQt5 import QtWidgets, QtCore, uic
>>>>>>> Stashed changes
import pyqtgraph as pg
import numpy as np
from pyOpenBCI import OpenBCICyton
from pyqtgraph import PlotWidget, plot
from liveController import LiveController
from ultraCortexConnector import connectToBoard

SCALE_FACTOR_EEG = (4500000)/24/(2**23-1) #uV/count

class LiveWindow(QWidget):

    def __init__(self, parent = None):
        super().__init__()
<<<<<<< Updated upstream
        self.parent = parent
        self.initPlot()
        self.show()
=======
        self.controller = parent
        self.boardConnection = None
        self.samplesThread = None
        x = []

        connectToBoard()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()


    def startStream(self, board, sample):
        channelSample = sample.channels_data[0] * SCALE_FACTOR_EEG
        self.x.append(channelSample)
      
    def update_plot_data(self):
        self.x = self.x[1:]  
        self.data_line.setData(self.x)
>>>>>>> Stashed changes

    def initPlot(self,x):
        grid = QGridLayout()
        y = [1,2,3,4,5,6,7,8,9,10]

        for i in range(1,9):
            ch = pg.PlotWidget(title="Channel %d" % i)
            self.data_line = ch.plot(self.x, pen=(255,0,0), name="Red curve")
            grid.addWidget(data_line,i,0)

        for i in range(1,9):
            ch = pg.PlotWidget(title="Channel %d" % (i+8))
            self.data_line = ch.plot(self.x, pen=(255,0,0), name="Red curve")
            grid.addWidget(data_line,i,1)


        self.setLayout(grid)


class getSample(QThread):
    def __init__(self, boardConnection, samplesDict):
        QThread.__init__(self)
        self.boardConnection = boardConnection
        self.samplesDict = samplesDict

    def run(self):
        self.boardConnection.start_stream(callback)