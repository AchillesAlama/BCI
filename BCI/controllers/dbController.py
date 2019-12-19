from datetime import datetime, timedelta
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

    def dummyDataGen(self, username):
        """ Creates a new user, new run, 16 channels and random data and 
        saves to DB. For filling DB with dummy data for debugging purposes.
        """
        # Make new user and run
        import random as r

        #get random date between two dates
        start = datetime(1990, 1, 1, 0, 0, 0)
        end = datetime.now()
        birth = start + timedelta(seconds=r.randint(0, int((end - start).total_seconds())))
        birth = birth.date()

        #random male or female
        gender = "male" if r.randint(0, 1) == 0 else "female"

        #nationality 
        nations = ["english", "american", "bulgarian", "spanish", "french", "german", "swedish", "danish", "norwegian"]
        nationality = nations[r.randint(0, len(nations)-1)]

        #make user
        newUser = self.makeUser(username, birth, gender, nationality)
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

    def getUserSamples(self, user, testType):
        """Returns all time samples for a certain user for a certain test type.
        @user (string):     
            User for which to find samples
        @testType (int): 
            Integer code for which kind of training mode was used when 
            gathering the data.
        @return (dict): 
            Dict with arrays of dicts, 
            on the form {channel 1: [{value: ..., timestamp: ...}],
                         channel 2: [...]}. 
            Each channel sorted by timestamp.
        """
        resultDict = {}
        for i in range(1, 16):
            userSampleQuery = """select measurement.Value, measurement.Timestamp from 
measurement join channel on channel.channel_id = measurement.idChannel
join Run on run.run_id = channel.idRun
join User on user.user_id = run.idUser
where channel.Number = %d and 
user.name = "%s" and 
run.type = %d 
order by measurement.timestamp""" % (i, user, testType)
            resultDict["channel " + str(i)] = self.db.select(userSampleQuery)
        
        return resultDict