from views.runView import RunView
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel, QMessageBox
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

        self.randImgSequence = self.getRandomImgSequence(4, 8) # Controls sequence of images
        countDown = 3 #Number to count down from
        self.countdown = [i for i in range(1, countDown+1)][::-1] #Countdown numbers list
        self.runSequence = self.countdown + self.randImgSequence #Iterate first through countdown then images
        self.imgFileNames = self.getImgFilePaths()
        self.currentIndex = 0 #Current position in the sequence list
        self.runInProgress = False #Flag true when pictures are showing
        self.startPictureLoop()

    def startPictureLoop(self):
        """Creates and starts a timer which triggers a function every second
        to iterate through the images to be shown."""
        self.imgChangeTimer = QTimer(self.view)
        self.imgChangeTimer.timeout.connect(self.setRandomPicture)
        self.imgChangeTimer.start(1000)

    def setRandomPicture(self):
        """Is called every second by timer. Sets the image in the central label
        to a random picture from the data/sets/ folder. Which picture is chosen
        is controlled by the class's "randImgSequence" attribute."""

        #During countdown just show the countdown numbers
        if (self.currentIndex < len(self.countdown)): 
            self.view.centralLabel.setText(str(self.runSequence[self.currentIndex]))
            self.currentIndex += 1
            return
        else:
            self.runInProgress = True

        #We stop run when sequence is done
        if (self.currentIndex == (len(self.runSequence))):
            self.stopRun()
            self.runInProgress = False
        else:
            #Use the next index in randImgSequence for picture choosing
            randImg = self.imgFileNames[self.runSequence[self.currentIndex]]
            self.currentIndex +=1 
            self.view.setNewImage(randImg)

    def stopRun(self):
        """Stops the timer and closes run window."""
        self.imgChangeTimer.stop()
        self.view.close()

    def getImgFilePaths(self):
        """Returns a list of names of the files to be iterated through"""
        imageDir = os.path.abspath("./data/sets/")

        #Find all file names
        f = []
        for (dirpath, dirnames, filenames) in walk(imageDir):
            f.extend(filenames)
            break

        #Add the directory name to get full path
        for i in range(len(f)):
            f[i] = imageDir + "\\" + f[i]
        
        #Return list of paths
        return f
                
    def getRandomImgSequence(self, numOfImages, seqLen):
        """Returns a sequence of indexes used for control of displayed pictures.
        Every image should be shown an equal amount of times and the same image
        should not be shown twice in a row.
        @numOfImages (int): number of different images shown 
        @seqLen (int): length of sequence
        
        @returns (list): list of length @seqLen with indexes"""

        if (seqLen % numOfImages != 0):
            raise Exception("seqLen needs to be multiple of numOfImages")

        sequences = []

        #Define base section with @numOfImages elements and only unique elements,
        #and use this as base for all sections which is just re-arranged versions
        #of this section.
        numOfSections = (int)(seqLen / numOfImages)
        baseSection = [i for i in range(numOfImages)]

        for s in range(numOfSections):
            baseCopy = baseSection[::]
            newSection = []
            for i in range(numOfImages):
                randChoice = random.choice(baseCopy)
                #First element cant be equal last element of last section
                while (i == 0 and s != 0 and randChoice == sequences[s*numOfImages + i -1]):
                    randChoice = random.choice(baseCopy)

                #Add the random index and remove it from possible choices
                newSection.append(randChoice)
                baseCopy.remove(newSection[i])
            
            #Save found section 
            sequences.extend(newSection)

        return sequences
         
    def escapePressed(self):
        """Triggers when user presses escape. Aborts the run and nothing is
        saved to DB."""
        self.stopRun()

        #Tell user that the run was interrupted 
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("The run was interrupted and no data was saved to the database.")
        msg.setWindowTitle("Run aborted")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()
        
