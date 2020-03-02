from dbController import DBController
from views.mlView import MLView 

class MLController():

    def __init__(self, parent=None):
        self.controller = parent
        self.view = MLView(self)

    def getSamplesForUser(self, userID):
        """Gets all the samples related to a certain user and returns a nested
        on the form {runId1: 
                        {event1: 
                            {filename: (e.g.) 'top.png'},
                                window1: [sample1, sample2...],
                                ...
                                window4: [sample1, sample2...]},
                             
                            event2: 
                            {filename: (e.g.) 'bottom.png'},
                                window1: [sample1, sample2...],
                                ...
                                window4: [sample1, sample2...]},         
                        runId2:...   
                        }.
                        
            Each sample is a list with EEG values for channels 1-16, e.g. channel 1 data would
            be obtainable by sample1[0]. Filenames does not include path.
            """
        dbCon = DBController()
        rawFromDB = dbCon.getAllUserSamples(userID)