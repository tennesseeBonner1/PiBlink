""" InputManager.py
    Last Modified: 6/2/2020
    Taha Arshad, Tennessee Bonner, Devin Mensah, Khalid Shaik, Collin Vaille

    This file is responsible for handling all input from the main window. This file also controls a few high level concerns including the 
    creation/deletion of the current session, the play mode of the program (data acquisition vs. playback), and the play status of the 
    current session if the play mode is data acquisition (playing vs. paused). Because of this file's role in managing high level concerns, it could be 
    considered to be the controller of the program.
"""
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox, QApplication, QInputDialog
import TheGraph as tg
import TheSession as ts
import DisplaySettingsManager as dsm
import GraphExporter
import JSONConverter
import TimeCriticalOperations as tco
import MatrixManager as mm
import AnalysisSettingsManager as asm
from enum import Enum

#PlayMode options enumerator
class PlayMode(Enum):
    ACQUISITION = 0
    PLAYBACK = 1

#Initializes default values, references, button icons, and button handlers for the mainWindow
def initialSetUp(theMainWindow):

    global programCrashing, settingsLocked, mainWindow, playMode, popUpFont
    global playIcon, pauseIcon, unlockedIcon, lockedIcon
    
    #Used when intercepting a window close event to determine what to do
    programCrashing = False

    #If false you can change the trial, session or system settings
    settingsLocked = False

    #Get reference to the main window
    mainWindow = theMainWindow

    #Set play and unlocked icons
    playIcon = mainWindow.playButton.icon()
    unlockedIcon = mainWindow.lockButton.icon()
    
    #Sets the icon for the pause button
    pauseIcon = QtGui.QIcon()
    pauseIcon.addPixmap(QtGui.QPixmap("Images/Pause Button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

    #Sets the icon for the locked button
    lockedIcon = QtGui.QIcon()
    lockedIcon.addPixmap(QtGui.QPixmap("Images/Locked Button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

    #Define the font used in pop up windows
    popUpFont = QtGui.QFont()
    popUpFont.setPointSize(14)

    #Default play mode is data acquisition
    playMode = None
    setPlayMode(PlayMode.ACQUISITION)

    connectButtons()


#Connects buttons to their handlers (handlers are the functions called on button clicks)
def connectButtons():

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
    mainWindow.actionOpen.triggered.connect(lambda: openSession())
    mainWindow.actionSaveParametersAs.triggered.connect(JSONConverter.saveAsParameterFile)
    mainWindow.actionLoadParameters.triggered.connect(JSONConverter.loadParameterFile)
    mainWindow.actionCaptureGraph.triggered.connect(lambda: capture("Graph", False))
    mainWindow.actionCaptureWindow.triggered.connect(lambda: capture("Window", False))
    mainWindow.actionCaptureScreen.triggered.connect(lambda: capture("Screen", False))

    #Detects all "Edit -> [X]" menu actions
    mainWindow.actionDisplaySettings.triggered.connect(dsm.openDisplaySettingsMenu)

    #Detects all "Analyze -> [X]" menu actions
    mainWindow.actionRe_Analyze_Session.triggered.connect(asm.openAnalysisSettingsWindow)
    mainWindow.actionGenerate_Matrix_View.triggered.connect(mm.generateMatrixView)
    mainWindow.actionGoToTrial.triggered.connect(lambda: openGoToTrialDialog(None))

    #Detects when user clicks on session info label
    mainWindow.sessionInfoLabel.mousePressEvent = openGoToTrialDialog

    #Override close event function of QMainWindow for purpose of adding "are you sure you want to quit?" prompt
    mainWindow.centralwidget.parentWidget().closeEvent = closeEvent


#When the lock button is pressed, toggle lock status (but only lock if settings are valid)
def lockButtonPressed():

    #If the settings are locked already, attempt to unlock using setLockModeForSettings
    if settingsLocked:
        setLockModeForSettings(False)
    
    #Otherwise try and lock, verifying that the settings are valid
    elif verifySettingsValid():
        setLockModeForSettings(True)
    

#When the play button is pressed, toggle play status
def playButtonPressed():
    setPlaying(not tg.playing)


#Called when Analyze -> Go To Trial is selected or when session info label is clicked
#In order to be called when label is clicked on, event needs to be passed in...
#but it's never used
def openGoToTrialDialog(event):
    #Only works if session is loaded in playback
    if playMode != PlayMode.PLAYBACK or (not ts.currentSession):
        return

    #Open dialog box to prompt for trial number
    inputDialog = QInputDialog(mainWindow.centralwidget)
    inputDialog.setInputMode(QInputDialog.IntInput)
    inputDialog.setWindowTitle("Go To Trial")
    inputDialog.setLabelText("Go To Trial...")
    inputDialog.setFont(popUpFont)
    inputDialog.setIntValue(ts.currentSession.currentTrial)
    ok = inputDialog.exec()

    #If clicked OK, go to specified trial
    if ok:
        loadTrial(inputDialog.intValue())


#When the previous button is pressed, load previous trial
def previousTrial():

    loadTrial(ts.currentSession.currentTrial - 1)


#When the next button is pressed, load next trial
def nextTrial():

    loadTrial(ts.currentSession.currentTrial + 1)


#Called to load a specific trial
def loadTrial(trialNumber):

    #Clear current trial
    tg.resetTrialGraph()
    
    #Set trial number, wrapping around if trial number is out bounds
    if trialNumber > ts.currentSession.trialCount:
        ts.currentSession.currentTrial = 1

    elif trialNumber < 1:
        ts.currentSession.currentTrial = ts.currentSession.trialCount

    else:
        ts.currentSession.currentTrial = trialNumber

    #Display new trial
    tg.createTrialGraph()


#Whenever the window is supposed to close, this event intercepts/overrides the default close event
def closeEvent(event):

    #Must stop session before we can close window
    if ts.currentSession and (not programCrashing):
        stopSessionConditionalConfirmation()

        #If the user does not want to close session, the session will remain (In such a case, ignore event and return)
        if ts.currentSession:
            event.ignore() #Do not close window
            return

    #Clean up
    tco.orderToStopProcess()

    #Closes the QMainWindow, which closes the program
    event.accept()


#Stop session and only ask for confirmation if appropriate (if data acquisition is ongoing)
def stopSessionConditionalConfirmation():

    #Ask for confirmation only if data acquisition is ongoing
    if (not tg.done) and playMode == PlayMode.ACQUISITION:
        stopSessionWithConfirmation()

    else:
        stopSessionWithoutConfirmation()


#Ask if user is sure they want to stop, then proceed if yes
def stopSessionWithConfirmation():

    #Pause during "Are you sure?" dialog pop-up
    if tg.playing:    
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
    confirmStop.setFont(popUpFont)
    decision = confirmStop.exec()

    #If it is, stop the session
    if decision == QMessageBox.Yes:
        stopSessionWithoutConfirmation()


#Stops the session immediately without asking user
def stopSessionWithoutConfirmation():

    #For data acquisition sessions, stop sampling and save to file
    if playMode == PlayMode.ACQUISITION:
        #Stop sampling
        tco.orderToStopSession()

        #Save session to file
        JSONConverter.endDataAcquisition()

        #Hide trial info label
        mainWindow.trialInfoLabel.hide()

    #Clears the session
    ts.currentSession = None

    #Resets the graph
    tg.resetTrialGraph()

    #Resets the play, stop, and lock buttons
    mainWindow.playButton.setIcon(playIcon)
    mainWindow.playButton.setEnabled(True)
    mainWindow.stopButton.setEnabled(False)
    mainWindow.lockButton.setEnabled(True)

    #Always go back to default acquisition mode when no session is pulled up
    setPlayMode(PlayMode.ACQUISITION)


#Defines whether or not the trial is playing (only applies to data acquisition mode)
def setPlaying(play):

    #No pause/play in playback
    if playMode == PlayMode.PLAYBACK:
        return

    #Creates a session if there's not one already (there must be a current session)
    if not ts.currentSession:

        #Create session
        ts.currentSession = ts.TheSession(mainWindow)
        
        #Perform set up specific to data acquisition...

        #Prepare session saving module
        JSONConverter.startDataAcquisition()

        #Display trial info label
        mainWindow.trialInfoLabel.setText("RUNNING TRIAL")
        mainWindow.trialInfoLabel.show()

    #Sets whether or not the graph is playing based off of the value of play
    tg.setPlaying(play)

    #Update play button icon
    if play:
        mainWindow.playButton.setIcon(pauseIcon)
    else:
        mainWindow.playButton.setIcon(playIcon)

    #Update trial info label
    if not tg.duringITI:
        if play:
            mainWindow.trialInfoLabel.setText("RUNNING TRIAL")
        else:
            mainWindow.trialInfoLabel.setText("TRIAL PAUSED")

    #Any interaction with play button means you cannot unlock the settings
    #...because a session must already be running
    mainWindow.lockButton.setEnabled(False)

    #The session can be stopped if the play button is interacted with
    #...because a session must already be running
    mainWindow.stopButton.setEnabled(True)


#Sets the lockmode
def setLockModeForSettings(lock):
    
    global settingsLocked

    #Changes the locked setting to the value that is passed to the function
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
def setAccessibilityOfSettings(accessible):

    mainWindow.sessionNameLineEdit.setEnabled(accessible)
    mainWindow.subjectAgeSpinBox.setEnabled(accessible)
    mainWindow.subjectSexComboBox.setEnabled(accessible)
    mainWindow.sampleIntervalSpinBox.setEnabled(accessible)
    mainWindow.trialCountSpinBox.setEnabled(accessible)
    mainWindow.itiSpinBox.setEnabled(accessible)
    mainWindow.itiVarianceSpinBox.setEnabled(accessible)
    mainWindow.minVoltageSpinBox.setEnabled(accessible)
    mainWindow.thresholdSDSpinBox.setEnabled(accessible)
    mainWindow.thresholdMinDurSpinBox.setEnabled(accessible)
    mainWindow.trialDurationSpinBox.setEnabled(accessible)
    mainWindow.baselineDurationSpinBox.setEnabled(accessible)
    mainWindow.csNameLineEdit.setEnabled(accessible)
    mainWindow.csDurationSpinBox.setEnabled(accessible)
    mainWindow.interstimulusIntervalSpinBox.setEnabled(accessible)
    mainWindow.usNameLineEdit.setEnabled(accessible)
    mainWindow.usDurationSpinBox.setEnabled(accessible)
    mainWindow.usDelaySpinBox.setEnabled(accessible)

    #Also set accessibility of loading settings
    mainWindow.actionLoadParameters.setEnabled(accessible)


#Checks the current settings and brings up a message box if anything is invalid as well as return a boolean based on the validity
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
        invalidSettingsNotice.setFont(popUpFont)
        invalidSettingsNotice.exec()

    return not trialDurationInvalid and not sessionNameInvalid 


#Returns whether or not the trial duration is valid based on the various other durations
def trialDurationIsValid():

    beginningToEndOfUS = mainWindow.baselineDurationSpinBox.value()
    beginningToEndOfUS += mainWindow.csDurationSpinBox.value()
    beginningToEndOfUS += mainWindow.interstimulusIntervalSpinBox.value()
    beginningToEndOfUS += mainWindow.usDurationSpinBox.value()

    return mainWindow.trialDurationSpinBox.value() >= beginningToEndOfUS


#Returns if the session name contains any characters that could cause problems in a file name
def sessionNameIsValid():

    sessionText = mainWindow.sessionNameLineEdit.text()
    return not ("\\" in sessionText or "/" in sessionText or ":" in sessionText or "<" in sessionText or ">" in sessionText or "*" in sessionText or "?" in sessionText or "\"" in sessionText or "|" in sessionText)

#FUNCTION IS CURRENTLY INCOMPLETE AND UNIMPLEMENTED
def trialCountIsValid():
    return MainWindow.trailCountSpinBox.value() % 2 == 0

#Sets the defaults for the names if this function is called
def assignDefaultsToEmptyFields():

    if not mainWindow.csNameLineEdit.text():
        mainWindow.csNameLineEdit.setText(mainWindow.csNameLineEdit.placeholderText())

    if not mainWindow.usNameLineEdit.text():
        mainWindow.usNameLineEdit.setText(mainWindow.usNameLineEdit.placeholderText())


#Takes a screenshot (of graph, window, or whole screen depending on captureType) and then...
def capture(captureType, returnCapture):

    #Take shot of graph
    if captureType == "Graph":

        #Cases where graph capture fails
        if not tg.graphInitialized:

            #Notify user there is no graph to capture
            noGraph = QMessageBox()
            noGraph.setText("There is no graph to capture.")
            noGraph.setWindowTitle("Graph Capture Failed")
            noGraph.setStandardButtons(QMessageBox.Ok)
            noGraph.setIcon(QMessageBox.Information)
            noGraph.setFont(popUpFont)
            noGraph.exec()

            #Do not proceed with graph capture
            return
        
        #This only takes a shot of the stimulus graph (excludes bar graph on side)
        screenshot = GraphExporter.captureItem(tg.trialGraph)
        
    #Take shot of main window
    elif captureType == "Window":
        screenshot = mainWindow.centralwidget.grab()

    #Take shot of entire screen/desktop
    else:
        screenshot = QApplication.primaryScreen().grabWindow(0)
    
    #Returns the capture
    if returnCapture:
        return screenshot

    #Opens a "Save As" window, and then saves as expected (unless user clicks cancel)
    else:

        #Pop up "Save As" window to retrieve file name and type to save as
        nameAndType = QtGui.QFileDialog.getSaveFileName(parent = mainWindow.centralwidget, caption = "Save " + captureType + " Capture As", filter = "PNG (*.png);;JPG (*.jpg)")

        #If user didn't click cancel on "Save As", save screenshot using "Save As" options
        if len(nameAndType[0]) > 0:
            screenshot.save(nameAndType[0], extractFileType(nameAndType[1]))


#Edit the filename to remove 'jpeg'
def extractFileType(filter):

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


#Called when a new session is created
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
    #resetSettingsToDefaults()


#Open the session
def openSession(fileStr=""):

    #You must first close the current session 
    if ts.currentSession:
        stopSessionConditionalConfirmation()

        #If user says no to stopping current session, then cancel opening another
        if ts.currentSession:
            return

    if fileStr == "":

        #Pop up "Open" window to retrieve file name and location of session file user wants to open. The function returns a (file name/location, file type) tuple but its indexed at 0 to just get file name
        fileNameAndLocation = QtGui.QFileDialog.getOpenFileName(parent = mainWindow.centralwidget, caption = "Open Session For Playback", directory = JSONConverter.getSavedSessionDirectory(createIfNonexistent = True), filter = "JSON (*.json)")[0]
    
    else:
        fileNameAndLocation = fileStr
        
    #If user didn't click cancel on "Open", proceed for opening session in playback mode
    if len(fileNameAndLocation) > 0:

        #Opening a session means going into playback mode
        setPlayMode(PlayMode.PLAYBACK)

        #Load in the session from the JSON file
        errorMessage = JSONConverter.openJSONFile(fileNameAndLocation, True)
        
        #Check if there was an error before proceeding
        if errorMessage:

            #Craft error message
            fullMessage = "Cannot read session file for the following reason...\n\n" + errorMessage

            #Notify user
            cannotReadSession = QMessageBox()
            cannotReadSession.setText(fullMessage)
            cannotReadSession.setWindowTitle("Error Opening Session")
            cannotReadSession.setStandardButtons(QMessageBox.Ok)
            cannotReadSession.setIcon(QMessageBox.Critical)
            cannotReadSession.setFont(popUpFont)
            cannotReadSession.exec()

            #In case a session was created, clear it (there shouldn't be though, just being safe)
            if ts.currentSession:
                stopSessionWithoutConfirmation()

            #Return to data acquisition mode
            setPlayMode(PlayMode.ACQUISITION)

        else:

            #Display the first trial of the session on the graph
            tg.createTrialGraph()

    else:

        #User cancelled opening a session so default back to empty, ready to start data acquisition mode
        setPlayMode(PlayMode.ACQUISITION)


#Use this to change the playMode variable, do not assign to it directly
def setPlayMode(newPlayMode):

    global playMode

    #Can only change the play mode when there is no ongoing session
    if ts.currentSession:
        return

    #On program start, this is called to set the initial play mode...
    #which also initializes singleton instance of acquisition parameters
    if not playMode:
        ts.acquisitionParameters = ts.TheSession(mainWindow)

    #Before switching, perform necessary clean up for previous play mode
    #i.e. remember latest data acquisition mode parameters
    #ts.currentSession is wiped when done running session, but this remains
    elif playMode == PlayMode.ACQUISITION:
        ts.acquisitionParameters.readInSettingsFromGUI(mainWindow)

    #Remember new play mode
    playMode = newPlayMode

    #Update text that indicates play mode
    updateSessionInfoLabel()

    #Show buttons that belong to that play mode and hide buttons that do not. Also do hide before show so that the layout doesn't get stretched from excess shown buttons
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

    #Enabled/disable menu actions that only work for a particular play mode
    mainWindow.actionRe_Analyze_Session.setEnabled(playMode == PlayMode.PLAYBACK)
    mainWindow.actionGenerate_Matrix_View.setEnabled(playMode == PlayMode.PLAYBACK)
    mainWindow.actionGoToTrial.setEnabled(playMode == PlayMode.PLAYBACK)

    #Lock settings in playback, unlock settings in data acquisition (session cannot be ongoing)
    mainWindow.lockButton.setEnabled(playMode == PlayMode.ACQUISITION)
    setLockModeForSettings(playMode == PlayMode.PLAYBACK)

    #Playback immediately opens session (so stop should be accessible), but opposite for acquisition
    mainWindow.stopButton.setEnabled(playMode == PlayMode.PLAYBACK)

    #When entering data acquisition, restore data acquisition parameters
    if playMode == PlayMode.ACQUISITION:
        ts.acquisitionParameters.outputSettingsToGUI(mainWindow)


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


#No longer needed with advent of parameter files
'''
#Resets all setting fields on the UI to have their default values
def resetSettingsToDefaults():
    #Session settings
    mainWindow.sessionNameLineEdit.setText("")
    mainWindow.subjectAgeSpinBox.setValue(30)
    mainWindow.subjectSexComboBox.setCurrentIndex(0)
    mainWindow.sampleIntervalSpinBox.setValue(1)
    mainWindow.trialCountSpinBox.setValue(25)
    mainWindow.itiSpinBox.setValue(15)
    mainWindow.itiVarianceSpinBox.setValue(3)
    mainWindow.thresholdSDSpinBox.setValue(4)
    mainWindow.thresholdMinDurSpinBox.setValue(10)

    #Trial settings
    mainWindow.trialDurationSpinBox.setValue(3000)
    mainWindow.baselineDurationSpinBox.setValue(1000)
    mainWindow.csNameLineEdit.setText("Tone")
    mainWindow.csDurationSpinBox.setValue(100)
    mainWindow.interstimulusIntervalSpinBox.setValue(500)
    mainWindow.usNameLineEdit.setText("Air Puff")
    mainWindow.usDurationSpinBox.setValue(100)
    mainWindow.usDelaySpinBox.setValue(0)
'''

#Closes all windows upon crash
def closeWindowsOnCrash():

    global programCrashing
    programCrashing = True
    QtGui.QApplication.instance().closeAllWindows()
