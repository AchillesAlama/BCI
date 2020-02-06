from views.runView import RunView
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QGuiApplication
import os.path
from os import walk
import random
from PyQt5.QtGui import QPixmap

class RunController():
    """This class controls the window responsible for showing different images
    on screen whilst collecting EEG data."""

    def __init__(self, parent=None):
        self.controller = parent
        self.view = RunView(parent = self)
        self.startPictureLoop()
        self.imgChangeTimer = None

    def startPictureLoop(self):
        self.imgChangeTimer = QTimer(self.view)
        self.imgChangeTimer.timeout.connect(self.setRandomPicture)
        self.imgChangeTimer.start(1000)

    def setRandomPicture(self):
        randImg = self.chooseRandomPicture()
        self.view.setNewImage(randImg)
        
        print(randImg)
        

    def chooseRandomPicture(self):
        """Returns the absolute path of a randomly chosen file in data/sets/."""
        imageDir = os.path.abspath("./data/sets/")

        #Find all file names
        f = []
        for (dirpath, dirnames, filenames) in walk(imageDir):
            f.extend(filenames)
            break

        #Return random element
        return imageDir + "\\" + random.choice(f)