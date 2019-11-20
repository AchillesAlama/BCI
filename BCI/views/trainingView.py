from PyQt5.QtWidgets import (QApplication, QAction, QLineEdit,
                            QLabel, QWidget, QMainWindow, QListWidget,
                           QGridLayout,QPushButton, QGroupBox,
                           QVBoxLayout, QToolButton, QHBoxLayout)
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, QThread, Qt
from PyQt5.QtGui import QIcon, QPixmap
from controllers.trainingController import TrainingController

class TrainingWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.initTraining()
        self.show()

    def initAddUserPopUp(self):
        self.title = 'Add User Form'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initAddUserPopUpUI()
        
    def initAddUserPopUpUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        addUserPopup = QMessageBox.question(self, 'Please fill in the fields', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        windowExample = QtWidgets.QWidget()
        labelName = QtWidgets.QLabel(windowExample)
        labelName.setText('Name: ')
        labelBirthday = QtWidgets.QLabel(windowExample)
        labelBirthday.setText('Birthday: ')
        labelGender = QtWidgets.QLabel(windowExample)
        labelGender.setText('Gender: ')
        labelNationality = QtWidgets.QLabel(windowExample)
        labelNationality.setText('Nationality: ')

        userName = QLineEdit(self)
        userBirthday = QLineEdit(self)
        userGender = QLineEdit(self)
        userNationality = QLineEdit(self)
        
        if addUserPopup == QMessageBox.Yes:
            lambda: trainingController.saveUser(userName,userBirthday,userGender,userNationality)
            addUserPopup.apply
        else:
            addUserPopup.cancel


    def initTraining(self):
        grid = QGridLayout()

        #Top left
        addUser = QPushButton("Add User")
        editUser = QPushButton("Edit User")
        deleteUser = QPushButton("Delete User")
        addUser.clicked.connect(initAddUserPopUp(self))

        topLeft = QGroupBox("Training Tests List")
        newTopLeft = QVBoxLayout()
        newTopLeft.addWidget(userList)
        topLeft.setLayout(newTopLeft)
        topLeft.setMaximumSize(150,150)

        #Top right
        topRight = QGroupBox("Training Tests List")
        newTopRight = QVBoxLayout()
        self.listCheckBox = ["Happy", "Sad", "Despressed", "F U", "idgaf"]
        for i, v in enumerate(self.listCheckBox):
            self.listCheckBox[i] = QCheckBox(v)
            self.listLabel[i] = QLabel()
            newTopRight.addWidget(self.listCheckBox[i], i, 0)

        for i, v in enumerate(self.listCheckBox):
            if self.listCheckBox[i].isChecked():
                lambda: trainingController.moodCheck(i)
            else:
                print("no boxes checked")



        #Bottom left
        userList = QListWidget()
        userList.setWindowTitle('User List')
        userList.setMaximumSize(100, 100)
        userList.setMinimumSize(100, 100)

        bottomLeft = QGroupBox("Add New User")
        newBottomLeft = QVBoxLayout()
        newBottomLeft.addWidget(addUser)
        newBottomLeft.addWidget(editUser)
        newBottomLeft.addWidget(deleteUser)
        newBottomLeft.addStretch(1)
        bottomLeft.setLayout(newBottomLeft)
        bottomLeft.setMaximumSize(150,250)

        #Bottom right
        bottomRight = QGroupBox("Settings")
        newBottomRight = QVBoxLayout()
        startTraining = QPushButton("Start")
        lambda: trainingController.startTraining()
        newBottomRight.addWidget(startTraining)


        grid.addWidget(topLeft, 0, 0)
        grid.addWidget(topRight, 0, 1)
        grid.addWidget(bottomLeft, 1, 0)
        grid.addWidget(bottomRight, 1, 1)

        self.setLayout(grid)