<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======


=======
from liveView import LiveWindow
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import (QWidget, QGridLayout)
import utility.ultraCortexConnector as ucc
from functools import partial 
import time
import csv
>>>>>>> Stashed changes

SCALE_FACTOR_EEG = (4500000)/24/(2**23-1) #uV/count

class LiveController(QWidget):
      
    def __init__(self, parent=None):
<<<<<<< Updated upstream
        self.parent = parent
>>>>>>> Stashed changes
=======
        super().__init__()
        self.controller = parent
        self.view = LiveWindow(parent = self)
        self.boardConnection = None
        self.samplesThread = None
        self.measurmentTable = []
        self.x = []     #this will be updated by refereanc in UCC class also in GetSampleThread

    def loadPlots(self):
        self.boardConnection = ucc.connectToBoard()
        #self.samplesThread = GetSampleThread(self.boardConnection, self.x)
        #self.samplesThread.start() #Starting collection of samples
        self.view.initPlot(self.x)
        #self.timer = QtCore.QTimer()
        #self.timer.setInterval(1000)
        #self.timer.timeout.connect(lambda: self.view.initPlot(self.x))
        #self.timer.start()
        
class GetSampleThread(QThread):
    def __init__(self, boardConnection, x):
        QThread.__init__(self)
        self.boardConnection = boardConnection
        self.x = x

    def run(self):
        with open('test.csv', 'w', newline='') as file:
            self.writer = csv.writer(file)

        ucc.saveLiveSampsToList(self.boardConnection, self.x, self.writer)
        
>>>>>>> Stashed changes
