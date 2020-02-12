from runView import RunView
from PyQt5.QtCore import QTimer, QThread
from PyQt5.QtWidgets import QLabel, QMessageBox, QPushButton, QApplication, QDialog, QProgressBar, QGridLayout
from PyQt5.QtGui import QGuiApplication
import os.path
from os import walk
from collections import OrderedDict
import random
from PyQt5.QtGui import QPixmap
from time import sleep
import numpy as np

from dbController import DBController
import utility.ultraCortexConnector as ucc
import utility.infoDisplay as id
from datetime import (datetime, timedelta)
import math

class RunController():
    """This class controls the window responsible for showing different images
    on screen whilst collecting EEG data."""

    def __init__(self, parent=None):
        self.controller = parent
        self.view = RunView(parent = self)

        self.randImgSequence = self.getRandomImgSequence(4, 16) # Controls sequence of images
        countDown = 3 #Number to count down from
        self.pictureLength = 1000 #Milliseconds to show each picture
        self.countdown = [i for i in range(1, countDown+1)][::-1] #Countdown numbers list
        self.runSequence = self.countdown + self.randImgSequence #Iterate first through countdown then images
        self.imgFileNames = self.getImgFilePaths()
        self.currentIndex = 0 #Current position in the sequence list
        self.runInProgress = False #Flag true when pictures are showing
        self.boardConnection = None
        self.samplesThread = None # QThread responsible for running the EEG stream
        self.samplesList = [] #List of OpenBCISamples, keeps track of all samples of run
        self.selectedUserId = self.controller.getCurrentUserData()['User_ID']

        #Timer triggers image changing
        self.imgChangeTimer = QTimer(self.view)
        self.imgChangeTimer.setInterval(self.pictureLength)
        self.imgChangeTimer.timeout.connect(self.timerRunFunction)

        #Starts run
        self.startRun()
        
    def startRun(self):
        #Connect to the board and start run
        self.view.centralLabel.setText("Connecting to board...")
        QApplication.processEvents()
        
        self.boardConnection = ucc.connectToBoard()
        
        if self.boardConnection:
            self.view.centralLabel.setText("Connected to board, starting run...")
            QApplication.processEvents()
            self.samplesThread = SampleSaveThread(self.boardConnection, self.samplesList)
            self.samplesThread.start() #Starting collection of samples
            
            #Wait until first samples are received, break if waited too long
            breakCntr = 0
            while not self.samplesThread.isStreamingStarted():
                if breakCntr >= 10:
                    msg = id.makeErrorPopup("Did not start receiving samples from device.")
                    msg.exec()
                    self.stopRun()
                    return
                else:
                    sleep(1)
                    breakCntr += 1

            #Start picture iteration
            self.imgChangeTimer.start()
            QApplication.processEvents()
        else:
            msg = id.makeErrorPopup("Could not connect to board.")
            msg.exec()
            self.stopRun()
        

    def timerRunFunction(self):
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
                
    def saveSamplesToDB(self):
        
        samplingRate = 250
        dbCon = DBController()

        #Here we assume the 'real' startime (UTC, not local) of the streaming has been set at the 
        #first call to the sample callback function. Starttime should be start of sampling,
        #not time of connection to board which is default
        startTime = datetime.strptime(self.boardConnection.start_time, "%Y-%m-%d_%H%M%S")
        
        #This makes sure all the saving is atomic
        with dbCon.db.transaction():
            #Get existing user, make new run, and save each samples
            currentUser = dbCon.getUser(self.selectedUserId)
            newRun = dbCon.makeRun(1, currentUser)
            newRun.save()

            #Make the 16 channels
            placements = ucc.getNumberPlacementTuples()

            print("About to create %d samples" % (len(self.samplesList)*16))

            #Create popup showing progressbar of data saving
            measCntr = 0
            progWin = SaveDBProgressBar(len(self.samplesList))
            chanItList = range(16)

            #Create channel names to match fields in DB
            channelQueryStr = ", ".join(["Channel" + str(i) + "_val" for i in range(1, 17)])
            baseQuery = "insert into sample (Timestamp, SampleNumber, idRun, " + channelQueryStr + ") values (\"%s\", %d, %d, " + "%d, "*15 + "%d)"

            #Adjust the ids (problem described in adjustIDs description)
            self.adjustSampleIDs(self.samplesList)

            #Generate "synthetic" timestamps of samples using sampleNums, samplerate and starttime,
            #we assume starttime is the time when the sampling starts
            for sample in self.samplesList:
                timeDelta = timedelta(microseconds = sample.id*1000000.0/samplingRate) #time since start
                timestamp = (startTime + timeDelta).strftime("%Y-%m-%d %H:%M:%S.%f")
                
                #Build tuple to match baseQuery for value insertion into string
                valueTuple = (timestamp, sample.id, newRun.Run_ID)
                for i in range(16):
                    valueTuple += (sample.channels_data[i], )

                
                dbCon.db.statement(baseQuery % valueTuple)
                    
                measCntr += 1
                progWin.update(measCntr)
                QApplication.processEvents()
                        
                #roll back transaction if user chooses to cancel
                if progWin.stopFlag == True:
                    dbCon.db.rollback()
                    return
            
            progWin.stop()
    
    def adjustSampleIDs(self, sampleList):
        """Problem: the ids of samples in a stream are not unique but simply goes 
        between 1-255 and starts over at 1 again and again. This is problematic
        for our synthetic timestamp creation. This function goes through the 
        completed list of samples and corrects the Ids to an ever increasing 
        sequence.
        @sampleList (list of OpenBCISamples): completed list of samples for a run.
        """

        cntr = 0;
        for i in range(len(sampleList)):
            #if id is smaller than last id, increase cntr 
            #(adjust for last sample already having been increased)
            if i > 0 and sampleList[i].id < (sampleList[i-1].id - cntr*256):
                cntr +=1
            
            sampleList[i].id += cntr*256


    def stopRun(self):
        """Stops the timer, closes connection to board and closes run window."""
        self.imgChangeTimer.stop()

        if self.boardConnection:
            #The sleeps in between seem to be important
            self.boardConnection.stop_stream()
            sleep(0.5)
            self.boardConnection.write_command('v') #soft reset of the board
            sleep(0.5)
            
            #We rely on the runController (and hence self.boardConnection) 
            #being destroyed at end of this function, since the destruction
            #should trigger a disconnect from the board (see init function of
            #OpenBCICyton). Using the board's disconnect function directly 
            #sometimes triggers a crash, cause yet unknown.
            
        if self.samplesThread:
            self.samplesThread.quit()
            msg = id.makeYesNoPopup("Run successfully completed. Do you want to save samples to database?")
            retval = msg.exec()
            if retval == QMessageBox.Yes:
                self.saveSamplesToDB()

        #Each run will instantiate a new run controller, less error prone than
        #manual maintenence of vars
        self.view.close()
        del self 

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
        
