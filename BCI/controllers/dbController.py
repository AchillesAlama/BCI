from datetime import datetime, timedelta
from pyOpenBCI import OpenBCICyton
from models.dbModel import User, Run, Sample
from orator import DatabaseManager, Model
from utility import infoDisplay as id
from utility import ultraCortexConnector as ucc

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

    def makeRun(self, type, user):
        newRun = Run()
        currentTime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        newRun.Starttime = currentTime
        newRun.type=type
        newRun.User().associate(user) 
        return newRun
    
    def makeSample(self, sampleNumber, channelVals, timestamp, run):
        """Creates and returns a new Sample object to be saved.
        
        @sampleNumber (int): Should correspond to the id sent with every sample
            from the board.
        @channelVals (list): Array with the values for each sample. Value
            at index 0 should be the value for channel 1 and so on.
        @timestamp (datestring on format "%Y-%m-%d %H:%M:%S"): time at witch 
            sample was taken, UTC time.
        @run (Run object): As returned by makeRun for example, the run that 
            owns this sample.
        @returns (Sample object): a new sample to be saved to DB. 
        """
        newSample = Sample()
        newSample.Timestamp = timestamp

        for i in range(1, 17):
            eval("newSample.Channel" + i + "_val = " + str(channelVals[i]))

        newSample.SampleNumber = sampleNumber
        newSample.Run().associate(run)
        return newSample


    def getUser(self, id):
        """Returns an actual model object of User, not simple dictionary with info"""
        return User.first_or_create(User_ID = id)

    def getAllUsers(self):
        """Returns a list of dicts with info of all users in DB"""
        userQuery = "select * from user"
        return self.db.select(userQuery)

    def deleteUser(self, userID):
        """Deletes user from database based on user ID.
        @userID (str): 
            ID of user to be deleted.
        """
        deletedRows = User.where('user_id', '=', userID).delete()
        
