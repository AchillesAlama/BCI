from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, 
                             QLabel, QGridLayout, QDesktopWidget, 
                             QPushButton)
from PyQt5.QtGui import QPixmap,QSizePolicy, QDesktopWidget, QFont, QShortcut, QKeySequence
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

class RunView(QWidget):
    """This class represents the full screen window used during runs/experiments.
    Normal use case would be to have the window display different images whilst
    collecting data with the EEG headset."""

    def __init__(self, parent = None):
        super().__init__()
        self.controller = parent
        self.initUI()

    def initUI(self):
        self.mainGrid = QGridLayout()
        self.setLayout(self.mainGrid)

        #Create image holding label
        self.centralLabel = QLabel(self)
        self.centralLabel.setAlignment(Qt.AlignCenter)
        countdownFont = QFont("Times", 42, QFont.Bold)
        self.centralLabel.setFont(countdownFont)
        self.mainGrid.addWidget(self.centralLabel, 0, 0)
        
        #Allow user to abort run on pressing escape
        abortShortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        abortShortcut.activated.connect(self.controller.escapePressed)

        #Open in full screen
        self.showMaximized()
        QApplication.processEvents()        
        
       
    def closeEvent(self, event):
        """Called when user closes window, used to stop timer."""
        self.controller.imgChangeTimer.stop()
        event.accept()

    def setNewImage(self, imgPath):
        self.centralLabel.setPixmap(QPixmap(imgPath))
       