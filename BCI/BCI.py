import sys
from PyQt5.QtWidgets import (QApplication, QAction, QWidget,
QMainWindow, QGridLayout,QPushButton, QGroupBox,QVBoxLayout,
QToolButton, QHBoxLayout)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize, Qt
from functools import partial

from views.main import *
from views.live import *
from views.training import *
from views.testing import *


class App(QMainWindow):

    def __init__(self, root):
        super().__init__()
        self.title = 'BCI Hamburg Software v1.0'
        self.setWindowTitle(self.title)
        mainWindow.initUI(self)



if __name__ == '__main__':
    root = QApplication(sys.argv)
    ex = App(root)
    sys.exit(root.exec_())
