import sys
from PyQt5.QtWidgets import (QApplication, QAction, QWidget,
QMainWindow, QGridLayout,QPushButton, QGroupBox,QVBoxLayout,
QToolButton, QHBoxLayout, QMenuBar)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize, Qt
from functools import partial

class MainWindow(QWidget):

    def __init__(self, parent=None): 
        super().__init__()
        self.parent = parent
        mainMenu = QMenuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        helpMenu = mainMenu.addMenu('Help')
 
        # Make grid and add mode buttons
        self.horizontalGroupBox = QGroupBox()
        grid = QHBoxLayout()
        
        liveBtn = QToolButton()
        liveBtn.setText('Live Mode')
        liveBtn.setIcon(QIcon(QPixmap('images/live_mode')))
        liveBtn.setIconSize(QSize(100, 100))
        liveBtn.clicked.connect(lambda: self.parent.change_view("live_mode"))
        self.setStyleSheet("QToolButton { min-width: 200px; min-height: 180px; font-family: helvetica; font-size: 24px}")
        liveBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        trainingBtn = QToolButton()
        trainingBtn.setText('Training Mode')
        trainingBtn.setIcon(QIcon(QPixmap('images/training_mode')))
        trainingBtn.setIconSize(QSize(100, 100))
        trainingBtn.clicked.connect(lambda: self.parent.change_view("training_mode"))
        self.setStyleSheet("QToolButton { min-width: 200px; min-height: 180px; font-family: helvetica; font-size: 24px}")
        trainingBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        testingBtn = QToolButton()
        testingBtn.setText('Testing Mode')
        testingBtn.setIcon(QIcon(QPixmap('images/test_mode')))
        testingBtn.setIconSize(QSize(100, 100))
        testingBtn.clicked.connect(lambda: self.parent.change_view("test_mode"))
        self.setStyleSheet("QToolButton { min-width: 200px; min-height: 180px; font-family: helvetica; font-size: 24px}")
        testingBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        grid.addWidget(liveBtn)
        grid.addWidget(trainingBtn)
        grid.addWidget(testingBtn)

        liveMode = QAction("&Live Mode", self)
        liveMode.triggered.connect(lambda: self.parent.change_view("live_mode"))
        trainingMode = QAction("&Training Mode", self)
        trainingMode.triggered.connect(lambda: self.parent.change_view("training_mode"))
        testMode = QAction("&Test Mode", self)
        testMode.triggered.connect(lambda: self.parent.change_view("test_mode"))
        
        viewMenu.addAction(liveMode)
        viewMenu.addAction(trainingMode)
        viewMenu.addAction(testMode)

        self.horizontalGroupBox.setLayout(grid)
        self.windowLayout = QVBoxLayout()
        self.windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(self.windowLayout)
