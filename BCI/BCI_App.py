import sys
from PyQt5.QtWidgets import (QApplication, QAction, QWidget,
QMainWindow, QGridLayout,QPushButton, QGroupBox,QVBoxLayout,
QToolButton, QHBoxLayout)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize, Qt
from functools import partial
import controllers.mainController as MainCon

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'BCI Hamburg Software v1.0'
        self.setWindowTitle(self.title)
        self.controller = MainCon.MainController(parent=self)
        self.setCentralWidget(self.controller.view)
        self.show()

if __name__ == '__main__':
    root = QApplication(sys.argv)
    ex = App()
    sys.exit(root.exec_())
