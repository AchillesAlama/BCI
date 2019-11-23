from pyOpenBCI import OpenBCICyton
from functools import partial 
from controllers.dbController import DBController

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

def saveChannelsCallback(sample, channels, dbController):
    """ To be used as callback function in start_stream() to
    save each sample to DB
    """
    for i in range(0, 16):
        val = sample.channels_data[channels[i].Number]
        newMeas = dbController.makeMeasurement(val, sample.id, channels[i])
        newMeas.save()
    