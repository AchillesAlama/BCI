from views.mainView import *
from views.liveView import *
from views.trainingView import *
from views.testingView import *

class MainController():
    def __init__(self, parent=None):
        self.parent = parent
        self.view = MainWindow(parent=self)

    def change_view(self, viewName):
        if viewName == "live_mode":
            self.parent.setCentralWidget(liveWindow(self))
        elif viewName == "test_mode":
            self.parent.setCentralWidget(testingWindow(self))
        elif viewName == "training_mode":
            self.parent.setCentralWidget(trainingWindow(self))