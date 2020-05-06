""" TheGraph.py
    Last Modified: 5/6/2020
    Taha Arshad, Tennessee Bonner, Devin Mensah, Khalid Shaik, Collin Vaille

    This file is responsible for implementing all operations related to the graph displayed on the
    main window.

    More specifically, it implements the operations for creating, updating, clearing, pausing/resuming,
    and annotating (adding arrows to) the graph. The emphasis here is on implementing the code to
    make them work, not the code for managing the logic of when they should happen. Other files,
    particularly input manager, act as the driver/controller for when they should be called.
"""
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import TheSession as ts
import timeit
import DisplaySettingsManager as dsm
import JSONConverter
import InputManager as im
import DataAnalysis as da
import TimeCriticalOperations as tco


#Helper methods used later on
def clamp(value, minimum, maximum):

    return min(maximum, max(minimum, value))


#Converts the colors
def htmlColorString(qtColor):

    return "rgb(" + str(qtColor.red()) + ", " + str(qtColor.blue()) + ", " + str(qtColor.green()) + ")"


#Initializes global variables that need to have default values or references to objects in main window
def initialSetUp(theMainWindow):

    global graphInitialized, playing, duringITI, done, mainWindow, graphWindow

    graphInitialized = False
    playing = False
    duringITI = False
    done = False

    #Graph settings on main window
    mainWindow = theMainWindow
    graphWindow = theMainWindow.graphWidget

    #Also set the "color" of the blank graph screen
    graphWindow.setBackground(None)


#Whether or not the graph is playing
def isPlaying():

    return playing


#Sets the graph's play status to parameter (i.e. true = playing, false = paused)
def setPlaying(play):

    global playing, duringITI, graphInitialized
    
    playing = play

    #During data acquisition, synch time critical process to be in same play state
    if im.playMode == im.PlayMode.ACQUISITION:
        tco.orderToSetPlaying(play)

    #When we press play and there is no graph, create one
    #Need to check duringITI b/c graph is not initialized during ITI but ITI
    #shouldn't be interrupted
    if play and (not graphInitialized) and (not duringITI):
        createGraph()


#Resets the graph (removes graph window and is ready for new call to createGraph)
def resetGraph():

    global playing, graphInitialized, duringITI, done

    #Reset variables
    playing = False
    graphInitialized = False
    done = False

    #Stop timers
    displayTimer.stop()
    itiTimer.stop()

    #In case this was called during ITI, stop ITI
    duringITI = False

    #Clear the graph
    graphWindow.clear()
    graphWindow.setBackground(None)


