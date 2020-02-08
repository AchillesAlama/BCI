"""This file contains functions to help inform user about things like errors through
for example pop-up windows."""

from PyQt5.QtWidgets import QMessageBox

def makeErrorPopup(errorMsg):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Error")
    msg.setText("ERROR: " + errorMsg)
    msg.setStandardButtons(QMessageBox.Ok)
    

