from pyOpenBCI import OpenBCICyton
from functools import partial 
from controllers.dbController import DBController
from utility import infoDisplay as id

SCALE_FACTOR_EEG = (4500000)/24/(2**23-1) #uV/count

def connectToBoard():
    try:
        board = OpenBCICyton(daisy=True)
        return board
    except Exception:
        return None

def saveSampsToDict(board, samplesDict):
    """This function is responsible for saving the EEG samples during a run."""
    callback = partial(saveSampsToDictCallback, samplesDict=samplesDict)
    board.start_stream(callback)

def saveSampsToDictCallback(sample, samplesDict):
        """ To be used as callback function in start_stream() to
        save each sample to DB
        """
        for i in range(0, 16):
            val = sample.channels_data[i] * SCALE_FACTOR_EEG
            samplesDict[str(i)].append(val)

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
   



