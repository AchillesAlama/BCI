from datetime import datetime
from models.dbModel import User, Channel, Run, Measurement
from orator import DatabaseManager, Model

class DBController():

    def __init__(self, parent=None):
        self.parent = parent
        
        #Configure DB
        self.config = {
                'mysql': {
                        'driver': 'mysql',
                        'host': 'localhost',
                        'database': 'mydb',
                        'user': 'root',
                        'password': 'beetroot',
                        'prefix': ''
                }
        }

        self.db = DatabaseManager(self.config)
        Model.set_connection_resolver(self.db)

    def makeUser(self, name, birthday, gender, nationality):
        return User(Name=name, Birthday=birthday, Gender=gender, Nationality=nationality)

    def makeChannel(self, number, placement, unit, run):
        newChannel = Channel()
        newChannel.Number = number
        newChannel.Placement = placement
        newChannel.Unit = unit
        newChannel.Run().associate(run)
        return newChannel

    def makeRun(self, type, user):
        newRun = Run()
        currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        newRun.Starttime = currentTime
        newRun.type=type
        newRun.User().associate(user) 
        return newRun
    
    def makeMeasurement(self, value, sampleNumber, channel):
        newMeasurement = Measurement()
        currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        newMeasurement.Timestamp = currentTime
        newMeasurement.Value = value
        newMeasurement.SampleNumber = sampleNumber
        newMeasurement.Channel().associate(channel)
        return newMeasurement

    def dummyDataGen(self):
        """ Creates a new user, new run, 16 channels and random data and 
        saves to DB. For filling DB with dummy data for debugging purposes.
        """
        # Make new user and run
        import random as r
        newUser = self.makeUser("DummyUser", "1881-01-01", "male", "north korean")
        newUser.save()
        newRun = self.makeRun(1, newUser)
        newRun.save()
        placements = ["fp1", "fp2", "c3", "c4", #Order matches numbers 1-16 in OpenBCI head plot
                      "t5", "t6", "o1", "o2", 
                      "f7", "f8", "f3", "f4", 
                      "t3", "t4", "p3", "p4"]
        channels = []

        #Make channels
        for i, place in enumerate(placements):
            newChan = self.makeChannel(i, place, "uV", newRun)
            newChan.save()
            channels.append(newChan)

        #Create measurements for each channel
        nMeasurements = 100
        for counter in range(0,nMeasurements):
            for chan in channels:
                newMeas = self.makeMeasurement(r.randrange(10000), counter, chan)
                newMeas.save()