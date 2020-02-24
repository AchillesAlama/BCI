from pyOpenBCI import OpenBCICyton

from functools import partial 
from dbController import DBController
from utility import infoDisplay as id
import datetime
from datetime import timezone

SCALE_FACTOR_EEG = (4500000)/24/(2**23-1) #uV/count

DEBUG_TIME = None

def connectToBoard():
    try:
        board = OpenBCICyton(daisy=True)
        return board
    except Exception as e:
        print(e)
        return None

def saveSampsForRun(board, samplesList, pauseFlag):
   
    """This function is responsible for saving the EEG samples during a run."""
    callback = partial(saveSampsForRunCallback, samplesList=samplesList, 
                       boardCon = board, pause=pauseFlag)
    board.start_stream(callback)

def saveSampsForRunCallback(sample, samplesList, boardCon, pause):
        
        """ To be used as callback function in start_stream() to
        save each sample to DB

        @samplesList (list of OpenBciSamples): All the samples of a run.
        @boardCon (OpenBCICyton object): repreysents the connection to the board. 
        @pause (bool): used to ignore certain samples
        """
        
        if (not pause):
            samplesList.append(sample)

def printChannel(channelNum):
    try:
        board = OpenBCICyton(daisy=True)
    except Exception as e:
        id.makeErrorPopup(str(e))
        return

    callback = partial(printChannelsCallback, channelNum=channelNum)
    board.start_stream(callback)

def printChannelsCallback(sample, channelNum):
    """ To be used as callback function in start_stream() to
    save each sample to DB
    """
    print(sample.channels_data[channelNum-1])
   
def getNumberPlacementTuples():
    """Returns a list of tuples which connects a channel numbers
    to a position as according to the international 10/20 system
    of EEG sensor placement."""
    
    placements = ["fp1", "fp2", "c3", "c4", #Order matches numbers 1-16 in OpenBCI head plot
                    "t5", "t6", "o1", "o2", 
                    "f7", "f8", "f3", "f4", 
                    "t3", "t4", "p3", "p4"]

    tupleList = []
    for i in range(1, 17): #range does not include upper limit
        tupleList.append((i, placements[i-1]))
    return tupleList
