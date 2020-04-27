from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QApplication, QProgressDialog, QDialog, QLabel
from PyQt5.QtGui import QFileDialog
import TheSession as ts
import InputManager as im
import MatrixViewWindow as mvw
import GridDimensionsWindow as gdw

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
    
    #Connect window buttons to handlers
    matrixViewWrapper.saveButton.clicked.connect(saveMatrixAsImage)
    matrixViewWrapper.regenerateButton.clicked.connect(openGridDimensionsMenu)
    matrixViewWrapper.closeButton.clicked.connect(matrixViewWindow.close)

    #Display the window
    matrixViewWindow.exec()

#Called to open the parameters menu for generating the matrix
def openGridDimensionsMenu():
    global gridDimensionsWrapper

    gridDimensionsWindow = QDialog()
    gridDimensionsWrapper = gdw.Ui_gridViewWindow()
    gridDimensionsWrapper.setupUi(gridDimensionsWindow)

    gridDimensionsWindow.exec()

def calculateRows(value):
    #Calculate all the numbers that the array's length can be divided by
    divisibles = []    
    for i in range(1, value):
        if (value % i == 0):
            divisibles.append(i)
            print("i " + str(i))
            
            if ((value // i) != i):
                divisibles.append(value // i)
                print("value // i " + str(value //i) )

    #Take the two closest values that the lengh can be divided by, and return a value in between those two
    if (len(divisibles) % 2 == 0):
        returnValue = divisibles[(len(divisibles) // 2)] - divisibles[(len(divisibles) // 2) - 1] 
        testValue = int(float(returnValue) // 2.0)
        returnValue = divisibles[(len(divisibles) // 2) - 1] + testValue
        return returnValue

    #return the centermost value of deliverables
    #EX: value = 9 (divisible by 1, 3 and 9) 
    else:
        if (len(divisibles) == 1):
            return divisibles[0]
        elif (len(divisibles) == 3):
            return divisibles[2]
        else:
            return divisibles[int(float(len(divisibles)) // 2.0)]

#Fill the window with the trial screenshots
def loadTrialsIntoGridLayout():
    gridLayout = matrixViewWrapper.trialGridLayout

    #For reference
    trialCount = len(trialCaptures)

    rows = calculateRows(trialCount)
    print("Rows should be " + str(rows)) 

    #Define number of rows and columns

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

def saveMatrixAsImage():
    #Take picture of the grid
    matrixAsImage = matrixViewWrapper.gridWidget.grab()

    #Pop up "Save As" window to retrieve file name and type to save as
    nameAndType = QFileDialog.getSaveFileName(parent = im.mainWindow.centralwidget,
                                                        caption = "Save Trial Matrix Capture As",
                                                        filter = "PNG (*.png);;JPG (*.jpg)")

    #If user didn't click cancel on "Save As", save screenshot using "Save As" options
    if len(nameAndType[0]) > 0:
        matrixAsImage.save(nameAndType[0], im.extractFileType(nameAndType[1]))