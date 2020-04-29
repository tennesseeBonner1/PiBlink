"""
	Handles all of the events that happen once Analyze -> Re-Analyze Session is pressed in the
	menu bar.
"""

from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QMessageBox
import AnalysisSettingsWindow as asw
from datetime import datetime
import json
import JSONConverter as jsCon
import DataAnalysis as da
import InputManager as im

#sets up the window for re-analyzing the currently open session
def openAnalysisSettingsWindow():
	global windowWrapper, dialogWindow

	dialogWindow = QDialog()
	windowWrapper = asw.Ui_AnalysisSettingsWindow()
	windowWrapper.setupUi(dialogWindow)

	#set connections
	windowWrapper.pushButton_ReAnalyze.released.connect(reAnalyze)
	windowWrapper.radioButton_GenerateNew.toggled.connect(setFilenameEditorEnabled)
	
	#properly set the text in the line editor
	windowWrapper.lineEdit_customSaveName.setText(getCurrentFilename())
	
	dialogWindow.exec()

#This function is the main course of the whole module meal
#Takes the values from the analysis settings menu, grabs the json file of the session currently
#open, and loops through each trial, replacing its onsets and offsets with results from DataAnalysis
def reAnalyze():
	overwrite = windowWrapper.radioButton_Overwrite.isChecked()
	newFile = windowWrapper.radioButton_GenerateNew.isChecked()
	customName = windowWrapper.lineEdit_customSaveName.text()
	stdDevNumber = windowWrapper.spinBox_StdDev.value()
	minSamples = windowWrapper.spinBox_MinSamp.value()

	nameError = False

	#first we check to see if we're saving with a custom name that's valid
	if not overwrite or newFile:
		if ("\\" in customName or "/" in customName or ":" in customName or "<" in customName or ">" in customName or "*" in customName or "?" in customName or "\"" in customName or "|" in customName):
			invalidSettingsNotice = QMessageBox()
			invalidSettingsNotice.setText("Filename may not contain any of the following characters: \\ / : * ? \" < > |\n")
			invalidSettingsNotice.setWindowTitle("Invalid Filename")
			invalidSettingsNotice.setStandardButtons(QMessageBox.Ok)
			invalidSettingsNotice.setIcon(QMessageBox.Warning)
			nameError = True
			invalidSettingsNotice.exec()
			return

	fileCopy = jsCon.jsonObject
	
	#Go through all of the trials, calculate their stats based on their data, and store that in place
	#of the old stats
	numTrials = int(fileCopy["header"]["trialCount"])
	for x in range(numTrials):
		fileCopy["trials"][x]["stats"] = da.getTrialStats(stdDevNumber, minSamples, fileCopy["trials"][x]["samples"])
	
	#Get the contents ready to be written to file
	fileString = json.dumps(fileCopy)

	#get the name of the file currently open,
	oldFileName = getCurrentFilename()

	#check if there's already a .json in the new name, removing it if there is
	if ".json" in customName:
		customName = customName.replace(".json", "")

	#replace the old name with the new name
	#oldFilename and customName should be the same if "Overwrite Current File" is enabled
	newFilename = jsCon.saveFilename.replace(oldFileName, customName)

	print(newFilename)

	saveFile = open(newFilename, "w")
	saveFile.write(fileString)
	saveFile.close()

	im.openSession(newFilename)
	if not nameError:
		closeWindow()

#Gets the filename of the currently open file and returns it
def getCurrentFilename():
	#Partition the lengthy pathname to get only the file name (checking for both \ and / to be safe)
	startName = jsCon.saveFilename.rpartition('\\')[2]
	startName = startName.rpartition('/')[2]

	#remove the file extension
	startName = startName.rpartition('.')[0]
	
	return startName

#Sets the line editor to be enabled/disabled depending on if the "Save as Custom Name" option is selected
def setFilenameEditorEnabled():
	windowWrapper.lineEdit_customSaveName.setEnabled(windowWrapper.radioButton_GenerateNew.isChecked())

def closeWindow():
	dialogWindow.close()