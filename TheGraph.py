from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import TheSession as ts
import timeit
import DisplaySettingsManager as dsm
import NoiseWizard as dw
import JSONConverter
import InputManager as im

#Helper methods used later on
def clamp(value, minimum, maximum):
    return min(maximum, max(minimum, value))

#Converts the colors
def htmlColorString(qtColor):
    return "rgb(" + str(qtColor.red()) + ", " + str(qtColor.blue()) + ", " + str(qtColor.green()) + ")"

#Initializes global variables that need to have default values or references to objects in main window
def initialSetUp (theMainWindow):
    global graphInitialized, playing, duringITI, done
    global startedCS, csInProgress, startedUS, usInProgress
    global mainWindow, graphWindow, blinkStarted

    graphInitialized = False
    playing = False
    duringITI = False
    done = False
    blinkStarted = False

    startedCS = csInProgress = startedUS = usInProgress = False

    #Graph settings on main window
    mainWindow = theMainWindow
    graphWindow = theMainWindow.graphWidget

    #Also set the "color" of the blank graph screen
    graphWindow.setBackground(None)

#Whether or not the graph is playing
def isPlaying ():
    return playing

#Sets the graph's play status to parameter (i.e. true = playing, false = paused)
def setPlaying (play):
    global playing, duringITI, graphInitialized
    
    playing = play

    #if not play:
    #    assessAverage()

    if not duringITI:
        if play and (not graphInitialized):
            createGraph()

#Resets the graph (i.e. removes graph window and is ready for new call to createGraph)
def resetGraph ():
    global playing, graphInitialized, duringITI, done
    global startedCS, csInProgress, startedUS, usInProgress

    #Reset variables
    playing = False
    graphInitialized = False
    done = False

    startedCS = csInProgress = startedUS = usInProgress = False

    #Stop timers
    sampleTimer.stop()
    displayTimer.stop()
    itiTimer.stop()

    #Print out accuracy and reset measurements for start of new benchmark
    if im.playMode == im.PlayMode.ACQUISITION:
        assessSamplingAccuracy()

    #In case this was called during ITI, stop ITI
    duringITI = False

    #Clear the graph
    graphWindow.clear()
    graphWindow.setBackground(None)

    #Since the graph controls the analog outputs, it must turn them off when the graph is cleared
    if im.playMode == im.PlayMode.ACQUISITION:
        dw.setCSAmplitude(False)
        dw.setUSAmplitude(False)

#Creates the graph
def createGraph():
    #Variables that persist outside this function call
    global iteration, curve, stimulusGraph, dataSize, data, bars, barHeights, graphInitialized, playing, done, baseLineEnd

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

    #Removes default "A" button on bottom left corner used for resetting the zoom on the graph
    stimulusGraph.hideButtons()

    #Disables the context menu you see when right-clicking on the graph
    stimulusGraph.setMenuEnabled(False)

    baseLineEnd = ts.currentSession.csStartInSamples
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

    #Launch graph based on play mode
    if im.playMode == im.PlayMode.PLAYBACK:
        #LOAD IN PLAYBACK VIEW OF TRIAL...

        #Update graph with array of samples for trial
        curve.setData(JSONConverter.openTrial())
    else:
        #START DATA ACQUISITION...
        #i.e. start timers

        #Regularly sample data (according to sample rate defined in session settings)
        iteration = 0
        sampleTimer.start(ts.currentSession.sampleInterval) #Parameter is millisecond interval between updates

        #Regularly update display (according to display rate defined in display settings)
        displayTimer.start(1000 / dsm.displayRate)

    #Done initializing/creating/launching the graph
    done = False #As in done with session, which we are not (we are just starting the session!!!)
    graphInitialized = True

#Called once every sample (manages analog input and outputs)
def sampleUpdate():
    #Variables that need to be survive across multiple calls to update function
    global iteration, dataSize, data, playing, baseLineEnd, blinkStarted

    #Pause functionality
    if not playing:
        #Deactivate analog outputs on pause
        dw.setCSAmplitude(False)
        dw.setUSAmplitude(False)

        #Rest of update is only for play mode
        return
    
    recordRealSampleInterval()

    #Update Input/Output
    #Only executes when the graph is still being filled out (hasn't reached end of graph)
    if iteration < dataSize:
        #Read in next sample/input value from analog input (INPUT)
        data[iteration] = dw.getEyeblinkAmplitude()
        
        if iteration < baseLineEnd:
            JSONConverter.addToAverage(data[iteration])
        elif iteration == baseLineEnd:
            JSONConverter.setSD(data, iteration)
        elif iteration > baseLineEnd:
            blinkValue = JSONConverter.checkForBlink(data[iteration], iteration)
            if (blinkStarted == False):
                if (blinkValue == True):
                    blinkStarted == True
                    addArrow(iteration)
            if (blinkStarted == True):
                if (blinkValue == False):
                    blinkStarted == False
        
        #Controls output of tone/airpuff (OUTPUT)
        manageAnalogOutputs()
    else: #End of trial
        endTrialStartITI() #Won't start ITI if this was the last trial

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
#Doesn't need to be called during playback b/c playback shouldn't interact with analog I/O
def manageAnalogOutputs ():
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

