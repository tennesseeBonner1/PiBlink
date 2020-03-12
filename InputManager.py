from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox, QApplication
import TheGraph as tg
import TheSession as ts

#Called on start of program to perform all needed initialization
#Need initialization for default values, references, button icons, and button handlers
def initialSetUp (theMainWindow, thePlayIcon, theUnlockedIcon):

    global settingsLocked, mainWindow, playIcon, pauseIcon, unlockedIcon, lockedIcon
    
    #If false you can change the trial, session or system settings
    settingsLocked = False

    #Sets the mainWindow, playIcon and UnlockedIcon to the variables that were passed
    mainWindow = theMainWindow
    playIcon = thePlayIcon
    unlockedIcon = theUnlockedIcon
    
    #Sets the icon for the pause button
    pauseIcon = QtGui.QIcon()
    pauseIcon.addPixmap(QtGui.QPixmap("Images/Pause Button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

    #Sets the icon for the locked Button
    lockedIcon = QtGui.QIcon()
    lockedIcon.addPixmap(QtGui.QPixmap("Images/Locked Button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

    connectButtons()

#Connects buttons to their handlers (handlers are the functions called on button clicks)
def connectButtons ():
    #Detects when the play, stop and lock buttons are pushed
    mainWindow.playButton.clicked.connect(playButtonPressed)
    mainWindow.stopButton.clicked.connect(stopButtonPressed)
    mainWindow.lockButton.clicked.connect(lockButtonPressed)

    #Detects menu actions such as "File -> Close" and "File -> Screencapture"
    mainWindow.actionClose.triggered.connect(closeWindow)
    mainWindow.actionScreenCapture.triggered.connect(captureScreen)

    #Override close event function of QMainWindow for purpose of adding "are you sure you want to quit?" prompt
    mainWindow.centralwidget.parentWidget().closeEvent = closeEvent

#When the lock button is pressed
def lockButtonPressed ():

    #If the settings are locked already, attempt to unlock using setLockModeForSettings
    if settingsLocked:
        setLockModeForSettings(False)
    
    #Otherwise try and lock, by verifying that the trial duration is valid
    elif trialDurationIsValid():
        setLockModeForSettings(True)
    
    #If the trial duration is invalid, let the user know
    else:
        invalidSettingsNotice = QMessageBox()
        invalidSettingsNotice.setText(
            "Trial duration must be greater than or equal to baseline + CS + ISI + US!")
        invalidSettingsNotice.setWindowTitle("Invalid Settings")
        invalidSettingsNotice.setStandardButtons(QMessageBox.Ok)
        invalidSettingsNotice.exec()

#If the play button is pressed, set playing to the opposite of tg.isPlaying
def playButtonPressed ():
    setPlaying(not tg.isPlaying())

#If the stop button is pressed 
def stopButtonPressed ():

    #Pauses when stop is pressed
    if (tg.isPlaying()):    
        setPlaying(not tg.isPlaying())

    #Confirm that this is what the user wants
    confirmStop = QMessageBox()
    confirmStop.setText("Are you sure you want to stop the current session?")
    confirmStop.setWindowTitle("Confirm Stop")
    confirmStop.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    decision = confirmStop.exec()

    #If it is, stop the session
    if decision == QMessageBox.Yes:
        stopSession()
        
#Tell the window (QMainWindow) to close (this will then be intercepted by the close event function below)
def closeWindow ():
    mainWindow.centralwidget.parentWidget().close()

#Whenever the window is supposed to close, this event intercepts/overrides the default close event
def closeEvent (event):
    #If there is an ongoing session
    if ts.currentSession:
        #Display a "are you sure?" message
        confirmClose = QMessageBox()
        confirmClose.setText("Closing will end the current session. Are you sure you want to close?")
        confirmClose.setWindowTitle("Confirm Close")
        confirmClose.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        decision = confirmClose.exec()

        #If NOT sure, ignore event and return, else fall through to close code
        if decision != QMessageBox.Yes:
            event.ignore() #Do not close window
            return

    #Closes the QMainWindow, which closes the program
    event.accept()

#Defines whether or not the trial is playing
def setPlaying (play):

    #Gets the current session
    if not ts.currentSession:
        ts.currentSession = ts.TheSession(mainWindow)

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

#Returns whether or not the trial duration is valid based on the various other durations
def trialDurationIsValid ():
    beginningToEndOfUS = mainWindow.baselineDurationSpinBox.value()
    beginningToEndOfUS += mainWindow.csDurationSpinBox.value()
    beginningToEndOfUS += mainWindow.interstimulusIntervalSpinBox.value()
    beginningToEndOfUS += mainWindow.usDurationSpinBox.value()

    return mainWindow.trialDurationSpinBox.value() >= beginningToEndOfUS

#Sets the defaults for the names if this function is called
def assignDefaultsToEmptyFields ():
    if not mainWindow.csNameLineEdit.text():
        mainWindow.csNameLineEdit.setText(mainWindow.csNameLineEdit.placeholderText())

    if not mainWindow.usNameLineEdit.text():
        mainWindow.usNameLineEdit.setText(mainWindow.usNameLineEdit.placeholderText())

#Stops the session entirely
def stopSession ():
    
    #Clears the session
    ts.currentSession = None

    #Resets the graph
    tg.resetGraph()

    #Stops playing the graph
    tg.setPlaying(False)

    #Resets the play, stop, and lock buttons
    mainWindow.playButton.setIcon(playIcon)
    mainWindow.stopButton.setEnabled(False)
    mainWindow.lockButton.setEnabled(True)

#Takes a screenshot and saves it to the root folder of the project
def captureScreen ():
    #Take shot of entire screen/desktop
    #screenshot = QApplication.primaryScreen().grabWindow(0)

    #Take shot of main window
    screenshot = mainWindow.centralwidget.grab()

    #Take shot of graph
    #screenshot = mainWindow.graphWidget.grab()

    #Save screenshot
    screenshot.save('screenshot.jpg', 'jpg')

