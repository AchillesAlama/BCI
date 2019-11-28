from orator import DatabaseManager, Model
from orator.orm.utils import has_many, belongs_to 
from datetime import datetime
import models.dbModel

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
        currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        newMeasurement.Timestamp = currentTime
        newMeasurement.Value = value
        newMeasurement.SampleNumber = sampleNumber
        newMeasurement.Channel().associate(channel)
        return newMeasurement


