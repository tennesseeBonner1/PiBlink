""" MatrixManager.py
    Last Modified: 5/23/2020
    Taha Arshad, Tennessee Bonner, Devin Mensah, Khalid Shaik, Collin Vaille

    This file is responsible for managing...
    1. The Matrix Parameters Window (MatrixParametersWindow.py)
    2. The Matrix View Window (MatrixViewWindow.py)
    3. The act of collecting the images to display in the matrix view window.

    Essentially all things to do with the matrix view of trials.

    From the outside, call generateMatrixView() to launch the parameters window and begin
    the whole series of events.
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QProgressDialog, QDialog, QLabel, QMessageBox
from PyQt5.QtGui import QFileDialog
import TheSession as ts
import InputManager as im
import JSONConverter as jc
import MatrixViewWindow as mvw
import MatrixParametersWindow as mpw
import math
import traceback


#Perform all needed set up the first time this file is called
def initialSetUp():

    global trialDimensionsChanged

    trialDimensionsChanged = True

initialSetUp()


#Generates the Matrix View
def generateMatrixView(regenerating = False):

    #Get the parameters for the matrix should be
    operationCancelled = getMatrixParameters(regenerating)

    if operationCancelled:
        return

    #We can skip this if we are regenerating view with same trial dimensions
    if (not regenerating) or trialDimensionsChanged: 

        #Then, populate the global trialCaptures list
        operationCancelled = generateTrialCaptures()

        if operationCancelled:
            return

    #Finally, display matrix window using the data from that list
    openMatrixViewMenu()


#Populates the global trialCaptures list
def generateTrialCaptures():

    global trialCaptures

    #Feature only available for playback of session
    if im.playMode == im.PlayMode.ACQUISITION or (not ts.currentSession):
        return

    #Remember what trial we were originally on so we can go back to it after this
    originalTrialNumber = ts.currentSession.currentTrial

    #Define parameters
    trialCount = ts.currentSession.trialCount

    #Initialize trial captures list as empty list
    trialCaptures = []

    #Create progress bar pop up (specify flags to remove "?" button on top of window)
    #flags = Qt.WindowSystemMenuHint | Qt.WindowTitleHint
    inProgress = QProgressDialog()

    #Customize progress bar
    inProgress.setLabelText("Preparing for trial capture...")
    inProgress.setWindowTitle("Generating Matrix View...")
    inProgress.setFixedWidth(350)
    inProgress.setWindowModality(Qt.ApplicationModal) #Blocks user control of other windows
    inProgress.setMaximum(trialCount) #Number of steps in progress bar = number of trials
    inProgress.setFont(im.popUpFont)

    #Show progress bar
    inProgress.show()

    #Keep track of whether capture process was successful
    errorMessage = None

    #For every trial (in order) Display on graph, take screenshot, change size of screenshot, save screenshot in list
    for trialNumber in range(1, trialCount + 1):

        #Update progress text
        inProgress.setLabelText("Capturing trial " + str(trialNumber) + " / " + str(trialCount) + "...")

        #Display trial on graph
        im.loadTrial(trialNumber)

        #Let the UI update itself (you get errors about not being able to capture a 0 by 0 graph otherwise)
        QApplication.processEvents()

        #Try 5 times to capture trial
        errorMessage = None
        trialCapture = None
        for x in range(0, 5):
            try:    #Attempt to capture trial
                trialCapture = captureCurrentTrial()
            except Exception:  #Remember error message
                errorMessage = traceback.format_exc(10) #Limit to 10 lines
            else:   #Capture successful, so no need to try again
                errorMessage = None #Disregard any previous failed attempt
                break

        #If capture failed, stop capture process
        if errorMessage:
            break

        #Save capture in list
        trialCaptures.append(trialCapture)

        #Update progress bar
        inProgress.setValue(trialNumber)

        #User clicked cancel on operation so break out of work loop
        if inProgress.wasCanceled():
            break

    #Closing actions
    if errorMessage:
        #Notify user
        errorGeneratingMatrix = QMessageBox()
        errorGeneratingMatrix.setText("Error generating matrix view:\n\nCapture of trial " + 
                                      str(ts.currentSession.currentTrial) + " failed.\n\n" + 
                                      "Full error message:\n" + str(errorMessage))
        errorGeneratingMatrix.setWindowTitle("Error Generating Matrix")
        errorGeneratingMatrix.setStandardButtons(QMessageBox.Ok)
        errorGeneratingMatrix.setIcon(QMessageBox.Critical)
        errorGeneratingMatrix.setFont(im.popUpFont)
        errorGeneratingMatrix.exec()

        #Reset graph to display trial it had before this function was called
        im.loadTrial(originalTrialNumber)

        #Close progress bar by telling it we're done
        inProgress.setValue(ts.currentSession.trialCount)

        #Do not proceed with opening matrix view
        return True
    else:
        #Reset graph to display trial it had before this function was called
        im.loadTrial(originalTrialNumber)

        #Return whether operation was cancelled
        return inProgress.wasCanceled()


#Used by generateTrialCaptures to get scaled image of current trial
def captureCurrentTrial():
    #Capture graph (i.e. capture trial)
    trialCapture = im.capture("Graph", True)

    #Resize capture (mode specifies to do it without any smoothing to save performance)
    trialCapture = trialCapture.scaled(trialWidth, trialHeight, transformMode = Qt.FastTransformation)

    return trialCapture


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
    generateMatrixView(regenerating = True)


#Fill the window with the trial screenshots
def loadTrialsIntoGridLayout():

    global trialsPerPage, totalPageCount

    #Perform some preliminary computations
    computeMaxTrialsPerRowAndColumn()
    trialsPerPage = maxTrialsPerRow * maxTrialsPerColumn
    totalPageCount = math.ceil(len(trialCaptures) / trialsPerPage)

    #Start with page 1
    loadPage(1)


#Loads the preceding page
def nextPage():

    loadPage(pageNumber + 1)


#Loads the previous page
def previousPage():

    loadPage(pageNumber - 1)


#Load the page specified, wrapping around if page number is out of bounds
def loadPage(newPageNumber):

    if newPageNumber < 1:
        newPageNumber = totalPageCount

    elif newPageNumber > totalPageCount:
        newPageNumber = 1

    loadPageNoChecks(newPageNumber)


#Actual code for loading the page, ideally only loadPage will call this function to be safe
def loadPageNoChecks(newPageNumber):

    global pageNumber, trialCount, loadedTrials

    #Clear any previous page
    clearGridLayout()

    #Initialize variables
    pageNumber = newPageNumber
    trialCount = len(trialCaptures)
    gridLayout = matrixViewWrapper.gridLayout
    currentTrialIndex = trialsPerPage * (pageNumber - 1)
    startingTrial = currentTrialIndex + 1

    #Set spacing
    gridLayout.setSpacing(spacing)

    #Set page number display
    matrixViewWrapper.pageNumberLabel.setText("Page " + str(pageNumber) + "/" + str(totalPageCount))

    #Add each trial capture to grid layout in order (left to right, then up down)
    for row in range(maxTrialsPerColumn):
        for column in range(maxTrialsPerRow):
            #Make sure there are still trial captures left to add
            if currentTrialIndex == trialCount:
                break

            #Cannot add screenshots (of type QPixMap) directly to grid layout
            #So create empty label, add image to it, then add to layout (genius)
            surroundingLabel = QLabel() #"Trial " + str(currentTrialIndex + 1)
            surroundingLabel.setPixmap(trialCaptures[currentTrialIndex])
            surroundingLabel.setToolTip("Trial " + str(currentTrialIndex + 1))

            #Add trial capture (screenshot) to graph in (row, column)
            gridLayout.addWidget(surroundingLabel, row, column)

            #Move onto next trial capture
            currentTrialIndex += 1

    #Set the label above the matrix that denotes what trials are being shown
    matrixViewWrapper.trialNumbersLabel.setText("Showing trials " + str(startingTrial) + "-" + str(currentTrialIndex) + " of " + str(trialCount) + ":")

    #Set the label above the matrix that denotes what session the trials belong to
    matrixViewWrapper.sessionNameLabel.setText(jc.getCurrentFilename())


#Clears all widgets inside grid layout, effectively clearing any previous page
def clearGridLayout():

    gridLayout = matrixViewWrapper.gridLayout

    #https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt/13103617
    for x in reversed(range(gridLayout.count())):
        gridLayout.itemAt(x).widget().setParent(None)


#Save the image of the matrix view
def saveMatrixAsImage():

    #Take picture of the grid
    matrixAsImage = matrixViewWrapper.gridWidget.grab()

    #Pop up "Save As" window to retrieve file name and type to save as
    nameAndType = QFileDialog.getSaveFileName(parent = im.mainWindow.centralwidget, caption = "Save Trial Matrix Capture As", filter = "PNG (*.png);;JPG (*.jpg)")

    #If user didn't click cancel on "Save As", save screenshot using "Save As" options
    if len(nameAndType[0]) > 0:
        matrixAsImage.save(nameAndType[0], im.extractFileType(nameAndType[1]))


#Opens the matrix parameters window and saves the chosen parameters as global variables
def getMatrixParameters(regenerating):
    global matrixParametersWrapper, trialDimensionsChanged

    #Create the matrix parameters window (using the Qt Designer-generated Ui_trialMatrixParametersDialog)
    matrixParametersWindow = QDialog()
    matrixParametersWrapper = mpw.Ui_trialMatrixParametersDialog()
    matrixParametersWrapper.setupUi(matrixParametersWindow)

    #Make the window not resizable
    matrixParametersWindow.setFixedSize(matrixParametersWindow.size())

    #Connect window buttons to handlers
    matrixParametersWrapper.cancelButton.clicked.connect(lambda: matrixParametersWindow.done(QDialog.Rejected))
    matrixParametersWrapper.generateButton.clicked.connect(lambda: parametersAccepted(matrixParametersWindow))

    #Make values automatically adjust to each other (to maintain aspect ratio for example)
    matrixParametersWrapper.trialWidthSpinBox.valueChanged.connect(trialWidthChanged)

    #First time, or regenerating?
    if regenerating: #Remember settings on regeneration
        displayParametersOnWindow()

    #Initially, Set the trial width and height defaults to current size of trial on graph
    else:   
        matrixParametersWrapper.trialWidthSpinBox.setValue(im.mainWindow.trialGraphWidget.width())

    #Initialize parameters to default ones displayed on the window
    readInParametersFromWindow()

    #Record trial width and height so we know if they get changed
    originalTrialWidth = trialWidth
    originalTrialHeight = trialHeight

    #Display the window
    result = matrixParametersWindow.exec()

    #Report if trial captures changed size (so we know if we have to recapture them)
    trialDimensionsChanged = originalTrialWidth != trialWidth or originalTrialHeight != trialHeight

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

    #Make sure you can fit at least one trial per page
    if trialWidth > maxPageWidth:
        maxPageWidth = trialWidth

    if trialHeight > maxPageHeight:
            maxPageHeight = trialHeight


#Set display parameters to those currently saved in global variables (Used when "change parameters" button is pressed to remember parameters)
def displayParametersOnWindow():

    matrixParametersWrapper.trialWidthSpinBox.setValue(trialWidth)
    matrixParametersWrapper.trialHeightSpinBox.setValue(trialHeight)
    matrixParametersWrapper.spacingSpinBox.setValue(spacing)
    matrixParametersWrapper.pageWidthSpinBox.setValue(maxPageWidth)
    matrixParametersWrapper.pageHeightSpinBox.setValue(maxPageHeight)
    matrixParametersWrapper.maxRowsSpinBox.setValue(maxRows)
    matrixParametersWrapper.maxColumnsSpinBox.setValue(maxColumns)


#User clicked generate button on matrix parameters window
def parametersAccepted(matrixParametersWindow):

    #Save parameters
    readInParametersFromWindow()

    #Close window with accepted state (Cancel and "X" buttons close window with rejected state)
    matrixParametersWindow.done(QDialog.Accepted)


#Called the moment the trial width is changed inside the edit parameters window
def trialWidthChanged(newWidth):

    #Change height to maintain aspect ratio
    aspectRatio = im.mainWindow.trialGraphWidget.width() / im.mainWindow.trialGraphWidget.height()
    matrixParametersWrapper.trialHeightSpinBox.setValue(int(newWidth / aspectRatio))


#Called when matrix view window is created to simplify the computation. Considers trialWidth, spacing, maxPageWidth, and maxColumns to determine what the real maximum number of trials should be.
def computeMaxTrialsPerRowAndColumn():

    global maxTrialsPerRow, maxTrialsPerColumn

    currentWidth = 0

    #Compute max trials per row
    for trial in range(1, maxColumns + 1): 

        #Add trial width
        currentWidth += trialWidth

        if currentWidth > maxPageWidth:
            break

        #At this point we know another trial will fit in the row
        maxTrialsPerRow = trial

        #Add spacing
        currentWidth += spacing

    #Compute max trials per column
    currentHeight = 0

    #Compute max trials per row
    for trial in range(1, maxRows + 1): 
        
        #Add trial height
        currentHeight += trialHeight
        
        if currentHeight > maxPageHeight:
            break

        #At this point we know another trial will fit in the column
        maxTrialsPerColumn = trial

        #Add spacing
        currentHeight += spacing