class SampleSaveThread(QThread):
    """This thread is responsible for starting the streaming of the EEG samples.
    This way we can receive samples at the same time as we are iterating through
    the images in the run."""
    def __init__(self, boardConnection, samplesList):
        QThread.__init__(self)
        self.boardConnection = boardConnection
        self.samplesList = samplesList

    def run(self):
        ucc.saveSampsToList(self.boardConnection, self.samplesList)

    def isStreamingStarted(self):
        """Returns true if the first samples have been received."""
        return len(self.samplesList) > 0

class SaveDBProgressBar(QDialog):
    """
    Simple dialog that shows how much data is saved to database so far.
    """
    def __init__(self, maxVal):
        super().__init__()
        self.maxVal = maxVal
        self.stopFlag = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Progress Bar')
        self.label = QLabel("Saving new samples to database:")
        self.progress = QProgressBar(self)
        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.stop)
        self.progress.setGeometry(0, 0, 300, 25)
        self.progress.setMaximum(self.maxVal)
        grid = QGridLayout()
        grid.addWidget(self.label, 0, 0)
        grid.addWidget(self.progress, 1, 0)
        grid.addWidget(self.cancelBtn, 2, 0)
        self.setLayout(grid)
        self.show()

    def stop(self):
        self.stopFlag = True

    def update(self, val):
        self.progress.setValue(val)
       