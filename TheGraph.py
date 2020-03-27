from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import TheSession as ts
import datetime as dt
import DisplaySettingsManager as dsm
import NoiseWizard as dw

#Helper methods used later on
def clamp(value, minimum, maximum):
    return min(maximum, max(minimum, value))

#Converts the colors
def htmlColorString(qtColor):
    return "rgb(" + str(qtColor.red()) + ", " + str(qtColor.blue()) + ", " + str(qtColor.green()) + ")"

#Initializes global variables that need to have default values or references to objects in main window
def initialSetUp (theMainWindow):
    global graphInitialized, playing, duringITI, mainWindow, graphWindow
    global startedCS, csInProgress, startedUS, usInProgress

    graphInitialized = False
    playing = False
    duringITI = False

    # Graph settings on main window
    mainWindow = theMainWindow
    graphWindow = theMainWindow.graphWidget

    startedCS = csInProgress = startedUS = usInProgress = False

    #Also set the "color" of the blank graph screen
    graphWindow.setBackground(None)

#Whether or not the graph is playing
def isPlaying ():
    return playing

#Sets the graph's play status to parameter (i.e. true = playing, false = paused)
def setPlaying (play):
    global playing, duringITI, graphInitialized
    
    playing = play

    if not duringITI:
        if play:
            if graphInitialized == False:
               createGraph()
        else:
            assessAverage()

#Resets the graph (i.e. removes graph window and is ready for new call to createGraph)
def resetGraph ():
    global playing, graphInitialized, duringITI
    global startedCS, csInProgress, startedUS, usInProgress

    #Reset variables
    playing = False
    graphInitialized = False

    startedCS = csInProgress = startedUS = usInProgress = False
    
    #Stop timers
    sampleTimer.stop()
    displayTimer.stop()

    #Clear the graph
    graphWindow.clear()
    graphWindow.setBackground(None)

    #Since the graph controls the analog outputs, it must turn them off when the graph is cleared
    dw.setCSAmplitude(False)
    dw.setUSAmplitude(False)

    #In case this was called during ITI, stop ITI
    if duringITI:
        duringITI = False
        itiTimer.stop()

