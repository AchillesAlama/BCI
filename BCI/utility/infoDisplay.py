"""This file contains functions to help inform user about things like errors through
for example pop-up windows."""

from PyQt5.QtWidgets import QMessageBox

def makeErrorPopup(errorMsg):
    """Returns a msg box to be executed from calling script with msg.exec()"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Error")
    msg.setText("ERROR: " + errorMsg)
    msg.setStandardButtons(QMessageBox.Ok)
    return msg 

def makeYesNoPopup(infoMsg):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Info")
    msg.setText(infoMsg)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    return msg 
