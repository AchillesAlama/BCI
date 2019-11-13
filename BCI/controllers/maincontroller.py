from views.main import *
from views.live import *
from views.training import *
from views.testing import *

class mainController():

    def change_view(self, viewName):
        if viewName == "live_mode":
            self.setCentralWidget(liveWindow(self))
        elif viewName == "test_mode":
            self.setCentralWidget(testingWindow(self))
        elif viewName == "training_mode":
            self.setCentralWidget(trainingWindow(self))