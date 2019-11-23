from PyQt5.QtWidgets import (QApplication, QAction, QLineEdit,
                            QLabel, QWidget, QMainWindow, QListWidget,
                           QGridLayout,QPushButton, QGroupBox,
                           QVBoxLayout, QToolButton, QHBoxLayout)

class TestingWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.initTesting()
        self.show()

        #Debugging data saving
        from controllers.dbController import DBController
        dbCon = DBController()
        mark = dbCon.makeUser("mark", "1995-02-09", "male", "spanish")
        mark.save()
        run = dbCon.makeRun(1, mark)
        run.save()
        self.channels = []
        for i in range(0,16):
            newChan = dbCon.makeChannel(i, "testPlacement"+str(i), "testUnit", run)
            newChan.save()
            self.channels.append(newChan)

        from utility.ultraCortexConnector import saveChannels
        saveChannels(self.channels)
        

    def initTesting(self):
        testGrid = QGridLayout()
        
        self.setLayout(testGrid)

    def test(self):
        self.title = 'BCI Hamburg Software v1.0'
        self.setWindowTitle(self.title)
