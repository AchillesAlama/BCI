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
