from views.liveView import LiveWindow

class LiveController():

    def __init__(self, parent=None):
        self.controller = parent
        self.view = LiveWindow(parent = self)