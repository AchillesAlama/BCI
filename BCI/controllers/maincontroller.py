from views.mainView import MainWindow
from controllers.liveController import LiveController
from controllers.trainingController import TrainingController
from controllers.testingController import TestingController
from controllers.mlController import MLController

class MainController():
    def __init__(self, parent=None):
        self.parent = parent
        self.view = MainWindow(parent=self)
        self.trainingController = TrainingController(self)
        self.liveController = LiveController(self)
        self.testingController = TestingController(self)
        self.mlController = MLController(self)

    def change_view(self, viewName):
        if viewName == "live_mode":
            self.parent.mainSpace.setCurrentWidget(self.liveController.view)
        elif viewName == "test_mode":
            self.parent.mainSpace.setCurrentWidget(self.testingController.view)
        elif viewName == "training_mode":
            self.parent.mainSpace.setCurrentWidget(self.trainingController.view)
        elif viewName == "model_training_mode":
            self.parent.mainSpace.setCurrentWidget(self.mlController.view)
        
        