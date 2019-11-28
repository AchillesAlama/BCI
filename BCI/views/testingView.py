from PyQt5.QtWidgets import (QApplication, QAction, QLineEdit,
                            QLabel, QWidget, QMainWindow, QListWidget,
                           QGridLayout,QPushButton, QGroupBox,
                           QVBoxLayout, QToolButton, QHBoxLayout)

class TestingWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.initTesting()
        self.show()

    def initTesting(self):
        testGrid = QGridLayout()
        
        self.setLayout(testGrid)

    def test(self):
        self.title = 'BCI Hamburg Software v1.0'
        self.setWindowTitle(self.title)