#Creates the graph
def createGraph():

    #Variables that persist outside this function call
    global iteration, curve, stimulusGraph, dataSize, data, bars, barHeights, graphInitialized, playing, done, previousITI

    #Update the session info label in the main window to reflect trial number
    im.updateSessionInfoLabel()

    #Define settings
    dataColor = dsm.colors[dsm.ColorAttribute.DATA.value]
    textColor = dsm.colors[dsm.ColorAttribute.TEXT.value]
    stimulusColor = dsm.colors[dsm.ColorAttribute.STIMULUS.value]
    stimulusColor.setAlpha(75) #Give it some transparency since it renders on top of data curve
    axisColor = pg.mkPen(color = dsm.colors[dsm.ColorAttribute.AXIS.value], width = 1)
    graphWindow.setBackground(dsm.colors[dsm.ColorAttribute.BACKGROUND.value])

    #Enable antialiasing for prettier plots
    pg.setConfigOptions(antialias = dsm.antiAliasing)

    #Add bar graph only when in data acquisition mode (no use for it in playback)
    if im.playMode == im.PlayMode.ACQUISITION:

        #Create bar graph
        barGraph = graphWindow.addPlot()
        barGraph.setMaximumWidth(100)
        barGraph.hideAxis('bottom')
        barGraph.getAxis('left').setPen(axisColor)
        barGraph.setMouseEnabled(x = False, y = False)
        barGraph.enableAutoRange('xy', False)
        barGraph.setXRange(0, 1)
        barGraph.setYRange(0, 7)
        barGraph.setLimits(xMin = 0, xMax = 1, yMin = 0, yMax = 7)
        barGraph.hideButtons()
        barGraph.setMenuEnabled(False)

        #Create arrays of size 1 for both x location of bars and bar heights (both with values initialized to 0)
        barXs = np.zeros(1)
        barHeights = np.zeros(1)

        #Add that bar data to the graph along with other settings like width and color
        bars = pg.BarGraphItem(x = barXs, height = barHeights, width = 1.0, brush = dataColor)
        barGraph.addItem(bars)

    #Create data array (this array will be displayed as the line on the graph)
    dataSize = ts.currentSession.trialLengthInSamples #Array size
    data = np.full(shape = dataSize, fill_value = -7, dtype = np.float32) #initialized to -7 (so they're off-screen)
    
    #Create empty graph
    stimulusGraph = graphWindow.addPlot()

    #Plot line in graph
    if dsm.shading:
        curve = stimulusGraph.plot(y = data, fillLevel = -0.3, brush = dataColor)

    else:
        curve = stimulusGraph.plot(y = data, fillLevel = -0.3, pen = dataColor)

    #Add graph labels
    stimulusGraph.setLabel('bottom', "<span style = \"color: " + htmlColorString(textColor) + "; font-size:18px\">Time (ms)</span>")
    stimulusGraph.setLabel('left', "<span style = \"color: " + htmlColorString(textColor) + "; font-size:18px\">Eyeblink Amplitude (VDC)</span>")

    #Axis line/tick color
    stimulusGraph.getAxis('bottom').setPen(axisColor)
    stimulusGraph.getAxis('left').setPen(axisColor)

    #Axis limits on graph
    stimulusGraph.setLimits(xMin = 0, xMax = dataSize, yMin = 0, yMax = 7, minXRange = 10, minYRange = 7)

    #Scale x axis ticks to measure milliseconds instead of samples
    stimulusGraph.getAxis('bottom').setScale(ts.currentSession.sampleInterval)

    #Removes default "A" button on bottom left corner used for resetting the zoom on the graph
    stimulusGraph.hideButtons()

    #Disables the context menu you see when right-clicking on the graph
    stimulusGraph.setMenuEnabled(False)

    #Create CS lines and shaded area between lines
    csStart = ts.currentSession.csStartInSamples
    csEnd = ts.currentSession.csEndInSamples
    csRegion = pg.LinearRegionItem(values = [csStart, csEnd], brush = stimulusColor, movable = False)
    csRegion.lines[0].setPen(stimulusColor)
    csRegion.lines[1].setPen(stimulusColor)
    stimulusGraph.addItem(csRegion)

    #Add CS label to middle of shaded area
    csLabel = pg.TextItem(html = "<span style = \"font-size: 16pt; color: " + htmlColorString(textColor) + "\">CS</span>", color = textColor, anchor = (0.5, 0))
    stimulusGraph.addItem(csLabel)
    csLabel.setPos((csStart + csEnd) / 2, 7)

    #Same for US
    usStart = ts.currentSession.usStartInSamples
    usEnd = ts.currentSession.usEndInSamples
    usRegion = pg.LinearRegionItem(values = [usStart, usEnd], brush = stimulusColor, movable = False)
    usRegion.lines[0].setPen(stimulusColor)
    usRegion.lines[1].setPen(stimulusColor)
    stimulusGraph.addItem(usRegion)

    usLabel = pg.TextItem(html = "<span style = \"font-size: 16pt; color: " + htmlColorString(textColor) + "\">US</span>", anchor = (0.5, 0))
    stimulusGraph.addItem(usLabel)
    usLabel.setPos((usStart + usEnd) / 2, 7)

    #Launch graph based on play mode
    if im.playMode == im.PlayMode.PLAYBACK:

        #Update graph with array of samples for trial
        data = JSONConverter.openTrial()
        curve.setData(data)

        #The data for the eyeblinks should have already been calculated, so just read in the onsets to place the "Arrows"
        onsets = JSONConverter.getOnsets()
        arrowCap = min(len(onsets), 30)

        for x in range(arrowCap):
            addArrow(onsets[x] - 1)

    #Data Acquisition    
    else:

        #Regularly sample data (according to sample rate defined in session settings)
        iteration = 0
        if ts.currentSession.currentTrial == 1:
            tco.orderToStartSession()
            previousITI = 0 #First trial's previous ITI is 0

        #Regularly update display (according to display rate defined in display settings)
        displayTimer.start(1000 / dsm.displayRate)

    #Done initializing/creating/launching the graph
    done = False #As in done with session, which we are not (we are just starting the session!!!)
    graphInitialized = True


