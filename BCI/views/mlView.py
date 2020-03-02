from PyQt5.QtWidgets import (QWidget)

class MLView(QWidget):

    def __init__(self, parent = None):
        super().__init__()
        self.controller = parent