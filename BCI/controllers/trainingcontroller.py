from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAbstractItemView,QTableWidgetItem,QWizard
from PyQt5.QtCore import QSize, QThread, Qt
from PyQt5.QtGui import QIcon, QPixmap
import os
from shutil import copyfile, rmtree
from time import sleep
import random
from views.trainingView import TrainingWindow, UserEditPopup, UserAddPopup
from controllers.dbController import DBController


class TrainingController():

    def __init__(self, parent=None):
        self.controller = parent
        self.view = TrainingWindow(parent = self)
        self.runController = None

        #Fill the user table
        self.updateUserTable()

    def handleUserButtonEnable(self):
        """Handles activation/deactivation of start run/delete user/edit user buttons.
        Exactly one user must be selected in list for enabling. Triggered on selection
        change in userTable."""
        if (len(self.view.userTable.selectedItems()) == 0):
            self.view.runButton.setEnabled(False)
            self.view.delUserBtn.setEnabled(False)
            self.view.editUserBtn.setEnabled(False)
        else:
            self.view.runButton.setEnabled(True)
            self.view.delUserBtn.setEnabled(True)
            self.view.editUserBtn.setEnabled(True)
    
    def getCurrentUserData(self):
        """Returns a dictionary with the user table columns as keys
        and values of the currently selected user.
        
        @return (dict):
            Data of currently selected user in table.
        """
        userDict = {}
        for c in range(self.view.userTable.columnCount()):
            colName = self.view.userTable.horizontalHeaderItem(c).text()
            userDict[colName] = self.view.userTable.item(self.view.userTable.currentRow(), c).text()
        
        return userDict

    def updateUserTable(self):
        """Sets user tree parameters based on fields of User in DB and
        fills tree with existing users"""

        self.view.userTable.clear()
        self.view.userTable.setRowCount(0)

        #Create user table columns based on DB fields
        allUsersData = DBController().getAllUsers()
        self.view.userTable.setColumnCount(len(allUsersData[0].keys()))
        self.view.userTable.setHorizontalHeaderLabels(allUsersData[0].keys())
        self.view.userTable.verticalHeader().setVisible(False) #Hide rownums
        self.view.userTable.setEditTriggers(QAbstractItemView.NoEditTriggers) #Disable editable cells
        self.view.userTable.setSelectionBehavior(QAbstractItemView.SelectRows) #Dont select individual cells
        self.view.userTable.setSelectionMode(QAbstractItemView.SingleSelection) #Select only 1 row
        self.view.userTable.itemSelectionChanged.connect(self.handleUserButtonEnable)

        #Fill table
        for r in range(len(allUsersData)):
            self.view.userTable.insertRow(r)
            for c, field in enumerate(allUsersData[0].keys()):
                self.view.userTable.setItem(r , c, QTableWidgetItem(str(allUsersData[r][field])))

    def addUser(self):
        self.currentPopUp = UserAddPopup(self)

    def editUser(self):
        self.currentPopUp = UserEditPopup(self)

    def deleteUser(self):
        """Shows popup for user to confirm deletion, 
        then removes from database.
        """
        #Find name and ID column
        userData = self.getCurrentUserData()

        #Prompt for confirmation
        deleteChoice = QMessageBox.question(self.view, 'Confirm user deletion', 
                                            'Are you sure you want to delete user ' 
                                            + userData['Name'] + " with ID " + userData['User_ID'] + 
                                            " from database permanently?", 
                                            QMessageBox.Yes | QMessageBox.No)
        
        if (deleteChoice == QMessageBox.Yes):
            DBController().deleteUser(userData['User_ID'] )
            self.updateUserTable() #Re-fill table


    def prepareSamples(username, testType):
        """Gets the samples from all runs for a certain user for a certain
        type of experiment, divides them up into chunks based on continuous 
        Category, then these chunks are divided further into 4 sections based
        on time (1 sec. long chunks), these chunks are then FFT:d and saved
        in 4 different CSV files in a format ready to use in the ML model.
        Each file has the samples from the 1st, 2nd, 3rd, or 4th second
        per continous output."""
        
        #userSamps = DBController().getUserSamples(username, testType)