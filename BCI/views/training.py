from PyQt5.QtWidgets import (QApplication, QAction, QLineEdit,
                            QLabel, QWidget, QMainWindow, QListWidget,
                           QGridLayout,QPushButton, QGroupBox,
                           QVBoxLayout, QToolButton, QHBoxLayout)
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, QThread, Qt
from PyQt5.QtGui import QIcon, QPixmap
from controllers.trainingcontroller import trainingController

class trainingWindow(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.initTraining()
        self.show()

    def initTraining(self):
        grid = QGridLayout()
        
        windowExample = QtWidgets.QWidget()
        labelSubject = QtWidgets.QLabel(windowExample)
        labelSubject.setText('Name: ')
        labelBirthday = QtWidgets.QLabel(windowExample)
        labelBirthday.setText('Birthday: ')
        labelGender = QtWidgets.QLabel(windowExample)
        labelGender.setText('Gender: ')
        labelNationality = QtWidgets.QLabel(windowExample)
        labelNationality.setText('Nationality: ')

        subjectName = QLineEdit(self)
        subjectBirthday = QLineEdit(self)
        subjectGender = QLineEdit(self)
        subjectNationality = QLineEdit(self)
        addSubjectButton = QPushButton('Add Subject', self)
        addSubjectButton.pressed.connect(lambda: trainingController.saveSubject(subjectName,subjectBirthday,subjectGender,subjectNationality))

        startBtn = QPushButton("Start set")
        newBtn = QPushButton("New set")
        editBtn = QPushButton("Edit set")
        #editBtn.clicked.connect()
        editBtn.setEnabled(False)
        newBtn.clicked.connect(lambda: trainingController.startNewTest(self))
        #startBtn.clicked.connect()
        startBtn.setEnabled(False)

        subjectList = QListWidget()
        subjectList.setWindowTitle('Subjects List')
        subjectList.setMaximumSize(100, 100)
        subjectList.setMinimumSize(100, 100)

        trainingTestsList = QListWidget()
        trainingTestsList.setWindowTitle('Example List')
        trainingTestsList.setMaximumSize(100, 200)
        trainingTestsList.setMinimumSize(100, 200)
        #trainingTestsList.itemSelectionChanged.connect(lambda: trainingController.newSetSelection)

        #Top left
        topLeft = QGroupBox("Add New Subject")
        newTopLeft = QVBoxLayout()
        newTopLeft.addWidget(labelSubject)
        newTopLeft.addWidget(subjectName)
        newTopLeft.addWidget(labelBirthday)
        newTopLeft.addWidget(subjectBirthday)
        newTopLeft.addWidget(labelGender)
        newTopLeft.addWidget(subjectGender)
        newTopLeft.addWidget(labelNationality)
        newTopLeft.addWidget(subjectNationality)
        newTopLeft.addWidget(addSubjectButton)
        newTopLeft.addStretch(1)
        topLeft.setLayout(newTopLeft)
        topLeft.setMaximumSize(150,250)

        #Top right
        topRight = QGroupBox("Training Tests List")
        newTopRight = QVBoxLayout()
        newTopRight.addWidget(trainingTestsList)
        topRight.setLayout(newTopRight)
        topRight.setMaximumSize(150,250)

        #Bottom left
        bottomLeft = QGroupBox("Training Tests List")
        newBottomLeft = QVBoxLayout()
        newBottomLeft.addWidget(subjectList)
        bottomLeft.setLayout(newBottomLeft)
        bottomLeft.setMaximumSize(150,150)

        #Bottom right
        bottomRight = QGroupBox("Settings")
        newBottomRight = QVBoxLayout()
        newBottomRight.addWidget(startBtn)
        newBottomRight.addWidget(newBtn)
        newBottomRight.addWidget(editBtn)
        bottomRight.setLayout(newBottomRight)
        bottomRight.setMaximumSize(150,150)

        grid.addWidget(topLeft, 0, 0)
        grid.addWidget(topRight, 0, 1)
        grid.addWidget(bottomLeft, 1, 0)
        grid.addWidget(bottomRight, 1, 1)

        self.setLayout(grid)