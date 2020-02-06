from views.testingView import TestingWindow

class TestingController():

    def __init__(self, parent=None):
        self.controller = parent
        self.view = TestingWindow(parent = self)