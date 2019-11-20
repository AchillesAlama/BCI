from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSize, QThread, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtWidgets
import xml.etree.ElementTree as ET
import os
from shutil import copyfile, rmtree
from time import sleep
import random
from views.startNewTest import startNewTestGUI 

class TrainingController():

    def saveSubject(subjectName,subjectBirthday,subjectGender,subjectNationality):
        n = subjectName.text()
        b = subjectBirthday.text()
        g = subjectGender.text()
        c = subjectNationality.text()

        with open('test.txt', 'w') as f:
            f.write("Name: " + n + "    ")
            f.write("Birthday: " + b + "    ")
            f.write("Gender: " + g + "    ")
            f.write("Nationality: " + c + "\n")

        subjectName.setText("")
        subjectBirthday.setText("")
        subjectGender.setText("")
        subjectNationality.setText("")

    def startNewTest(self):
        self.w = startNewTestGUI()
        self.w.setWindowState(Qt.WindowMaximized)
        self.w.show()

    def pathFinder(self):
        path1 = os.path.dirname(os.path.abspath(__file__))
        path2 = os.path.split(path1)
        path = os.path.join(path2[0],"data\\sets\\")
        return path

    def scanFolder(self,path):
        fileNames = os.listdir(path)
        return fileNames

    def timer():
        sleep(5)
        return True

    def timeStamp(self):
        timestamp = QDateTime.currentDateTime()