from datetime import datetime, timedelta
from pyOpenBCI import OpenBCICyton
from models.dbModel import User, Run, Sample, Encoding
from orator import DatabaseManager, Model
from utility import infoDisplay as id
from utility import ultraCortexConnector as ucc
from datetime import timezone

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
        currentTime = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        newRun.Starttime = currentTime
        newRun.type=type
        newRun.User().associate(user) 
        return newRun
    
    def makeEncoding(self, code ,fileName):
        """Creates and returns a new encoding object to be saved, or returns a ref to
        an existing such object if an encoding with such attributes already exists.
      
        @code (int): Encoding of the file.
        @fileName (string): Name of the file.s
        @returns (Encoding object): object to be saved to database with .save().
        """
        newEncoding = Encoding.first_or_create(code=code, filename=fileName)
        return newEncoding

    def makeSample(self, sampleNumber, channelVals, timestamp, run, encoding):
        """Creates and returns a new Sample object to be saved.
        
        @sampleNumber (int): Should correspond to the id sent with every sample
            from the board.
        @channelVals (list): Array with the values for each sample. Value
            at index 0 should be the value for channel 1 and so on.
        @timestamp (datestring on format "%Y-%m-%d %H:%M:%S"): time at which 
            sample was taken, UTC time.
        @run (Run object): As returned by makeRun for example, the run that 
            owns this sample.
        @encoding(Encoding object): as returned by makeEncoding, the encoding
            showing which img was shown during this sample.
        @returns (Sample object): a new sample to be saved to DB. 
        """
        newSample = Sample()
        newSample.Timestamp = timestamp

        for i in range(1, 17):
            eval("newSample.Channel" + i + "_val = " + str(channelVals[i]))

        newSample.SampleNumber = sampleNumber
        newSample.Run().associate(run)
        newSample.Encoding().associate(encoding)
        return newSample


    def getUser(self, id):
        """Returns an actual User object, not simple dictionary with info"""
        return User.first_or_create(User_ID = id)

    def getAllUsers(self):
        """Returns a list of dicts with info of all users in DB"""
        userQuery = "select * from user"
        return self.db.select(userQuery)

    def getAllUserSamples(self, userID):
        """Returns a list of dictionaries filled with information about
        the EEG values from all runs made by a certain user."""
        
        query = ("select Run_ID, SampleNumber, filename, Channel1_val, Channel2_val,"+
                "Channel3_val, Channel4_val, Channel5_val Channel6_val,"+
                "Channel7_val, Channel8_val, Channel9_val, Channel10_val, Channel11_val,"+
                "Channel12_val, Channel13_val, Channel14_val, Channel15_val, Channel16_val "+
                "from user join run "+
                "on run.idUser = user.User_ID join "+
                "sample on sample.idRun = run.Run_ID join "+
                "encoding on encoding.Encoding_ID = sample.idEncoding "+
                "where user.User_ID = %d;" % userID)

        return self.db.select(query)

    def deleteUser(self, userID):
        """Deletes user from database based on user ID.
        @userID (str): 
            ID of user to be deleted.
        """
        deletedRows = User.where('user_id', '=', userID).delete()
        
