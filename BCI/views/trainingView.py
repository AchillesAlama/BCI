from PyQt5.QtWidgets import (QLineEdit,
                            QLabel, QWidget, QTableWidget,
                           QGridLayout,QPushButton, QGroupBox,
                           QVBoxLayout, QHBoxLayout, QMessageBox, 
                           QDateEdit, QComboBox)
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate

from controllers.dbController import DBController

class TrainingWindow(QWidget):
    """Contains all the elements necessary for user to enter
    some run data and start a new run"""

    def __init__(self, parent=None):
        super().__init__()
        self.controller = parent
        self.initUI()

    def initUI(self):
        """Adds all UI elements needed to start run."""
        #Main layout
        grid = QGridLayout()

        #Create user selection /edit box
        userBox = QGroupBox()
        userBox.setTitle("Select user for run")
        userBoxLayout = QVBoxLayout()
        userBox.setLayout(userBoxLayout)
        self.userTable = QTableWidget(self)
        userBtns = QGroupBox()
        userBtnsLayout = QHBoxLayout()
        userBtns.setLayout(userBtnsLayout)
        
        #Add buttons to delete/add/edit users
        self.addUserBtn = QPushButton("Add User")
        self.addUserBtn.clicked.connect(self.controller.addUser)
        userBtnsLayout.addWidget(self.addUserBtn)
        self.editUserBtn = QPushButton("Edit User")
        self.editUserBtn.clicked.connect(self.controller.editUser)
        userBtnsLayout.addWidget(self.editUserBtn)
        self.editUserBtn.setEnabled(False)
        self.delUserBtn = QPushButton("Delete User")
        self.delUserBtn.clicked.connect(self.controller.deleteUser)
        userBtnsLayout.addWidget(self.delUserBtn)
        self.delUserBtn.setEnabled(False)

        userBoxLayout.addWidget(self.userTable)
        userBoxLayout.addWidget(userBtns)
        grid.addWidget(userBox)

        #Add run starting button
        self.runButton = QPushButton("Start run")
        self.runButton.clicked.connect(self.controller.startRun)
        self.runButton.setEnabled(False) #Should only be activated by choice of user
        grid.addWidget(self.runButton, 1, 1)

        #Set main layout
        self.setLayout(grid)
    
    

class UserPopup(QWidget):
    """Super class for the two popups which allows users to be edited or added.
    They are so similar that it warrants one super class which creates the labels
    and entries."""

    def __init__(self, parent = None):
        super().__init__()
        self.controller = parent
        self.initUI()
        self.setWindowModality(Qt.ApplicationModal)
        self.show()

    def initUI(self):
        self.mainLayout = QVBoxLayout()
        lineEditsGroup = QGroupBox()
        grid = QGridLayout()

        #Create line edit labels for each field except user ID (non-editable)
        for i, key in enumerate(['Name', 'Birthday', 'Gender', 'Nationality']):
            grid.addWidget(QLabel(key+"*"), i, 0)

        #Create name line entry
        self.nameEntry = QLineEdit(self)
        grid.addWidget(self.nameEntry, 0, 1)

        #Create birthday entry
        self.birthdayEntry = QDateEdit(self)
        grid.addWidget(self.birthdayEntry, 1, 1)

        #Create gender selection
        self.genderBox = QComboBox(self)
        self.genderBox.addItem("Male")
        self.genderBox.addItem("Female")
        self.genderBox.addItem("Other")
        grid.addWidget(self.genderBox, 2, 1)

        #Add nationality
        self.nationEntry = QLineEdit(self)
        grid.addWidget(self.nationEntry, 3, 1)

        lineEditsGroup.setLayout(grid)
        self.mainLayout.addWidget(lineEditsGroup)

        self.setLayout(self.mainLayout)

    def verifyInputValidity(self):
        """Triggers when user tries to save changes. Checks all fields
        for correct data."""

        #Reset borders in case of earlier tries
        for field in [self.nameEntry, self.birthdayEntry, self.genderBox, self.nationEntry]:
            field.setStyleSheet("border: 1px solid black")

        if self.nameEntry.text().strip() == "": 
            self.nameEntry.setStyleSheet("border: 2px solid red")
            return 1

        if (self.birthdayEntry.date() >= QDate().currentDate()): 
            self.birthdayEntry.setStyleSheet("border: 2px solid red")
            return 1

        if self.genderBox.currentText().strip() not in ["Male", "Female", "Other"]: 
            self.genderBox.setStyleSheet("border: 2px solid red")
            return 1

        if self.nationEntry.text().strip() == "": 
            self.nationEntry.setStyleSheet("border: 2px solid red")
            return 1
        
        return 0


class UserEditPopup(UserPopup):
    """Represents the popup window allowing for existing user info
    to be edited."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.fillExistingInfo()
        self.setWindowTitle("Edit user data")

        #Add save changes button
        saveBtn = QPushButton("Save Changes", self)
        saveBtn.clicked.connect(self.addNewChanges)
        self.mainLayout.addWidget(saveBtn)

    def fillExistingInfo(self):
        """Fills the fields with current info."""

        userData = self.controller.getCurrentUserData()
        self.nameEntry.setText(userData['Name'])
         
        currentBirth = QDate.fromString(userData['Birthday'], "yyyy-MM-dd")
        self.birthdayEntry.setDate(currentBirth)

        genderDict = {'male': 0, 'female': 1, 'other': 2}
        self.genderBox.setCurrentIndex(genderDict[userData['Gender'].lower()])

        self.nationEntry.setText(userData['Nationality'])

    def addNewChanges(self):
        """Saves the changes of the user details to the database."""

        if (self.verifyInputValidity() == 0):
            #Extract info from fields and save to DB
            name = self.nameEntry.text()
            birthday = self.birthdayEntry.date().toPyDate().strftime("%Y-%m-%d")
            gender = self.genderBox.currentText()
            nationality = self.nationEntry.text()

            userid = self.controller.getCurrentUserData()['User_ID']
            userQuery = "UPDATE User SET Name=\"%s\", Birthday=\"%s\", Gender=\"%s\", Nationality=\"%s\" where User_ID = %s;"\
                % (name, birthday, gender, nationality, userid)

            DBController().db.update(userQuery)
            
            self.controller.updateUserTable()
            self.close()

class UserAddPopup(UserPopup):
    """Represents the popup window allowing for new users
    to be added to database."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add new user")

        #Add save changes button
        saveBtn = QPushButton("Add user", self)
        saveBtn.clicked.connect(self.addNewUser)
        self.mainLayout.addWidget(saveBtn)

    def addNewUser(self):
        """Saves the entered info to the database in order to create
        a new user."""
        if (self.verifyInputValidity() == 0):
            #Extract info from fields and save to DB
            name = self.nameEntry.text()
            birthday = self.birthdayEntry.date().toPyDate()
            gender = self.genderBox.currentText()
            nationality = self.nationEntry.text()
            newUser = DBController().makeUser(name=name, birthday=birthday,gender=gender, nationality=nationality)
            newUser.save()
            self.controller.updateUserTable()
            self.close()
            