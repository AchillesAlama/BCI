import sys
from PyQt5.QtWidgets import (QWidget, QGroupBox,QVBoxLayout,
QToolButton, QHBoxLayout)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QSize, Qt
from functools import partial

class MainWindow(QWidget):
    """First thing user sees when opening application,
    should be a choice between the possible modes of the application."""

    def __init__(self, parent=None): 
        super().__init__()
        self.parent = parent
        self.initUI()
        #self.show()

    def initUI(self):
        """Creates all user interface elements."""
        
        self.horizontalGroupBox = QGroupBox()
        grid = QHBoxLayout()

        #Create and add the 4 buttons
        btnFont = QFont('Helvetica', 16, 50)
        for mode in ['live_mode', 'training_mode', 'model_training_mode', 'test_mode']:
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
