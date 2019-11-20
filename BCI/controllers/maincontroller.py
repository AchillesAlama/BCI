from views.mainView import MainWindow
from views.liveView import LiveWindow
from views.trainingView import TrainingWindow
from views.testingView import TestingWindow

class MainController():
    def __init__(self, parent=None):
        self.parent = parent
        self.view = MainWindow(parent=self)

    def change_view(self, viewName):
        if viewName == "live_mode":
            self.parent.setCentralWidget(LiveWindow(self))
        elif viewName == "test_mode":
            self.parent.setCentralWidget(TestingWindow(self))
        elif viewName == "training_mode":
            self.parent.setCentralWidget(TrainingWindow(self))