from componants.main import *
from componants.live import *
from componants.training import *
from componants.testing import *

class mainController():

    def change_view(self, viewName):
        if viewName == "live_mode":
            self.setCentralWidget(liveWindow(self))
        elif viewName == "test_mode":
            self.setCentralWidget(testingWindow(self))
        elif viewName == "training_mode":
            self.setCentralWidget(trainingWindow(self))