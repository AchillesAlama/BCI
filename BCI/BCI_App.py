from PyQt5.QtWidgets import (QApplication, QAction, QWidget,
QMainWindow, QGridLayout,QPushButton, QGroupBox,QVBoxLayout,
QToolButton, QHBoxLayout)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize, Qt
from controllers.mainController import MainController
import sys
from functools import partial

class App(QMainWindow):

    def __init__(self):
        #Init window params
        super().__init__()
        self.title = 'BCI Hamburg Software v1.0'
        self.setWindowTitle(self.title)

        #Create main controller and set its view to central widget
        self.controller = MainController(parent=self)
        self.setCentralWidget(self.controller.view)

        #Menu belongs to main window
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Mode')

        #Add menu options for changing between modes
        for mode in ["live_mode", "training_mode", "test_mode"]:
            modeAction = QAction('&' + mode.replace("_", " ").title(), self)
            modeAction.triggered.connect(partial(self.controller.change_view, mode))
            fileMenu.addAction(modeAction)

        self.show()

if __name__ == '__main__':
    root = QApplication(sys.argv)
    ex = App()
    sys.exit(root.exec_())