#Creates the graph
def createGraph():
    #Variables that persist outside this function call
    global iteration, curve, stimulusGraph, dataSize, data, bars, barHeights, graphInitialized, playing

    #Update the session info label in the main window to reflect trial number
    labelText = "DATA ACQUISITION\n\nTRIAL " + str(ts.currentSession.currentTrial) + " / " + str(ts.currentSession.trialCount)
    mainWindow.sessionInfoLabel.setText(labelText)

    #Define settings
    dataColor = dsm.colors[dsm.ColorAttribute.DATA.value]
    textColor = dsm.colors[dsm.ColorAttribute.TEXT.value]
    stimulusColor = dsm.colors[dsm.ColorAttribute.STIMULUS.value]
    stimulusColor.setAlpha(75) #Give it some transparency since it renders on top of data curve
    axisColor = pg.mkPen(color = dsm.colors[dsm.ColorAttribute.AXIS.value], width = 1)
    graphWindow.setBackground(dsm.colors[dsm.ColorAttribute.BACKGROUND.value])

    #Enable antialiasing for prettier plots
    pg.setConfigOptions(antialias = dsm.antiAliasing)

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

    #Create arrays of size 1 for both x location of bars and bar heights (both with values initialized to 0)
    barXs = np.zeros(1)
    barHeights = np.zeros(1)

    #Add that bar data to the graph along with other settings like width and color
    bars = pg.BarGraphItem(x = barXs, height = barHeights, width = 1.0, brush = dataColor)
    barGraph.addItem(bars)

    #Create data array (this array will be displayed as the line on the graph)
    dataSize = ts.currentSession.trialLengthInSamples #Array size
    data = np.full(shape = dataSize,
                   fill_value = -7,
                   dtype = np.float32) #Create array with all elements initialized to -7 (so they're off-screen)
    #If you don't specify the data type here^, it assumes integers
    
    #Create empty graph
    stimulusGraph = graphWindow.addPlot()

    #Plot line in graph
    if dsm.shading:
        curve = stimulusGraph.plot(y = data, fillLevel = -0.3, brush = dataColor)
    else:
        curve = stimulusGraph.plot(y = data, fillLevel = -0.3, pen = dataColor)

    #Add graph labels
    stimulusGraph.setLabel('bottom',
        "<span style = \"color: " + htmlColorString(textColor) + "; font-size:18px\">Time (ms)</span>")
    stimulusGraph.setLabel('left',
        "<span style = \"color: " + htmlColorString(textColor) + "; font-size:18px\">Eyeblink Amplitude (VDC)</span>")

    #Axis line/tick color
    stimulusGraph.getAxis('bottom').setPen(axisColor)
    stimulusGraph.getAxis('left').setPen(axisColor)

    #Axis limits on graph
    stimulusGraph.setLimits(xMin = 0, xMax = dataSize, yMin = 0, yMax = 7, minXRange = 10, minYRange = 7)

    #Scale x axis ticks to measure milliseconds instead of samples
    stimulusGraph.getAxis('bottom').setScale(ts.currentSession.sampleInterval)

    #Add CS and US start/end lines in graph...

    #Create CS lines and shaded area between lines
    csStart = ts.currentSession.csStartInSamples
    csEnd = ts.currentSession.csEndInSamples
    csRegion = pg.LinearRegionItem(values = [csStart, csEnd], brush = stimulusColor, movable = False)
    csRegion.lines[0].setPen(stimulusColor)
    csRegion.lines[1].setPen(stimulusColor)
    stimulusGraph.addItem(csRegion)

    #Add CS label to middle of shaded area
    csLabel = pg.TextItem(html = "<span style = \"font-size: 16pt; color: " + 
                        htmlColorString(textColor) + "\">CS</span>", color = textColor, anchor = (0.5, 0))
    stimulusGraph.addItem(csLabel)
    csLabel.setPos((csStart + csEnd) / 2, 7)

    #Same for US
    usStart = ts.currentSession.usStartInSamples
    usEnd = ts.currentSession.usEndInSamples
    usRegion = pg.LinearRegionItem(values = [usStart, usEnd], brush = stimulusColor, movable = False)
    usRegion.lines[0].setPen(stimulusColor)
    usRegion.lines[1].setPen(stimulusColor)
    stimulusGraph.addItem(usRegion)

    usLabel = pg.TextItem(html = "<span style = \"font-size: 16pt; color: " + 
                        htmlColorString(textColor) + "\">US</span>", anchor = (0.5, 0))
    stimulusGraph.addItem(usLabel)
    usLabel.setPos((usStart + usEnd) / 2, 7)

    #Regularly sample data (according to sample rate defined in session settings)
    iteration = 0
    sampleTimer.start(ts.currentSession.sampleInterval) #Parameter is millisecond interval between updates

    #Regularly update display (according to display rate defined in display settings)
    displayTimer.start(1000 / dsm.displayRate)

    #Done initializing/creating the graph
    graphInitialized = True

#Called once every sample (manages analog input and outputs)
def sampleUpdate():
    #Variables that need to be survive across multiple calls to update function
    global iteration, dataSize, data, playing

    #Pause functionality
    if not playing:
        #Deactivate analog outputs on pause
        dw.setCSAmplitude(False)
        dw.setUSAmplitude(False)

        #Rest of update is only for play mode
        return
    
    measureRealSampleInterval()

    #Update input and output
    #Only executes when the graph is still being filled out (hasn't reached end of graph)
    if iteration < dataSize:
        #Read in next sample/input value (INPUT)
        data[iteration] = dw.getEyeblinkAmplitude()

        #Controls output of tone/airpuff (OUTPUT)
        manageOutputs()
    else: #End of trial
        if ts.currentSession.currentTrial < ts.currentSession.trialCount:
            endTrialStartITI()  #still have more trials to go so begin ITI

    #End of iteration
    iteration += 1

#Create timer to run sample update function (start is called on the timer in createGraph function above)
sampleTimer = QtCore.QTimer()
sampleTimer.timeout.connect(sampleUpdate)

#From https://doc.qt.io/qtforpython/PySide2/QtCore/QTimer.html#PySide2.QtCore.PySide2.QtCore.QTimer.setTimerType...
#"The accuracy also depends on the timer type.
#For PreciseTimer, QTimer will try to keep the accuracy at 1 millisecond.
#Precise timers will also never time out earlier than expected."
sampleTimer.setTimerType(QtCore.Qt.PreciseTimer)

#Updates the display
def displayUpdate():
    #Variables that need to be survive across multiple calls to update function
    global iteration, dataSize, curve, data, bars, barHeights, playing

    #Pause functionality
    if not playing:
        return

    #Update stimulus graph
    curve.setData(data)

    #Update bar graph
    lastSample = iteration - 1
    if lastSample != -1 and lastSample < dataSize:
        barHeights[0] = data[lastSample]
        bars.setOpts(height = barHeights)

