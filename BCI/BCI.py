import sys
from PyQt5.QtWidgets import (QApplication, QAction, QWidget,
QMainWindow, QGridLayout,QPushButton, QGroupBox,QVBoxLayout,
QToolButton, QHBoxLayout)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize, Qt
from functools import partial

from componants.main import *
from componants.live import *
from componants.training import *
from componants.testing import *
from model.model import Model

class App(QMainWindow):

    def __init__(self, root):
        super().__init__()
        self.model = Model()
        self.title = 'BCI Hamburg Software v1.0'
        self.setWindowTitle(self.title)
        mainWindow.initUI(self)

    def change_view(self, viewName):
        if viewName == "live_mode":
            self.setCentralWidget(liveWindow(self))
        elif viewName == "test_mode":
            self.setCentralWidget(testWindow(self))
        elif viewName == "training_mode":
            self.setCentralWidget(trainingWindow(self))



if __name__ == '__main__':
    root = QApplication(sys.argv)
    ex = App(root)
    sys.exit(root.exec_())
