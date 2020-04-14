from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox, QApplication
import TheGraph as tg
import TheSession as ts
import DisplaySettingsManager as dsm
import GraphExporter
import JSONConverter


arr = []
iterex = None

class bi_iterator(object):
    def __init__(self, collection):
        self.collection = collection
        self.index = 0

    def next(self):
        try:
            result = self.collection[self.index]
            self.index += 1
            return result
        except IndexError:
            self.index = len(self.collection)
            #raise StopIteration
        

    def prev(self):
        self.index -= 1
        if self.index < 0:
            self.index = 0
            raise StopIteration
        return self.collection[self.index]

    def __iter__(self):
        return self

#previous Clicked
def previousPressed():
    
    global arr, iterex
    try:
        openSession(iterex.prev())
    except Exception as e:
        print(str(e))
##    print(str(position))
##    print("ds")
##    if position == 0 or position == None or position < 0:
##        print(position)
##        openSession(arr[0])
##        return
##    if position == len(arr):
##        position = position - 2
##        openSession(arr[position])
##        position = position - 1
##        print(position)
##        return
##    openSession(arr[position])
##    position = position - 1
##    print(position)
#next clicked
def nextPressed():
    
    global iterex, arr
    try:
        openSession(iterex.next())
    except Exception as e:
        print(str(e))
##    print(str(position))
##    print("next")
##    if (position == len(arr)):
##        print(position)
##        return
##    if (position == None):
##        position = 0
##        openSession(arr[position])
##        position = position +1
##        print(position)
##        return
##    if (position == 0):
##        position = position +1
##        openSession(arr[position])
##        print(position)
##        return
##    openSession(arr[position])
##    position = position +1
##    print(position)
#Called on start of program to perform all needed initialization
#Need initialization for default values, references, button icons, and button handlers
def initialSetUp (theMainWindow, thePlayIcon, theUnlockedIcon):

    global settingsLocked, mainWindow, playIcon, pauseIcon, unlockedIcon, lockedIcon, arr, iterex
    
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

    previousTrialIcon = QtGui.QIcon()
    previousTrialIcon.addPixmap(QtGui.QPixmap("Images/Previous_Button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

    nextTrialIcon = QtGui.QIcon()
    nextTrialIcon.addPixmap(QtGui.QPixmap("Images/Previous_Button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    
    mainWindow.previousButton.clicked.connect(previousPressed)
    mainWindow.nextButton.clicked.connect(nextPressed)
    connectButtons()
    
    arr = []
    import os
    for file in os.listdir("./"):
        if file.endswith(".json"):
            print(os.path.join("./", file))
            arr.append(os.path.join("./", file))

    print(arr)
    iterex = bi_iterator(arr)
    

#Connects buttons to their handlers (handlers are the functions called on button clicks)
def connectButtons ():
    #Detects when the lock, play, and stop buttons are pressed respectively
    mainWindow.lockButton.clicked.connect(lockButtonPressed)
    mainWindow.playButton.clicked.connect(playButtonPressed)
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

#When the play button is pressed, toggle play status
def playButtonPressed ():
    setPlaying(not tg.isPlaying())

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

    #Closes the QMainWindow, which closes the program
    event.accept()


    
#Defines whether or not the trial is playing
def setPlaying (play):
    #Creates a session if one is not already running (there must be a current session to control)
    if not ts.currentSession:
        ts.currentSession = ts.TheSession(mainWindow)
        if tg.playMode == tg.PlayMode.ACQUISITION:
            JSONConverter.startDataAcquisition()
    elif tg.done and tg.playMode == tg.PlayMode.PLAYBACK: #Restart playback of session
        #Get rid of done label
        tg.graphWindow.clear()
        tg.graphWindow.setBackground(None)

        #Start over with first trial
        ts.currentSession.currentTrial = 1
        JSONConverter.openFirstTrial()

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

#Stop session and only ask for confirmation if appropriate (i.e. if data acquisition is ongoing)
#Asking for confirmation means a "are you sure" dialog box pops up and you can say yes or no
def stopSessionConditionalConfirmation ():
    #Ask for confirmation only if data acquisition is ongoing
    if (not tg.done) and tg.playMode == tg.PlayMode.ACQUISITION:
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
    decision = confirmStop.exec()

    #If it is, stop the session
    if decision == QMessageBox.Yes:
        stopSessionWithoutConfirmation()

#Stops the session immediately without asking user
def stopSessionWithoutConfirmation ():
    #Save data acquisition session
    if tg.playMode == tg.PlayMode.ACQUISITION:
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
    tg.setPlayMode(tg.PlayMode.ACQUISITION)

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

    #Creating new graphs means being in data acquisition mode
    tg.setPlayMode(tg.PlayMode.ACQUISITION)

    #Now that we are back in data acquisition mode, we can lock/unlock
    mainWindow.lockButton.setEnabled(True)

    #Start with default settings again
    resetSettingsToDefaults()

    #Go back to editing settings
    setLockModeForSettings(False)

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
        tg.setPlayMode(tg.PlayMode.PLAYBACK)

        #Shouldn't be able to edit settings of playback session
        setLockModeForSettings(True) #Lock settings
        mainWindow.lockButton.setEnabled(False) #Lock the lock (genius)

        JSONConverter.openSession(fileNameAndLocation)
    else:
        #User cancelled opening a session so default back to empty, ready to start data acquisition mode
        tg.setPlayMode(tg.PlayMode.ACQUISITION)

def openSession(file):
    #You must first close the current session 
    if ts.currentSession:
        stopSessionConditionalConfirmation()

        #If user says no to stopping current session, then cancel opening another
        if ts.currentSession:
            return

    #Pop up "Open" window to retrieve file name and location of session file user wants to open
    #The function returns a (file name/location, file type) tuple but I index it at 0 to just get file name
    fileNameAndLocation = file

    #If user didn't click cancel on "Open", proceed for opening session in playback mode
    if fileNameAndLocation !=None :
        #Opening a session means going into playback mode
        tg.setPlayMode(tg.PlayMode.PLAYBACK)

        #Shouldn't be able to edit settings of playback session
        setLockModeForSettings(True) #Lock settings
        mainWindow.lockButton.setEnabled(False) #Lock the lock (genius)

        JSONConverter.openSession(fileNameAndLocation)
    else:
        #User cancelled opening a session so default back to empty, ready to start data acquisition mode
        tg.setPlayMode(tg.PlayMode.ACQUISITION)

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