#Create timer to run sample update function (start is called on the timer in createGraph function above)
displayTimer = QtCore.QTimer()
displayTimer.timeout.connect(displayUpdate)

#Called by sample update to manage analog (both CS and US) outputs
def manageOutputs ():
    global startedCS, csInProgress, startedUS, usInProgress

    #Manage CS output
    if startedCS:
        if csInProgress:
            if iteration < ts.currentSession.csEndInSamples:
                dw.setCSAmplitude(True)
            else:
                csInProgress = False
                dw.setCSAmplitude(False)
    elif iteration >= ts.currentSession.csStartInSamples:
        startedCS = True
        csInProgress = True
        dw.setCSAmplitude(True)

    #Manage US output (exact same thing but for US)
    if startedUS:
        if usInProgress:
            if iteration < ts.currentSession.usEndInSamples:
                dw.setUSAmplitude(True)
            else:
                usInProgress = False
                dw.setUSAmplitude(False)
    elif iteration >= ts.currentSession.usStartInSamples:
        startedUS = True
        usInProgress = True
        dw.setUSAmplitude(True)

def endTrialStartITI():
    global itiProgress, itiInterval, duringITI

    #Stop current trial
    resetGraph()

    #Determine ITI duration
    generateITISize()
    
    #Restart ITI progress (indicates how long ITI has been going for in ms)
    itiProgress = 0

    #Establish how long to wait between calls to itiUpdate (in ms)
    itiInterval = 100

    #Begin ITI
    duringITI = True
    setPlaying(True)
    itiTimer.start(itiInterval) #Parameter is millisecond interval between updates

def itiUpdate():
    global itiProgress

    #ITI can be paused
    if not playing:
        return

    #Update how long ITI has been going
    itiProgress += itiInterval

    #print('tick')

    #Determine if ITI is over
    if itiProgress >= itiSize:
        endITIStartTrial()

#Create timer to run ITI (start is called on the timer in startITI function above)
itiTimer = QtCore.QTimer()
itiTimer.timeout.connect(itiUpdate)

def endITIStartTrial():
    global duringITI

    #Stop ITI
    duringITI = False
    itiTimer.stop()

    #Increment trial count
    ts.currentSession.currentTrial += 1

    #Begin new trial (calls createGraph for us since no graph currently exists)
    setPlaying(True)

#Computes the itiSize global variable, using current session's ITI and ITI variance durations
def generateITISize():
    global itiSize

    #Base ITI
    itiSize = ts.currentSession.iti * 1000
    
    #Apply ITI variance
    if ts.currentSession.itiVariance > 0:
        #Generate variance (Size = 1 indicates to only generate one number, i.e. not a sequence of numbers)
        itiVariance = np.random.randint(low = -ts.currentSession.itiVariance,
                                        high = ts.currentSession.itiVariance, size = 1)
        
        #Scale variance from s to ms
        itiVariance *= 1000

        #Apply variance
        itiSize += itiVariance

        #Ensure ITI isn't negative (variance could be larger in magnitude than base duration and be subtracted)
        if itiSize < 0:
            itiSize = 0

#Everything below is for tracking the actual sample rate for performance monitoring...
lastSampleTime = dt.datetime.now()
realSampleIntervalTotal = 0
totalSampleCount = 0

#Accumulates total sample count and time between samples for computation of average time elapsed between samples
def measureRealSampleInterval():
    global lastSampleTime, realSampleIntervalTotal, totalSampleCount

    #Get current time
    newSampleTime = dt.datetime.now()

    #Compute time elapsed between last update and now
    newInterval = (newSampleTime - lastSampleTime).microseconds / 1000

    #Add to totals
    totalSampleCount += 1
    realSampleIntervalTotal += newInterval

    #Done with iteration so update last sample time as right now
    lastSampleTime = newSampleTime

#Compute average sample interval duration based on accumulated totals from function above
def assessAverage():
    global realSampleIntervalTotal, totalSampleCount

    #Nothing to compute
    if totalSampleCount == 0 or not ts.currentSession:
        return
    
    #Average sample interval duration
    average = realSampleIntervalTotal / totalSampleCount
    print("Average: " + str(average))

    #Accuracy of that duration as compared to target sample interval duration
    accuracy = ((average - ts.currentSession.sampleInterval) / ts.currentSession.sampleInterval) * 100
    print("Accuracy: %" + str(accuracy))

    #Reset totals
    totalSampleCount = 0
    realSampleIntervalTotal = 0