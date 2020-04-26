from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QApplication, QProgressDialog, QDialog, QLabel
import TheSession as ts
import InputManager as im
import MatrixViewWindow as mvw

#Call this to do the whole thingy-ma-doodle
def generateMatrixView():
    #First, populate the global trialCaptures list
    generateTrialCaptures()

    #Then, display matrix window using the data from that list
    openMatrixViewMenu()

#Populates the global trialCaptures list
def generateTrialCaptures():
    #Feature only available for playback of session
    #This is just to be safe, you shouldn't even be able to call this method if it won't work
    if im.playMode == im.PlayMode.ACQUISITION or (not ts.currentSession):
        return

    #Remember what trial we were originally on so we can go back to it after this
    originalTrialNumber = ts.currentSession.currentTrial

    #Define parameters
    trialImageWidth = 400
    trialCount = ts.currentSession.trialCount

    #Initialize trial captures list as empty list
    global trialCaptures
    trialCaptures = []

    #Create progress bar pop up (specify flags to remove "?" button on top of window)
    inProgress = QProgressDialog(flags = Qt.WindowSystemMenuHint | Qt.WindowTitleHint)

    #Customize progress bar
    inProgress.setLabelText("Preparing for trial capture...")
    inProgress.setWindowTitle("Generating Matrix View...")
    inProgress.setFixedWidth(350)   #Really skinny otherwise
    inProgress.setWindowModality(Qt.ApplicationModal)    #Blocks user control of other windows
    inProgress.setMaximum(trialCount) #Number of steps in progress bar = number of trials

    #Show progress bar
    inProgress.show()

    #For every trial (in order)...
    #Display on graph, take screenshot, change size of screenshot, save screenshot in list
    for trialNumber in range(1, trialCount + 1):
        #Update progress text
        inProgress.setLabelText("Capturing trial " + str(trialNumber) + " / " + str(trialCount) + "...")

        #Display trial on graph
        im.loadTrial(trialNumber)

        #Let the UI update itself (you get errors about not being able to capture a 0 by 0 graph otherwise)
        QApplication.processEvents()

        #Capture graph (i.e. capture trial)
        trialCapture = im.capture("Graph", True)

        #Resize capture (mode specifies to do it without any smoothing to save performance)
        trialCapture = trialCapture.scaledToWidth(trialImageWidth, mode = Qt.FastTransformation)

        #Save capture in list
        trialCaptures.append(trialCapture)

        #Update progress bar
        inProgress.setValue(trialNumber)

        #User clicked cancel on operation so break out of work loop
        if inProgress.wasCanceled():
            break

    #Reset graph to display trial it had before this function was called
    #We should do this regard of if the operation is cancelled (hence before return statement below)
    im.loadTrial(originalTrialNumber)

    #User clicked cancel on operation so stop
    if inProgress.wasCanceled():
        return

#Called to open the matrix view window
def openMatrixViewMenu():
    global matrixViewWrapper

    #Create the matrix view window (using the Qt Designer-generated Ui_Dialog)
    matrixViewWindow = QDialog()
    matrixViewWrapper = mvw.Ui_Dialog()
    matrixViewWrapper.setupUi(matrixViewWindow)

    #Fill the window with the trial screenshots
    loadTrialsIntoGridLayout()

    #Display the window
    matrixViewWindow.exec()

#Fill the window with the trial screenshots
def loadTrialsIntoGridLayout():
    gridLayout = matrixViewWrapper.trialGridLayout

    #For reference
    trialCount = len(trialCaptures)

    #Define number of rows and columns
    rows = 2
    columns = trialCount // rows #Integer division
    if columns == 0:
        columns = 1
    elif trialCount % rows > 0: #Add left over column if needed
        columns += 1

    #Add each trial capture to grid layout in order
    currentTrialIndex = 0
    for row in range(rows):
        for column in range(columns):
            #Make sure there are still trial captures left to add
            if currentTrialIndex == trialCount:
                break

            #Cannot add screenshots (of type QPixMap) directly to grid layout
            #So create empty label, add image to it, then add to layout (genius)
            surroundingLabel = QLabel() #"Trial " + str(currentTrialIndex + 1)
            surroundingLabel.setPixmap(trialCaptures[currentTrialIndex])

            #Add trial capture (screenshot) to graph in (row, column)
            gridLayout.addWidget(surroundingLabel, row, column)

            #Move onto next trial capture
            currentTrialIndex += 1