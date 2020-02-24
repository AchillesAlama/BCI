from orator import Model
from orator.orm.utils import has_many, belongs_to 

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
    def Samples(self):
        return Sample

    @has_many('idRun', 'Run_ID')
    def Events(self):
        return Event

    @belongs_to('idUser', 'User_ID')
    def User(self):
        return User

class Encoding(Model):
    __table__= 'Encoding'
    __primary_key__ = 'Encoding_ID'
    __timestamps__ = False
    __fillable__ = ['code', 'filename']


class Sample(Model):
    __table__= 'Sample'
    __primary_key__ = 'Sample_ID'
    __timestamps__ = False
    fillableList = ['Timestamp', 'Samplenumber']
    fillableList.append(["Channel"+ str(i) + "_val" for i in range(1, 17)])
    __fillable__ = fillableList

    @belongs_to('idRun', 'Run_ID')
    def Run(self):
        return Run

    @belongs_to('idEncoding', 'Encoding_ID')
    def Encoding(self):
        return Encoding
