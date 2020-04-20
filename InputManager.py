from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox, QApplication
import TheGraph as tg
import TheSession as ts
import DisplaySettingsManager as dsm
import GraphExporter
import JSONConverter
import TimeCriticalOperations as tco
from enum import Enum

#Mode options enum
class PlayMode(Enum):
    ACQUISITION = 0
    PLAYBACK = 1

#Called on start of program to perform all needed initialization
#Need initialization for default values, references, button icons, and button handlers
def initialSetUp (theMainWindow, thePlayIcon, theUnlockedIcon):

    global settingsLocked, mainWindow, playMode
    global playIcon, pauseIcon, unlockedIcon, lockedIcon
    
    #If false you can change the trial, session or system settings
    settingsLocked = False

    #Sets the mainWindow, playIcon and UnlockedIcon to the variables that were passed
    mainWindow = theMainWindow
    playIcon = thePlayIcon
    unlockedIcon = theUnlockedIcon
    
    #Sets the icon for the pause button
    pauseIcon = QtGui.QIcon()
    pauseIcon.addPixmap(QtGui.QPixmap("Images/Pause Button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

    #Sets the icon for the locked button
    lockedIcon = QtGui.QIcon()
    lockedIcon.addPixmap(QtGui.QPixmap("Images/Locked Button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

    #Default play mode is data acquisition
    setPlayMode(PlayMode.ACQUISITION)

    connectButtons()

#Connects buttons to their handlers (handlers are the functions called on button clicks)
def connectButtons ():
    #Detects when the data acquisition buttons are pressed
    mainWindow.lockButton.clicked.connect(lockButtonPressed)
    mainWindow.playButton.clicked.connect(playButtonPressed)

    #Detects when the playback buttons are pressed
    mainWindow.previousButton.clicked.connect(previousTrial)
    mainWindow.nextButton.clicked.connect(nextTrial)

    #Detects when the rest of the button bar buttons are pressed
    mainWindow.stopButton.clicked.connect(stopSessionConditionalConfirmation)

    #Detects all "File -> [X]" menu actions
    mainWindow.actionNew.triggered.connect(newSession)
    mainWindow.actionOpen.triggered.connect(openSession)
    mainWindow.actionCaptureGraph.triggered.connect(lambda: capture("Graph"))
    mainWindow.actionCaptureWindow.triggered.connect(lambda: capture("Window"))
    mainWindow.actionCaptureScreen.triggered.connect(lambda: capture("Screen"))
    mainWindow.actionClose.triggered.connect(closeWindow)

    #Detects all "Edit -> [X]" menu actions
    mainWindow.actionDisplaySettings.triggered.connect(dsm.openDisplaySettingsMenu)

    #Override close event function of QMainWindow for purpose of adding "are you sure you want to quit?" prompt
    mainWindow.centralwidget.parentWidget().closeEvent = closeEvent

#When the lock button is pressed, toggle lock status (but only lock if settings are valid)
def lockButtonPressed ():
    #If the settings are locked already, attempt to unlock using setLockModeForSettings
    if settingsLocked:
        setLockModeForSettings(False)
    
    #Otherwise try and lock, verifying that the settings are valid
    elif verifySettingsValid():
        setLockModeForSettings(True)
    
#When the play button is pressed, toggle play status
def playButtonPressed ():
    setPlaying(not tg.isPlaying())

#When the previous button is pressed, load previous trial
def previousTrial():
    #Clear current trial
    tg.resetGraph()

    #Decrement trial number
    ts.currentSession.currentTrial -= 1

    #Wrap around if trial number of out bounds
    if ts.currentSession.currentTrial < 1:
        ts.currentSession.currentTrial = ts.currentSession.trialCount

    #Display new trial
    tg.createGraph()

#When the next button is pressed, load next trial
def nextTrial():
    #Clear current trial
    tg.resetGraph()
    
    #Increment trial number
    ts.currentSession.currentTrial += 1

    #Wrap around if trial number of out bounds
    if ts.currentSession.currentTrial > ts.currentSession.trialCount:
        ts.currentSession.currentTrial = 1

    #Display new trial
    tg.createGraph()

#Tell the window (QMainWindow) to close (this will then be intercepted by the close event function below)
def closeWindow ():
    mainWindow.centralwidget.parentWidget().close()

#Whenever the window is supposed to close, this event intercepts/overrides the default close event
def closeEvent (event):
    #Must stop session before we can close window
    if ts.currentSession:
        stopSessionConditionalConfirmation()

        #If the user does not want to close session, the session will remain after above line
        #In such a case, ignore event and return, else fall through to close code
        if ts.currentSession:
            event.ignore() #Do not close window
            return

    #Clean up
    tco.orderToStopProcess()

    #Closes the QMainWindow, which closes the program
    event.accept()

#Defines whether or not the trial is playing (only applies to data acquisition mode)
def setPlaying (play):
    if playMode == PlayMode.PLAYBACK:
        return

    #Creates a session if one is not already running (there must be a current session to control)
    if not ts.currentSession:
        ts.currentSession = ts.TheSession(mainWindow)
        JSONConverter.startDataAcquisition()

    #Sets whether or not the graph is playing based off of the value of play
    tg.setPlaying(play)

    #If play is true change the icon to the pause Icon
    if play:
        mainWindow.playButton.setIcon(pauseIcon)

    #Otherwise set the icon to the play icon
    else:
        mainWindow.playButton.setIcon(playIcon)

    #Any interaction with play button means you cannot unlock the settings
    mainWindow.lockButton.setEnabled(False)

    #The session can be stopped if the play button is interacted with
    mainWindow.stopButton.setEnabled(True)

#Sets the lockmode
def setLockModeForSettings (lock):
    
    #Changes the locked setting to the value that is passed to the function
    global settingsLocked

    settingsLocked = lock

    #If the system is locked, play can be pressed 
    mainWindow.playButton.setEnabled(lock)    

    #If locked, set the icon accordingly 
    if lock:
        mainWindow.lockButton.setIcon(lockedIcon)
    else:
        mainWindow.lockButton.setIcon(unlockedIcon)

    #If the system is locked set the defaults for any empty fields 
    if lock:
        assignDefaultsToEmptyFields()

    #Change the accessibility of the settings
    setAccessibilityOfSettings(not lock)

#Sets the accessibility of the various setting entries 
def setAccessibilityOfSettings (accessible):
    mainWindow.sessionNameLineEdit.setEnabled(accessible)
    mainWindow.subjectAgeSpinBox.setEnabled(accessible)
    mainWindow.subjectSexComboBox.setEnabled(accessible)
    mainWindow.sampleIntervalSpinBox.setEnabled(accessible)
    mainWindow.trialCountSpinBox.setEnabled(accessible)
    mainWindow.itiSpinBox.setEnabled(accessible)
    mainWindow.itiVarianceSpinBox.setEnabled(accessible)
    mainWindow.trialDurationSpinBox.setEnabled(accessible)
    mainWindow.baselineDurationSpinBox.setEnabled(accessible)
    mainWindow.csNameLineEdit.setEnabled(accessible)
    mainWindow.csDurationSpinBox.setEnabled(accessible)
    mainWindow.interstimulusIntervalSpinBox.setEnabled(accessible)
    mainWindow.usNameLineEdit.setEnabled(accessible)
    mainWindow.usDurationSpinBox.setEnabled(accessible)

#Checks the current settings and brings up a message box if anything is invalid
#Returns if the settings are valid or not
def verifySettingsValid():
    settingsValidityText = "Current settings are invalid for the following reasons:\n\n"
    trialDurationInvalid = not trialDurationIsValid()
    sessionNameInvalid = not sessionNameIsValid()

    if trialDurationInvalid:
        settingsValidityText += "Trial duration must be greater than or equal to baseline + CS + ISI + US\n"
    if sessionNameInvalid:
        settingsValidityText += "Session name may not contain any of the following characters: \\ / : * ? \" < > |\n"
    if trialDurationInvalid or sessionNameInvalid:
        invalidSettingsNotice = QMessageBox()
        invalidSettingsNotice.setText(settingsValidityText)
        invalidSettingsNotice.setWindowTitle("Invalid Settings")
        invalidSettingsNotice.setStandardButtons(QMessageBox.Ok)
        invalidSettingsNotice.setIcon(QMessageBox.Warning)
        invalidSettingsNotice.exec()

    return not trialDurationInvalid and not sessionNameInvalid 

#Returns whether or not the trial duration is valid based on the various other durations
def trialDurationIsValid ():
    beginningToEndOfUS = mainWindow.baselineDurationSpinBox.value()
    beginningToEndOfUS += mainWindow.csDurationSpinBox.value()
    beginningToEndOfUS += mainWindow.interstimulusIntervalSpinBox.value()
    beginningToEndOfUS += mainWindow.usDurationSpinBox.value()

    return mainWindow.trialDurationSpinBox.value() >= beginningToEndOfUS

#Returns if the session name contains any characters that could cause problems if in a file name
#No regex used because importing the library for one time use probably isn't worth it
def sessionNameIsValid ():
    sessionText = mainWindow.sessionNameLineEdit.text()
    return not ("\\" in sessionText or "/" in sessionText or ":" in sessionText or "<" in sessionText or ">" in sessionText or
        "*" in sessionText or "?" in sessionText or "\"" in sessionText or "|" in sessionText)

#Sets the defaults for the names if this function is called
def assignDefaultsToEmptyFields ():
    if not mainWindow.csNameLineEdit.text():
        mainWindow.csNameLineEdit.setText(mainWindow.csNameLineEdit.placeholderText())

    if not mainWindow.usNameLineEdit.text():
        mainWindow.usNameLineEdit.setText(mainWindow.usNameLineEdit.placeholderText())

#Stop session and only ask for confirmation if appropriate (i.e. if data acquisition is ongoing)
#Asking for confirmation means a "are you sure" dialog box pops up and you can say yes or no
def stopSessionConditionalConfirmation ():
    #Ask for confirmation only if data acquisition is ongoing
    if (not tg.done) and playMode == PlayMode.ACQUISITION:
        stopSessionWithConfirmation()
    else:
        stopSessionWithoutConfirmation()

#Ask if user is sure they want to stop, then proceed if yes
def stopSessionWithConfirmation ():
    #Pause during "Are you sure?" dialog pop-up
    if tg.isPlaying():    
        setPlaying(False)

    #Craft confirmation message
    stopMessage = "Data acquisition is incomplete."

    if JSONConverter.trialsSaved > 0:
        stopMessage += "\nOnly completed trials will be saved."
    else:
        stopMessage += "\nThe session will not be saved since no trials have completed."

    stopMessage += "\n\nAre you sure you want to stop the session anyways?"

    #Open dialog with message to confirm that this is what the user wants
    confirmStop = QMessageBox()
    confirmStop.setText(stopMessage)
    confirmStop.setWindowTitle("Confirm Session Stop")
    confirmStop.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    confirmStop.setIcon(QMessageBox.Question)
    decision = confirmStop.exec()

    #If it is, stop the session
    if decision == QMessageBox.Yes:
        stopSessionWithoutConfirmation()

#Stops the session immediately without asking user
def stopSessionWithoutConfirmation ():
    #Save data acquisition session
    if playMode == PlayMode.ACQUISITION:
        JSONConverter.endDataAcquisition()

    #Clears the session
    ts.currentSession = None

    #Resets the graph
    tg.resetGraph()

    #Resets the play, stop, and lock buttons
    mainWindow.playButton.setIcon(playIcon)
    mainWindow.playButton.setEnabled(True)
    mainWindow.stopButton.setEnabled(False)
    mainWindow.lockButton.setEnabled(True)

    #Always go back to default acquisition mode when no session is pulled up
    setPlayMode(PlayMode.ACQUISITION)

#Takes a screenshot, opens a "Save As" window, and then saves as expected (unless user clicks cancel)
#What it captures (graph, window, or whole screen) is determined via parameter
def capture (captureType):
    #Take shot of graph
    if captureType == "Graph":
        #Cases where graph capture fails
        if (not tg.graphInitialized) or tg.duringITI:
            #Notify user there is no graph to capture
            noGraph = QMessageBox()
            noGraph.setText("There is no graph to capture.")
            noGraph.setWindowTitle("Graph Capture Failed")
            noGraph.setStandardButtons(QMessageBox.Ok)
            noGraph.setIcon(QMessageBox.Information)
            noGraph.exec()

            #Do not proceed with graph capture
            return
        
        #This only takes a shot of the stimulus graph (excludes bar graph on side)
        screenshot = GraphExporter.captureItem(tg.stimulusGraph)
        
        #This includes the bar graph on the side
        #screenshot = mainWindow.graphWidget.grab()

    #Take shot of main window
    elif captureType == "Window":
        screenshot = mainWindow.centralwidget.grab()

    #Take shot of entire screen/desktop
    else:
        screenshot = QApplication.primaryScreen().grabWindow(0)
    
    #Pop up "Save As" window to retrieve file name and type to save as
    nameAndType = QtGui.QFileDialog.getSaveFileName(parent = mainWindow.centralwidget,
                                                    caption = "Save " + captureType + " Capture As",
                                                    filter = "PNG (*.png);;JPG (*.jpg)")

    #If user didn't click cancel on "Save As", save screenshot using "Save As" options
    if len(nameAndType[0]) > 0:
        screenshot.save(nameAndType[0], extractFileType(nameAndType[1]))

#Extracts "jpg" from "JPG (*.jpg)" for example.
#The "JPG (*.jpg)" is returned from QtGui.QFileDialog.getSaveFileName as second element in string tuple, but...
#QPixMap.save() requires ".jpg", thus this function performs the conversion.
def extractFileType (filter):
    #Default substring limits in case we can't find them in the string
    period = 0  #Start of substring (exclusive)
    closeParen = len(filter) #End of substring (exclusive)

    #Find substring limits in string
    for x in range(0, len(filter)):
        if filter[x] == '.':
            period = x
        elif filter[x] == ')':
            closeParen = x

    #Perform substring operation and return result
    return filter[(period + 1):closeParen]

def newSession():
    #You must first close the current session
    if ts.currentSession:
        stopSessionConditionalConfirmation()

        #If user says no to stopping current session, then cancel making new one
        if ts.currentSession:
            return

    #Creating new sessions means being in data acquisition mode
    setPlayMode(PlayMode.ACQUISITION)

    #Start with default settings again
    resetSettingsToDefaults()

    #That's it: at this point the user can navigate the UI to start the new session when and as desired

def openSession():
    #You must first close the current session 
    if ts.currentSession:
        stopSessionConditionalConfirmation()

        #If user says no to stopping current session, then cancel opening another
        if ts.currentSession:
            return

    #Pop up "Open" window to retrieve file name and location of session file user wants to open
    #The function returns a (file name/location, file type) tuple but I index it at 0 to just get file name
    fileNameAndLocation = QtGui.QFileDialog.getOpenFileName(parent = mainWindow.centralwidget,
                                                    caption = "Open Session For Playback",
                                                    filter = "JSON (*.json)")[0]

    #If user didn't click cancel on "Open", proceed for opening session in playback mode
    if len(fileNameAndLocation) > 0:
        #Opening a session means going into playback mode
        setPlayMode(PlayMode.PLAYBACK)

        #Load in the session from the JSON file
        errorMessage = JSONConverter.openSession(fileNameAndLocation)
        
        #Check if there was an error before proceeding...
        if errorMessage:
            #Error reading session data, notify user and return to default acquisition mode...

            #Craft error message
            fullMessage = "Cannot read session file for the following reason...\n\n" + errorMessage

            #Notify user
            cannotReadSession = QMessageBox()
            cannotReadSession.setText(fullMessage)
            cannotReadSession.setWindowTitle("Error Opening Session")
            cannotReadSession.setStandardButtons(QMessageBox.Ok)
            cannotReadSession.setIcon(QMessageBox.Critical)
            cannotReadSession.exec()

            #In case a session was created, clear it (there shouldn't be though, just being safe)
            if ts.currentSession:
                stopSessionWithoutConfirmation()

            #Return to data acquisition mode
            setPlayMode(PlayMode.ACQUISITION)
        else:
            #No error reading session data, continue...

            #Display the first trial of the session on the graph
            tg.createGraph()
    else:
        #User cancelled opening a session so default back to empty, ready to start data acquisition mode
        setPlayMode(PlayMode.ACQUISITION)

#Use this to change the playMode variable, do not assign to it directly
def setPlayMode(newPlayMode):
    #Can only change the play mode when there is no ongoing session
    if ts.currentSession:
        return

    #Remember new play mode
    global playMode
    playMode = newPlayMode

    #Update text that indicates play mode
    updateSessionInfoLabel()

    #Show buttons that belong to that play mode and hide buttons that do not
    #Also do hide before show so that the layout doesn't get stretched from excess shown buttons
    if playMode == PlayMode.ACQUISITION:
        mainWindow.previousButton.hide()
        mainWindow.nextButton.hide()
        mainWindow.lockButton.show()
        mainWindow.playButton.show()
    else:
        mainWindow.lockButton.hide()
        mainWindow.playButton.hide()
        mainWindow.previousButton.show()
        mainWindow.nextButton.show()

    #Lock settings in playback, unlock settings in data acquisition (session cannot be ongoing)
    mainWindow.lockButton.setEnabled(playMode == PlayMode.ACQUISITION)
    setLockModeForSettings(playMode == PlayMode.PLAYBACK)

    #Playback immediately opens session (so stop should be accessible), but opposite for acquisition
    mainWindow.stopButton.setEnabled(playMode == PlayMode.PLAYBACK)

#Updates the text near the top right of the main window that specifies mode and trial progress
def updateSessionInfoLabel():
    #Add the mode the graph is running in
    if playMode == PlayMode.ACQUISITION:
        newText = "DATA ACQUISITION\n\n"
    else:
        newText = "PLAYBACK\n\n"

    #Add "TRIAL [X] / [Y]" if there is an ongoing session
    if ts.currentSession:
        newText += ts.currentSession.getTrialProgressString()

    #Update label with new text
    mainWindow.sessionInfoLabel.setText(newText)

#Resets all setting fields on the UI to have their default values
def resetSettingsToDefaults():
    mainWindow.sessionNameLineEdit.setText("")
    mainWindow.subjectAgeSpinBox.setValue(30)
    mainWindow.subjectSexComboBox.setCurrentIndex(0)
    mainWindow.sampleIntervalSpinBox.setValue(1)
    mainWindow.trialCountSpinBox.setValue(60)
    mainWindow.itiSpinBox.setValue(15)
    mainWindow.itiVarianceSpinBox.setValue(3)
    mainWindow.trialDurationSpinBox.setValue(3000)
    mainWindow.baselineDurationSpinBox.setValue(1000)
    mainWindow.csNameLineEdit.setText("Tone")
    mainWindow.csDurationSpinBox.setValue(100)
    mainWindow.interstimulusIntervalSpinBox.setValue(500)
    mainWindow.usNameLineEdit.setText("Air Puff")
    mainWindow.usDurationSpinBox.setValue(100)