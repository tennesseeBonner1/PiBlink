from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QApplication, QProgressDialog, QDialog, QLabel
from PyQt5.QtGui import QFileDialog
import TheSession as ts
import InputManager as im
import MatrixViewWindow as mvw
import MatrixParametersWindow as mpw
import math

#Call this to do the whole thingy-ma-doodle
def generateMatrixView():
    #First, ask the user what the parameters for the matrix should be
    operationCancelled = getMatrixParameters()
    if operationCancelled:
        return

    #Then, populate the global trialCaptures list
    operationCancelled = generateTrialCaptures()
    if operationCancelled:
        return

    #Finally, display matrix window using the data from that list
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
        trialCapture = trialCapture.scaled(trialWidth, trialHeight,
                                           transformMode = Qt.FastTransformation)

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

    #Return whether operation was cancelled
    return inProgress.wasCanceled()

#Called to open the matrix view window
def openMatrixViewMenu():
    global matrixViewWrapper, matrixViewWindow

    #Create the matrix view window (using the Qt Designer-generated Ui_Dialog)
    matrixViewWindow = QDialog()
    matrixViewWrapper = mvw.Ui_matrixViewDialog()
    matrixViewWrapper.setupUi(matrixViewWindow)

    #Fill the window with the trial screenshots
    loadTrialsIntoGridLayout()
    
    #Connect window buttons to handlers
    matrixViewWrapper.saveButton.clicked.connect(saveMatrixAsImage)
    matrixViewWrapper.regenerateButton.clicked.connect(changeParameters)
    matrixViewWrapper.closeButton.clicked.connect(matrixViewWindow.close)
    matrixViewWrapper.previousButton.clicked.connect(previousPage)
    matrixViewWrapper.nextButton.clicked.connect(nextPage)

    #Display the window
    matrixViewWindow.exec()

#Called to close matrix view and reopen parameter window
def changeParameters():
    matrixViewWindow.close()
    generateMatrixView()

#Fill the window with the trial screenshots
def loadTrialsIntoGridLayout():
    global trialsPerPage, totalPageCount

    #Perform some preliminary computations
    computeMaxTrialsPerRowAndColumn()
    trialsPerPage = maxTrialsPerRow * maxTrialsPerColumn
    totalPageCount = math.ceil(len(trialCaptures) / trialsPerPage)

    #Start with page 1
    loadPage(1)

def nextPage():
    loadPage(pageNumber + 1)

def previousPage():
    loadPage(pageNumber - 1)

def loadPage(newPageNumber):
    if newPageNumber < 1:
        newPageNumber = totalPageCount
    elif newPageNumber > totalPageCount:
        newPageNumber = 1

    loadPageNoChecks(newPageNumber)

def loadPageNoChecks(newPageNumber):
    global pageNumber, trialCount, loadedTrials

    clearGridLayout()

    pageNumber = newPageNumber
    trialCount = len(trialCaptures)

    gridLayout = matrixViewWrapper.gridLayout
    
    gridLayout.setSpacing(spacing)

    matrixViewWrapper.pageNumberLabel.setText("Page " + str(pageNumber) + "/" + str(totalPageCount))
    
    currentTrialIndex = trialsPerPage * (pageNumber - 1)
    startingTrial = currentTrialIndex + 1

    #Add each trial capture to grid layout in order
    for row in range(maxTrialsPerColumn):
        for column in range(maxTrialsPerRow):
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

    matrixViewWrapper.gridInfoLabel.setText("Showing trials " + str(startingTrial) + "-"
                                        + str(currentTrialIndex) + " of " + str(trialCount) + ":")

def clearGridLayout():
    gridLayout = matrixViewWrapper.gridLayout

    #https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt/13103617
    for x in reversed(range(gridLayout.count())):
        gridLayout.itemAt(x).widget().setParent(None)

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