#Updates the display
def displayUpdate():

    #Variables that need to be survive across multiple calls to update function
    global iteration, dataSize, curve, data, bars, barHeights, playing

    #Read in new samples
    while not tco.sampleQueue.empty():

        data[iteration] = tco.sampleQueue.get(block = False)

        iteration += 1
    
    #Update stimulus graph
    curve.setData(data)

    lastSample = iteration - 1

    #Update bar graph
    if lastSample != -1 and lastSample < dataSize:

        barHeights[0] = data[lastSample]
        bars.setOpts(height = barHeights)

    #End of trial?
    if iteration >= dataSize:
        endTrialStartITI()


#Create timer to run sample update function (start is called on the timer in createGraph function above)
displayTimer = QtCore.QTimer()
displayTimer.timeout.connect(displayUpdate)


def endTrialStartITI():

    global previousITI, duringITI, itiCountdown, countdownLabel, done

    #Save trial
    JSONConverter.saveTrial(data, int(previousITI))

    #Stop current trial
    resetGraph()

    #Don't start ITI because that was the last trial we just finished
    if ts.currentSession.currentTrial >= ts.currentSession.trialCount:
        done = True
        
        #Pause upon completion
        im.setPlaying(False)

        #Completion message...
        doneText = "Data acquisition complete! Press Stop to save the session."

        #Display completion message in place of graph
        graphWindow.addLabel(text = doneText, size = "18pt", color = "#000000", row = 0, col = 0)

        #Also, don't allow restart of data acquisition (functionality not supported)
        mainWindow.playButton.setEnabled(False)

        #Return before ITI starts
        return

    #Create countdown label "Next trial in..."
    graphWindow.addLabel(text = "Next trial in...", size = "20pt", color = "#000000", row = 0, col = 0)

    #Wait for start of ITI updates (if it takes TCO more than 3 seconds then raise hell!)
    itiCountdown = tco.itiQueue.get(timeout = 3)
    previousITI = itiCountdown

    #Create countdown label "X.X"
    countdownLabel = graphWindow.addLabel(text = "{:5.1f}".format(itiCountdown),
                                          size = "69pt", color = "#000000", row = 1, col = 0)

    #Begin ITI
    duringITI = True
    setPlaying(True)
    itiTimer.start(100) #Parameter is millisecond interval between updates


#Update the iti for the countdown
def itiUpdate():

    global itiCountdown

    #ITI can be paused
    if not playing:
        return

    #Update how long ITI has been going (countdown is in seconds)
    #Each item in the ITI queue was the latest countdown value at the time it was sent,
    #so just empty out queue and set countdown to latest push
    while not tco.itiQueue.empty():
        itiCountdown = tco.itiQueue.get(block = False)

    #Display updated countdown (format countdown from int to string with 1 decimal point precision)
    countdownLabel.setText(text = "{:5.1f}".format(itiCountdown))

    #Determine if ITI is over
    if itiCountdown <= 0:
        endITIStartTrial()


#Create timer to run ITI (start is called on the timer in startITI function above)
itiTimer = QtCore.QTimer()
itiTimer.timeout.connect(itiUpdate)
itiTimer.setTimerType(QtCore.Qt.PreciseTimer)


#Stop the ITI and begin the next trial
def endITIStartTrial():
    #Stop ITI (does the following: clear countdown from graph, duringITI = False, itiTimer.stop())
    resetGraph()

    #Increment trial count
    ts.currentSession.currentTrial += 1

    #Begin new trial (calls createGraph for us since no graph currently exists)
    setPlaying(True)


#Adds arrow on top of data at xPosition (in samples) on graph
def addArrow(xPositionInSamples):

    #Create arrow with style options Make sure to specify rotation in constructor, b/c there's a bug in PyQtGraph (or PyQt) where you can't update the rotation of the arrow after creation
    #See (http://www.pyqtgraph.org/documentation/graphicsItems/arrowitem.html) for options
    arrow = pg.ArrowItem(angle = -90, headLen = 25, headWidth = 25, brush = dsm.colors[dsm.ColorAttribute.AXIS.value])

    #Set arrow's x and y positions respectively
    arrow.setPos(xPositionInSamples, data[xPositionInSamples])

    #Finally, add arrow to graph
    stimulusGraph.addItem(arrow)