#Adds arrow on top of data at xPosition (in ms) on graph
def addArrow(xPosition):

    #Create arrow with style options
    #Make sure to specify rotation in constructor, b/c there's a bug in PyQtGraph (or PyQt)...
    #where you can't update the rotation of the arrow after creation
    #See (http://www.pyqtgraph.org/documentation/graphicsItems/arrowitem.html) for options
    arrow = pg.ArrowItem(angle = -90,
                         headLen = 30,
                         headWidth = 30,
                         brush = dsm.colors[dsm.ColorAttribute.AXIS.value])

    #Set arrow's x and y positions respectively
    arrow.setPos(xPosition, data[xPosition])

    #Finally, add arrow to graph
    stimulusGraph.addItem(arrow)

def endTrialStartITI():
    global itiCountdown, itiInterval, duringITI, countdownLabel, done

    #Determine ITI duration
    generateITISize()
    
    #Save trial
    JSONConverter.saveTrial(data, int(itiSize))

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

    
    
    #Restart countdown timer (indicates how long ITI has left in ms)
    itiCountdown = itiSize

    #Create countdown label "Next trial in..."
    graphWindow.addLabel(text = "Next trial in...",
                         size = "20pt",
                         color = "#000000",
                         row = 0,
                         col = 0)

    #Create countdown label "X.X"
    countdownLabel = graphWindow.addLabel(text = "{:5.1f}".format(itiCountdown),
                         size = "69pt",
                         color = "#000000",
                         row = 1,
                         col = 0)

    #Establish how long to wait between calls to itiUpdate (in ms)
    itiInterval = 100

    #Begin ITI
    duringITI = True
    setPlaying(True)
    itiTimer.start(itiInterval) #Parameter is millisecond interval between updates

def itiUpdate():
    global itiCountdown

    #ITI can be paused
    if not playing:
        return

    recordRealSampleInterval()

    #Update how long ITI has been going (countdown is in seconds, interval is in ms)
    itiCountdown -= itiInterval / 1000

    #Display updated countdown (format countdown from int to string with 1 decimal point precision)
    countdownLabel.setText(text = "{:5.1f}".format(itiCountdown))

    #Determine if ITI is over
    if itiCountdown <= 0:
        endITIStartTrial()

#Create timer to run ITI (start is called on the timer in startITI function above)
itiTimer = QtCore.QTimer()
itiTimer.timeout.connect(itiUpdate)
itiTimer.setTimerType(QtCore.Qt.PreciseTimer)

def endITIStartTrial():
    #Stop ITI (does the following: clear countdown from graph, duringITI = False, itiTimer.stop())
    resetGraph()

    #Increment trial count
    ts.currentSession.currentTrial += 1

    #Begin new trial (calls createGraph for us since no graph currently exists)
    setPlaying(True)

#Computes the itiSize global variable, using current session's ITI and ITI variance durations
def generateITISize():
    global itiSize

    #Base ITI (in seconds)
    itiSize = ts.currentSession.iti
    
    #Apply ITI variance
    if ts.currentSession.itiVariance > 0:
        #Generate variance
        #Returns numpy.ndarray of size 1 so we index that array at 0 to get random number
        itiVariance = np.random.randint(low = -ts.currentSession.itiVariance,
                                        high = ts.currentSession.itiVariance, size = 1)[0]
        
        #Apply variance
        itiSize += itiVariance

        #Ensure ITI isn't negative (variance could be larger in magnitude than base duration and be subtracted)
        if itiSize < 0:
            itiSize = 0

#Everything below is for tracking the actual sample rate for performance monitoring...
startedSampling = False
startTime = timeit.default_timer()
totalSampleCount = 0

#Accumulates total sample count and timing info for computation of average time elapsed between samples
def recordRealSampleInterval():
    global startedSampling, startTime, totalSampleCount

    #Function is called every new sample
    totalSampleCount += 1

    #Record start time (in ms)
    if not startedSampling:
        startedSampling = True
        startTime = timeit.default_timer() * 1000

#Compute average sample interval duration based on accumulated totals from function above and assesses accuracy
def assessSamplingAccuracy():
    global startedSampling, startTime, totalSampleCount

    #Nothing to compute
    if totalSampleCount == 0 or not ts.currentSession:
        return

    print("ITI" if duringITI else "Trial")
    
    #Record end time (in ms)
    endTime = timeit.default_timer() * 1000

    #Average sample interval duration (in ms)
    average = (endTime - startTime) / totalSampleCount

    #print("Avg Interval: " + str(average) + " ms")

    #Latency: different between expected and actual interval on average (in ms)
    if duringITI:
        print("Avg Latency: " + str(average - itiTimer.interval()) + " ms\n")
    else:
        print("Avg Latency: " + str(average - sampleTimer.interval()) + " ms\n")

    #Reset totals
    startedSampling = False
    totalSampleCount = 0