#Opens the matrix parameters window and saves the chosen parameters as global variables
def getMatrixParameters():
    global matrixParametersWrapper

    #Create the matrix parameters window (using the Qt Designer-generated Ui_trialMatrixParametersDialog)
    matrixParametersWindow = QDialog()
    matrixParametersWrapper = mpw.Ui_trialMatrixParametersDialog()
    matrixParametersWrapper.setupUi(matrixParametersWindow)

    #Make the window not resizable
    matrixParametersWindow.setFixedSize(matrixParametersWindow.size())

    #Connect window buttons to handlers
    matrixParametersWrapper.cancelButton.clicked.connect(
        lambda: matrixParametersWindow.done(QDialog.Rejected))
    matrixParametersWrapper.generateButton.clicked.connect(
        lambda: parametersAccepted(matrixParametersWindow))

    #Make values automatically adjust to each other (to maintain aspect ratio for example)
    matrixParametersWrapper.trialWidthSpinBox.valueChanged.connect(trialWidthChanged)
    matrixParametersWrapper.trialHeightSpinBox.valueChanged.connect(preventZeroTrialsPerPage)
    matrixParametersWrapper.pageWidthSpinBox.valueChanged.connect(preventZeroTrialsPerPage)
    matrixParametersWrapper.pageHeightSpinBox.valueChanged.connect(preventZeroTrialsPerPage)

    #Set the trial width and height defaults to current size of trial on graph
    matrixParametersWrapper.trialWidthSpinBox.setValue(im.mainWindow.graphWidget.width())

    #Initialize parameters to default ones displayed on the window
    readInParametersFromWindow()

    #Display the window
    result = matrixParametersWindow.exec()

    #Let the calling procedure know if cancel or "X" was pressed
    return result == QDialog.Rejected

#Set global parameters to those currently displayed on parameters window
def readInParametersFromWindow():
    global trialWidth, trialHeight, spacing, maxPageWidth, maxPageHeight, maxRows, maxColumns

    trialWidth = matrixParametersWrapper.trialWidthSpinBox.value()
    trialHeight = matrixParametersWrapper.trialHeightSpinBox.value()

    spacing = matrixParametersWrapper.spacingSpinBox.value()

    maxPageWidth = matrixParametersWrapper.pageWidthSpinBox.value()
    maxPageHeight = matrixParametersWrapper.pageHeightSpinBox.value()

    maxRows = matrixParametersWrapper.maxRowsSpinBox.value()
    maxColumns = matrixParametersWrapper.maxColumnsSpinBox.value()

#User clicked generate button on matrix parameters window
def parametersAccepted(matrixParametersWindow):
    #Save parameters
    readInParametersFromWindow()

    #Close window with accepted state (Cancel and "X" buttons close window with rejected state)
    matrixParametersWindow.done(QDialog.Accepted)

def trialWidthChanged(newWidth):
    #Change height to maintain aspect ratio
    aspectRatio = im.mainWindow.graphWidget.width() / im.mainWindow.graphWidget.height()
    matrixParametersWrapper.trialHeightSpinBox.setValue(int(newWidth / aspectRatio))

    preventZeroTrialsPerPage()

def preventZeroTrialsPerPage():
    trialWidth = matrixParametersWrapper.trialWidthSpinBox.value()
    trialHeight = matrixParametersWrapper.trialHeightSpinBox.value()

    maxPageWidth = matrixParametersWrapper.pageWidthSpinBox.value()
    maxPageHeight = matrixParametersWrapper.pageHeightSpinBox.value()

    if trialWidth > maxPageWidth:
        matrixParametersWrapper.pageWidthSpinBox.setValue(trialWidth)

    if trialHeight > maxPageHeight:
        matrixParametersWrapper.pageHeightSpinBox.setValue(trialHeight)

def computeMaxTrialsPerRowAndColumn():
    global maxTrialsPerRow, maxTrialsPerColumn

    #Compute max trials per row
    currentWidth = 0
    for trial in range(1, maxColumns + 1): 
        #Add trial width
        currentWidth += trialWidth
        if currentWidth > maxPageWidth:
            break

        maxTrialsPerRow = trial

        #Add spacing
        currentWidth += spacing

    #Compute max trials per column
    currentHeight = 0
    for trial in range(1, maxRows + 1): 
        #Add trial height
        currentHeight += trialHeight
        if currentHeight > maxPageHeight:
            break

        maxTrialsPerColumn = trial

        #Add spacing
        currentHeight += spacing