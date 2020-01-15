import sys
from PyQt5.QtWidgets import (QApplication, QAction, QWidget,
QMainWindow, QGridLayout,QPushButton, QGroupBox,QVBoxLayout,
QToolButton, QHBoxLayout, QMenuBar)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import pyqtSlot, QSize, Qt
from functools import partial

class MainWindow(QWidget):
    """First thing user sees when opening application,
    should be a choice between the possible modes of the application."""

    def __init__(self, parent=None): 
        super().__init__()
        self.parent = parent
        self.initUI()
        self.show()

    def initUI(self):
        """Creates all user interface elements."""
        
        self.horizontalGroupBox = QGroupBox()
        grid = QHBoxLayout()

        #Create and add the 3 buttons
        btnFont = QFont('Helvetica', 16, 50)
        for mode in ['live_mode', 'training_mode', 'test_mode']:
            modeBtn = QToolButton(self)
            modeBtn.setText(mode.replace("_", " ").title())
            modeBtn.setIcon(QIcon(QPixmap('images/'+ mode)))
            modeBtn.setIconSize(QSize(200, 200))
            modeBtn.setFont(btnFont)
            modeBtn.clicked.connect(partial(self.parent.change_view, mode))
            modeBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            grid.addWidget(modeBtn)
  
        self.horizontalGroupBox.setLayout(grid)
        self.windowLayout = QVBoxLayout()
        self.windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(self.windowLayout)
