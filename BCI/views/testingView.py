from PyQt5.QtWidgets import (QWidget, QGridLayout)

class TestingWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.initTesting()

    def initTesting(self):
        testGrid = QGridLayout()
        
        self.setLayout(testGrid)

    def test(self):
        self.title = 'BCI Hamburg Software v1.0'
        self.setWindowTitle(self.title)
