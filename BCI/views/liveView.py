<<<<<<< Updated upstream
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
=======
from PyQt5.QtWidgets import (QWidget, QGridLayout, QGroupBox, QHBoxLayout)
from PyQt5 import QtGui, QtCore
import numpy as np
import time
import psutil
import matplotlib.pyplot as plt

SCALE_FACTOR_EEG = (4500000)/24/(2**23-1) 
>>>>>>> Stashed changes

class LiveWindow(QWidget):

    def __init__(self, parent = None):
        super().__init__()
<<<<<<< Updated upstream
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
=======
        self.controller = parent
        self.grid = QGridLayout()
        self.loadPlot = QtGui.QPushButton("Start",self)
        self.loadPlot.clicked.connect(lambda: self.controller.loadPlots())
        self.grid.addWidget(self.loadPlot)
        self.setLayout(self.grid) 

    def initPlot(self, x):
        self.x = x
        #print(len(x))
        #if (len(x) > 50):
        #    x1 = [x.channels_data[0] for x in self.x]
        #else:
        #    pass
        matplotlib.use("Agg")
        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig.show()
        i = 0
        x, y = [], []

        while True:
            x.append(i)
            y.append(psutil.cpu_percent())
    
            ax.plot(x, y, color='b')
    
            fig.canvas.draw()
    
            ax.set_xlim(left=max(0, i-50), right=i+50)
    
            time.sleep(0.1)
            i += 1
>>>>>>> Stashed changes
