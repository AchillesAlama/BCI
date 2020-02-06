from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QGridLayout)
from PyQt5.QtGui import QPixmap

class RunView(QWidget):
    """This class represents the full screen window used during runs/experiments.
    Normal use case would be to have the window display different images whilst
    collecting data with the EEG headset."""

    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.mainGrid = QGridLayout()
        self.setLayout(self.mainGrid)

        #Image in center of screen
        self.centralLabel = QLabel(self)
        self.centralLabel.setScaledContents(True)
        self.centralLabel.setFixedSize(500, 500)
        self.mainGrid.addWidget(self.centralLabel)

        self.showMaximized()

    def setNewImage(self, imgPath):
        self.centralLabel.setPixmap(QPixmap(imgPath))
       