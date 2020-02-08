from PyQt5.QtWidgets import (QWidget, QGridLayout)
import pyqtgraph as pg
import numpy as np

class LiveWindow(QWidget):

    def __init__(self, parent = None):
        super().__init__()
        self.controller = parent
        self.initPlot()

    def initPlot(self):
        grid = QGridLayout()
        
        x = []
        y = []

        for i in range(1,9):
            ch = pg.PlotWidget(title="Channel %d" % i)
            ch.plot(np.random.normal(size=100), pen=(255,0,0), name="Red curve")
            grid.addWidget(ch,i,0)

        for i in range(1,9):
            ch = pg.PlotWidget(title="Channel %d" % (i+8))
            ch.plot(np.random.normal(size=100), pen=(255,0,0), name="Red curve")
            grid.addWidget(ch,i,1)

        self.setLayout(grid)