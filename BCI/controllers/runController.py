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
import ntpath
from datetime import timezone

import utility.encoder as enc
from dbController import DBController
import utility.ultraCortexConnector as ucc
import utility.infoDisplay as id
from datetime import (datetime, timedelta)
import math
import utility.helpers

class RunController():
    """This class controls the window responsible for showing different images
    on screen whilst collecting EEG data."""

    def __init__(self, parent=None):
        self.controller = parent
        self.view = RunView(parent = self)

        self.randImgSequence = self.getRandomImgSequence(4, 16) # Controls sequence of images
        countDown = 3 #Number to count down from
        self.pictureLength = 4000 #Milliseconds to show each picture
        self.countdown = [i for i in range(1, countDown+1)][::-1] #Countdown numbers list
        self.runSequence = self.countdown + self.randImgSequence #Iterate first through countdown then images
        self.imgFileNames = self.getImgFilePaths() #filenames of imgs, indirectly controls encodings
        self.encodings = self.getImgEncodings() 
        self.currentIndex = 0 #Current position in the sequence list
        self.runInProgress = False #Flag true when pictures are showing
        self.boardConnection = None
        self.encoderConnection = None
        self.samplesThread = None # QThread responsible for running the EEG stream
        self.samplesList = [] #List of OpenBCISamples, keeps track of all samples of run
        self.eventList = [] #Saves all event info during the run, to be saved as Events in DB after run 
        self.selectedUserId = self.controller.getCurrentUserData()['User_ID']

        #Timer triggers image changing
        self.imgChangeTimer = QTimer(self.view)
        self.imgChangeTimer.setInterval(self.pictureLength)
        self.imgChangeTimer.timeout.connect(self.timerRunFunction)

        #Starts run
        self.startRun()
        
    def startRun(self):
        #Connect to encoder
        self.view.centralLabel.setText("Connecting to encoder...")
        QApplication.processEvents()
        self.encoderConnection = enc.connectToEncoder()

        if (not self.encoderConnection):
            msg = id.makeErrorPopup("Could not connect to encoder.")
            msg.exec()
            self.stopRun()
        else:
            enc.clearEncoding(self.encoderConnection)

        #Connect to the board
        self.view.centralLabel.setText("Connecting to board...")
        QApplication.processEvents()
        
        #Connect to board
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
            #self.imgChangeTimer.setInterval(4000)

        #We stop run when sequence is done
        if (self.currentIndex == (len(self.runSequence))):
            self.stopRun()
            self.runInProgress = False
            
        else:
            #Use the next index in randImgSequence for picture choosing
            randImg = self.imgFileNames[self.runSequence[self.currentIndex]]
            self.currentIndex +=1 
            timeOfEvent = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
            
            #Mark end of img
            enc.clearEncoding(self.encoderConnection)
            sleep(0.200) #acts as padding at end of every img to make sure we get some zeros

            #Change img
            self.view.setNewImage(randImg)

            #Trigger new encoding (all new samples coming in with new encoding
            #MUST have been taken after img change as long as these two functions
            #never change order)
            enc.setEncoding(self.encoderConnection, self.encodings[randImg])

            #restarts timer to make sure we have enough time to gather samples
            self.imgChangeTimer.start() 

                
    def saveSamplesToDB(self):
        
        samplingRate = 250
        dbCon = DBController()
        
        #This makes sure all the saving is atomic
        with dbCon.db.transaction():
            #Create the run and connect to user
            currentUser = dbCon.getUser(self.selectedUserId)
            newRun = dbCon.makeRun(1, currentUser)
            newRun.save()

            #Create the encodings used in this run
            encodings = []
            for filename, encoding in self.encodings.items():
                encodings.append(dbCon.makeEncoding(code=encoding, fileName=filename))

            for encoding in encodings:
                encoding.save()

            print("About to create %d samples" % (len(self.samplesList)*16))

            #Create popup showing progressbar of data saving
            measCntr = 0
            progWin = SaveDBProgressBar(len(self.samplesList))
            chanItList = range(16)

            #Create channel names to match fields in DB
            channelQueryStr = ", ".join(["Channel" + str(i) + "_val" for i in range(1, 17)])
            baseQuery = "insert into sample (SampleNumber, idRun, idEncoding, " + channelQueryStr + ") values (\"%s\", %d, %d, " + "%d, "*15 + "%d)"

            #Adjust the ids (problem described in adjustIDs description)
            self.adjustSampleIDs(self.samplesList)

            for sample in self.samplesList:
                #Find the encoding object which should be connected to this sample
                enc = list(filter(lambda x: x.code == int(sample.aux_data[0]) ,encodings))[0]
                
                #Build tuple to match baseQuery for value insertion into string
                valueTuple = (sample.id, newRun.Run_ID, enc.Encoding_ID, )
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

        if self.encoderConnection:
            enc.closeEncoder(self.encoderConnection)

        if self.boardConnection:
            #The sleeps in between seem to be important
            self.boardConnection.stop_stream()
            sleep(0.5)
            self.boardConnection.write_command('v') #soft reset of the board
            sleep(0.5)
            self.boardConnection.disconnect()
            sleep(0.5)
            
        if self.samplesThread and self.boardConnection:
            self.samplesThread.quit()

            #Clean the samples
            self.samplesList = self.cleanSamplesByEncoding(self.samplesList)
            self.samplesList = self.removeMarginSamples(self.samplesList)

            for sample in self.samplesList:
                print(int(sample.aux_data[0]))

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
         
    def getImgEncodings(self):
        """Returns a dictionary of tuples with the key being the image file name
        and the value being the corresponding encoding. Note that 0 is invalid encoding.
        """

        out = {}
        for i, img in enumerate(self.imgFileNames):
            out[img] = i+1
        return out

    def removeMarginSamples(self, samplesList):
        """At end of every img shown there should be some zeros inserted to
        clearly mark the end of the event. This function removes all these zero samples.
        The zero samples were introduced to mark exactly which samples from the end
        can be deleted, so no end samples actually belong to the following img."""

        return list(filter(lambda x: int(x.aux_data[0]) != 0, samplesList))

    def cleanSamplesByEncoding(self, samplesList):
        """Sometimes the Cyton board catches middle values between valid encodings.
        So between e.g. encodings 1 and 3 (img changes from 1 to 3) there might
        be a few samples with encoding 2 for example. This probably comes from 
        the encoder not changing the pin values fast enough compared to the Cyton
        sampling rate. This function finds and removes these middle values."""
        
        cntr = 0 # counts number of new encodings after a change
        tolerance = 10 #min num. of samples in a row needing the same encoding not to be deleted

        currentEncoding = oldEncoding = int(samplesList[0].aux_data[0])
        for i in range(len(samplesList)):
            currentEncoding = int(samplesList[i].aux_data[0])
            
            if currentEncoding != oldEncoding:
                #streak broken, if less than tolerance mark sample for later deletion
                if cntr <= tolerance:
                    for j in range(1,cntr+1):
                        samplesList[i-j].aux_data[0] = 255
                
                oldEncoding = currentEncoding 
                cntr = 1 #first new encoding
                
            else:
                cntr += 1 # streak continues

        #We avoided deletion in previous loop since that would change the length
        #of the list we are iterating through. Now we return a filtered list
        #based on the markings.

        return list(filter(lambda x: int(x.aux_data[0]) != 255 ,samplesList))


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
        self.pauseFlag = False

    def pause(self):
        """Doesn't actually pause anything, just makes the sample callback
        ignore samples for a while."""
        self.pauseFlag = True

    def unpause(self):
        self.pauseFlag = False

    def run(self):
        ucc.saveSampsForRun(self.boardConnection, self.samplesList, self.pauseFlag)

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
       