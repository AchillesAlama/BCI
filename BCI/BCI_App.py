from PyQt5.QtWidgets import (QApplication, QAction,
QMainWindow, QStackedWidget)

from controllers.mainController import MainController
import sys
from functools import partial

import utility.ultraCortexConnector as ucon

class App(QMainWindow):

    def __init__(self):
        #Init window params
        super().__init__()
        self.title = 'BCI Hamburg Software v1.0'
        self.setWindowTitle(self.title)

        #Create the main controller of this application(mostly switches modes)
        self.controller = MainController(parent=self)

        #Add all elements who will take up main window to stacked widget
        #in order to switch between views without having to recreate
        #them each time
        self.mainSpace = QStackedWidget()
        self.setCentralWidget(self.mainSpace)
        self.mainSpace.addWidget(self.controller.view)
        self.mainSpace.addWidget(self.controller.trainingController.view)
        self.mainSpace.addWidget(self.controller.testingController.view)
        self.mainSpace.addWidget(self.controller.liveController.view)
        self.mainSpace.addWidget(self.controller.mlController.view)
        self.mainSpace.setCurrentWidget(self.controller.view)
        self.adjustSize() #TODO: QStackedWidget sizes to biggest of its widgets, keep or change?

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
