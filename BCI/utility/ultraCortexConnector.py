from pyOpenBCI import OpenBCICyton
from functools import partial 
<<<<<<< Updated upstream
from controllers.dbController import DBController
=======
from dbController import DBController
from utility import infoDisplay as id
import datetime
import csv

SCALE_FACTOR_EEG = (4500000)/24/(2**23-1) #uV/count

def connectToBoard():
    try:
        board = OpenBCICyton(daisy=True)
        return board
    except Exception as e:
        print(e)
        return None

def saveSampsToList(board, samplesList):
    """This function is responsible for saving the EEG samples during a run."""
    callback = partial(saveSampsToListCallback, samplesList=samplesList, boardCon = board)
    board.start_stream(callback)

def saveSampsToListCallback(sample, samplesList, boardCon):
        """ To be used as callback function in start_stream() to
        save each sample to DB

        @samplesList (list of OpenBciSamples): All the samples of a run.
        @boardCon (OpenBCICyton object): repreysents the connection to the board. 
        """
        #Set (UTC, not local) start time first time (important! default start time is set to
        #the time a connection to the board was made, but for our synthetic generation
        #of timestamps the start time needs to be the time the sampling starts)
        if len(samplesList) == 0:
            boardCon.start_time = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H%M%S")
        
        samplesList.append(sample)
>>>>>>> Stashed changes

def printChannel(channelNum):
    board = OpenBCICyton(daisy=True)
    callback = partial(printSampleCallback, channelNum=channelNum)
    board.start_stream(callback)

def printChannelsCallback(sample, channelNum):
    """ To be used as callback function in start_stream() to
    save each sample to DB
    """
    print(sample.channels_data[channelNum])
   
def saveChannels(channels):
    board = OpenBCICyton(daisy=True)
    dbCon = DBController()
    callback = partial(saveChannelsCallback, channels=channels, dbController=dbCon)
    board.start_stream(callback)

<<<<<<< Updated upstream
def saveChannelsCallback(sample, channels, dbController):
    """ To be used as callback function in start_stream() to
    save each sample to DB
    """
    for i in range(0, 16):
        val = sample.channels_data[channels[i].Number]
        newMeas = dbController.makeMeasurement(val, sample.id, channels[i])
        newMeas.save()
    
=======
    tupleList = []
    for i in range(1, 17): #range does not include upper limit
        tupleList.append((i, placements[i-1]))
    return tupleList

def saveLiveSampsToList(board, x, writer):
    """This function is responsible for getting the EEG samples
    during a live run."""
    callback = partial(updatePlot, x = x, writer = writer)
    board.start_stream(callback)

def updatePlot(sample, x, writer):
    """This method makes sure that the maximun number of values
    displayed is X and starts removing elemnts if it's full."""
    #if (len(x) < 500):
    #    x.append(sample)
    #else:
    #    x.pop(0)
    #    x.append(sample)
    
    writer.writerow(sample.channels_data[0], sample.channels_data[1], sample.channels_data[2])
>>>>>>> Stashed changes
