from orator import DatabaseManager, Model
from orator.orm.utils import has_many, belongs_to 
from datetime import datetime

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
                        'password': '',
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
        currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        newMeasurement.Timestamp = currentTime
        newMeasurement.Value = value
        newMeasurement.SampleNumber = sampleNumber
        newMeasurement.Channel().associate(channel)
        return newMeasurement


########################################## MODEL DEFINITIONS (must reflect real DB) ############################################
class User(Model):
    __table__= 'User'
    __primary_key__ = 'User_ID'
    __timestamps__ = False
    __fillable__ = ['Name', 'Birthday', 'Gender', 'Nationality']
    @has_many('idUser', 'User_ID')
    def Runs(self):
        return Run

class Run(Model):
    __table__= 'Run'
    __primary_key__ = 'Run_ID'
    __timestamps__ = False
    __fillable__ = ['Starttime', 'Type']
    @has_many('idRun', 'Run_ID')
    def Channels(self):
        return Channel

    @belongs_to('idUser', 'User_ID')
    def User(self):
        return User

class Channel(Model):
    __table__= 'Channel'
    __primary_key__ = 'Channel_ID'
    __timestamps__ = False
    __fillable__ = ['Number', 'Placement', 'Unit']
    @has_many('idChannel', 'Channel_ID')
    def Measurements(self):
        return Measurement

<<<<<<< Updated upstream
    @belongs_to('idRun', 'Run_ID')
    def Run(self):
        return Run

class Measurement(Model):
    __table__= 'Measurement'
    __primary_key__ = 'Measurement_ID'
    __timestamps__ = False
    __fillable__ = ['Value', 'Timestamp', 'Samplenumber']

    @belongs_to('idChannel', 'Channel_ID')
    def Channel(self):
        return Channel
=======
    def deleteUser(self, userID):
        """Deletes user from database based on user ID.
        @userID (str): 
            ID of user to be deleted.
        """
        deletedRows = User.where('user_id', '=', userID).delete()
>>>>>>> Stashed changes
