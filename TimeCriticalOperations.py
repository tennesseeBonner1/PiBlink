""" TheSession.py
    Last Modified: 5/6/2020
    Taha Arshad, Tennessee Bonner, Devin Mensah, Khalid Shaik, Collin Vaille

    This file is responsible for spawning and managing the time-critical/sampling process.
    Everything that is time-critical is run on this separate process, (sampling and ITIs).

    The main process issues commands to the sampling process via the command queue.
    The sampling process sends samples to the main process via the sample queue.
    The sampling process sends ITI time updates to the main process via the ITI queue.

    The sampling process is spawned on program start and waits idle until data acquisition begins.

    The sampling process is sent an END_PROCESS command (see code below) when the main process
    ends (either by crashing or successful termination) so that it does not become a zombie.
"""
import multiprocessing as mp
import time
import os
import timeit
import numpy as np
from enum import Enum
import TheSession as ts
import NoiseWizard as dw

#Set this to false to eliminate performance print outs
printPerformanceMeasurements = False

#Command types that can be sent from main process to sampling process via the command queue
class Command(Enum):

    START_SESSION = 0
    PAUSE_SESSION = 1
    RESUME_SESSION = 2
    STOP_SESSION = 3
    END_PROCESS = 4


#Mutually exclusive states. At any time, sampling process must be in exactly one of them
class CurrentlyIn(Enum):

    MAIN_LOOP = 0
    RUNNING_SESSION = 1
    PAUSED_SESSION = 2


#Called at start of program to launch other process, establishes communication, and gets it ready for use (will sit in low-powerish polling state until data acquisition begins)
def initialSetUp():

    #Queues used for inter-process communication
    sampleQueue = mp.Queue(2000) #Direction: Output of sampling process, input of main process
    itiQueue = mp.Queue(200) #Same direction
    commandQueue = mp.Queue(200) #Opposite direction

    #Create and start time critical process (target is function called on time critical process to start it)
    timeCriticalProcess = mp.Process(target = startTimeCriticalProcess,
                                     args = (sampleQueue, itiQueue, commandQueue))

    timeCriticalProcess.start()

    #Save as global variables after starting time critical process so that process has no chance of gettings its global variables mixed up with ours
    saveQueuesAsGlobalVars(sampleQueue, itiQueue, commandQueue)


#This tells the time critical process to begin sampling with all the parameters it needs
def orderToStartSession():

    #First, clean out any previous sampling process output so we start with clean slate
    while not sampleQueue.empty():
        sampleQueue.get(block = False)
    while not itiQueue.empty():
        itiQueue.get(block = False)

    commandQueue.put((Command.START_SESSION, ts.currentSession))


#Control play status, i.e. True = play, False = pause
def orderToSetPlaying(play):

    if play:
        commandQueue.put((Command.RESUME_SESSION, None))

    else:
        commandQueue.put((Command.PAUSE_SESSION, None))

#Stop session
def orderToStopSession():

    commandQueue.put((Command.STOP_SESSION, None))

#Stop process
def orderToStopProcess():

    commandQueue.put((Command.END_PROCESS, None))

#The below function is called separately by both processes as part of set up
def saveQueuesAsGlobalVars (theSampleQueue, theITIQueue, theCommandQueue):

    global sampleQueue, itiQueue, commandQueue

    sampleQueue = theSampleQueue
    itiQueue = theITIQueue
    commandQueue = theCommandQueue


#Function called when time critical process is launched
def startTimeCriticalProcess(theSampleQueue, theITIQueue, theCommandQueue):

    #Establish communication medium with main process
    saveQueuesAsGlobalVars(theSampleQueue, theITIQueue, theCommandQueue)

    #testPerformance()

    mainLoop()

    if printPerformanceMeasurements:
        print("\nEnd of sampling process.\n")

#Main loop for time critical process
#Waits on command to start data acquisition
def mainLoop():

    global stopProcess
    stopProcess = False

    while (not stopProcess):

        #Wait to be commanded to do something
        while commandQueue.empty():

            blockWait() #Don't need to busy wait when no data acquisition is running

        #Process single command
        breakOnReturn = processCommand(CurrentlyIn.MAIN_LOOP)

        if breakOnReturn:
            break


#Begins running data acquisition session according to session settings passed in
def runSession(sessionObject):

    recordSessionStart()
    
    initializeSession(sessionObject)

    #Session loop
    for trial in range(1, trialCount + 1):
        #Run trial
        runTrial()
        if stopSession or stopProcess:
            break

        #Run ITI (except for last trial where there is no following ITI)
        if trial < trialCount:
            runITI()
            if stopSession or stopProcess:
                break

    #Benchmarking (only if session is not interrupted)
    if (not stopSession) and (not stopProcess):
        assessSessionTiming()


#Runs a single data acquisition trial
def runTrial():

    #Start data acquisition trial
    initializeTrial()

    #Used to implement sample interval parameter (see loop below for usage)
    msLeftInCurrentInterval = sampleIntervalInMS

    samplingIteration = 0

    #Sampling loop
    for msIteration in range(trialDurationInMS):

        #Process single command
        if not commandQueue.empty():

            breakOnReturn = processCommand(CurrentlyIn.RUNNING_SESSION)

            if breakOnReturn:
                break

        #Get next sample (occurs every 1 ms)
        msLeftInCurrentInterval -= 1
        newSample = dw.getNextSample()  #Busy waits until sample is ready

        #If sample interval has expired, send sample to main process (otherwise, discard sample)
        if msLeftInCurrentInterval == 0:

            #Send sample to main process
            sampleQueue.put(newSample)

            #Start new interval
            samplingIteration += 1
            msLeftInCurrentInterval = sampleIntervalInMS

            #Update analog outputs every sample interval
            manageAnalogOutputs(samplingIteration)

            #Record benchmarking information
            recordTrialStart()

    #End of data-acquisition trial (Turn off outputs and perform benchmarking)
    dw.setCSAmplitude(False)
    dw.setUSAmplitude(False)
    assessTrialTiming()
    addToSessionTime(trialDurationInMS / 1000)

#Generate the duration of and run a single ITI
def runITI():

    #Generate ITI duration
    itiCountdown = generateITISize()

    #Benchmarking
    addToSessionTime(itiCountdown)

    #Every tenth of a second (decisecond), update ITI
    while itiCountdown > 0:
        #Send main process update of ITI timing
        itiQueue.put(itiCountdown)

        #Wait a tenth of a second
        busyWait()

        #Update ITI
        itiCountdown -= 0.1

        #Process single command
        if not commandQueue.empty():
            breakOnReturn = processCommand(CurrentlyIn.RUNNING_SESSION)
            if breakOnReturn:
                break

    #Last update to indicate done with ITI
    itiQueue.put(0)

#Pauses the processes until they resume or are stopped
def pauseLoop():

    recordPauseStart()

    #Turn off outputs while paused
    dw.setCSAmplitude(False)
    dw.setUSAmplitude(False)

    #Keep looping until we should leave pause state
    while (not stopProcess):

        #Waiting for command
        while commandQueue.empty():
            blockWait() #Can afford innacuracy in reaction to resuming trial

        #Process single command
        breakOnReturn = processCommand(CurrentlyIn.PAUSED_SESSION)

        if breakOnReturn:
            break

    recordPauseEnd()

#Initialize a session
def initializeSession(sessionObject):

    global stopSession
    global sampleIntervalInMS, trialCount, baseITI, itiVariance
    global csStart, csEnd, usStart, usEnd, trialDurationInMS, trialLengthInSamples

    #Only set to true when session execution needs to be terminated (i.e. stop button pressed)
    stopSession = False

    #Get sample interval
    sampleIntervalInMS = sessionObject.sampleInterval

    #Get trial count
    trialCount = sessionObject.trialCount

    #Get ITI base and variance
    baseITI = sessionObject.iti
    itiVariance = sessionObject.itiVariance

    #Get CS/US start/end
    csStart = sessionObject.csStartInSamples
    csEnd = sessionObject.csEndInSamples
    usStart = sessionObject.usSignalStartInSamples
    usEnd = sessionObject.usSignalEndInSamples

    #Get trial length in samples
    trialLengthInSamples = sessionObject.trialLengthInSamples

    '''
    Get target trial duration in MS.
    This might be slightly more than the time of the final sample.
    
    Example:
    Trial Duration = 5000 ms, Sample Interval = 3 ms
    So Sample count = int(5000 / 3) = 1666.
    This means the last sample occurs at 1666 * 3 = 4998 ms, 2 ms before 5000 ms duration.
    The sampling loop DELIBERATELY waits those extra 2 ms, collecting no extra samples...
    to ensure the timing accuracy/pacing remains on track.
    The timing difference would accumulate over many trials, so this might matter?
    '''
    trialDurationInMS = sessionObject.trialDuration

#Initializes a trial
def initializeTrial():

    global startedCS, csInProgress, startedUS, usInProgress
    
    #Prepare ADC library for sampling
    dw.onTrialStart()

    #Give default values to trial status variables
    startedCS = False
    csInProgress = False
    startedUS = False
    usInProgress = False


#Process a single command from main process like resume or end process
def processCommand(currentlyIn):

    global stopSession

    #Extract the command
    fullCommand = commandQueue.get(block = False)
    command = fullCommand[0]
    commandArguments = fullCommand[1]

    breakOnReturn = False

    #Identify the command and process it if applicable to current situation
    if command == Command.START_SESSION and currentlyIn == CurrentlyIn.MAIN_LOOP:
        runSession(commandArguments)

    elif command == Command.PAUSE_SESSION and currentlyIn == CurrentlyIn.RUNNING_SESSION:

        pauseLoop()

        if stopSession:   #If stop button was pressed while in pause loop
            breakOnReturn = True

    elif command == Command.RESUME_SESSION and currentlyIn == CurrentlyIn.PAUSED_SESSION:
        breakOnReturn = True

    elif command == Command.STOP_SESSION and (
        currentlyIn == CurrentlyIn.RUNNING_SESSION or currentlyIn == CurrentlyIn.PAUSED_SESSION):
        stopSession = True
        breakOnReturn = True

    elif command == Command.END_PROCESS:
        onEndProcess()

    #May need to climb out of multiple levels of recursion to stop process (This is achieved by checking the global var stopProcess)
    if stopProcess:
        breakOnReturn = True

    return breakOnReturn


#Called every sample interval to manage analog (both CS and US) outputs. This function was designed with optimization in mind
def manageAnalogOutputs (samplingIteration):
    
    global startedCS, csInProgress, startedUS, usInProgress

    #Manage CS output
    if startedCS:

        if csInProgress:

            if samplingIteration < csEnd:

                dw.setCSAmplitude(True)

            else:

                csInProgress = False
                dw.setCSAmplitude(False)

    elif samplingIteration >= csStart:

        startedCS = True
        csInProgress = True
        dw.setCSAmplitude(True)

    #Manage US output (exact same thing but for US)
    if startedUS:

        if usInProgress:

            if samplingIteration < usEnd:

                dw.setUSAmplitude(True)

            else:

                usInProgress = False
                dw.setUSAmplitude(False)

    elif samplingIteration >= usStart:

        startedUS = True
        usInProgress = True
        dw.setUSAmplitude(True)


#Fast version of wait used during ITI (more CPU-intensive)
def busyWait():

    theStartTime = timeit.default_timer()

    while timeit.default_timer() - theStartTime < 0.1:
        pass


#Slow version of wait used when time is NOT critical (less CPU-intensive)
def blockWait():
    time.sleep(0.05)


#Perform clean up (turn off analog outputs)
def onEndProcess():

    global stopProcess

    stopProcess = True

    dw.setCSAmplitude(False)
    dw.setUSAmplitude(False)


#Below section is for tracking the actual sample rate for performance monitoring (still on time critical process)
startedSampling = False
startTime = timeit.default_timer()
totalSampleCount = 0

#Generates and returns the ITI size in seconds, using base ITI and ITI variance
def generateITISize():

    #Base ITI (in seconds)
    generatedITI = baseITI
    
    #Apply ITI variance (also in seconds)
    if itiVariance > 0:
        #Generate variance
        #Returns numpy.ndarray of size 1 so we index that array at 0 to get random number
        generatedVariance = np.random.randint(low = -itiVariance, high = itiVariance, size = 1)[0]
        
        #Apply variance
        generatedITI += generatedVariance

        #Ensure ITI isn't negative (variance could be larger in magnitude than base duration and be subtracted)
        if generatedITI < 0:
            generatedITI = 0

    #We're done here
    return generatedITI

#-----------------------------------------------------------------------------------------------
#Rest of file is for benchmarking/performance testing

#Accumulates total sample count and timing info for computation of average time elapsed between samples
def recordTrialStart():

    global startedSampling, startTime, totalSampleCount

    #Function is called every new sample
    totalSampleCount += 1

    #Record start time (in ms)
    if not startedSampling:

        startedSampling = True
        startTime = timeit.default_timer() * 1000


#Compute average sample interval duration based on accumulated totals from function above and assesses accuracy
def assessTrialTiming():

    global startedSampling, startTime, totalSampleCount

    #Nothing to compute
    if totalSampleCount == 0:
        return

    #Record end time (in ms)
    endTime = timeit.default_timer() * 1000

    #Average sample interval duration (in ms)
    average = (endTime - startTime) / totalSampleCount

    if printPerformanceMeasurements:
        print("\nTrial complete.")
        print("Avg Interval: " + str(average) + " ms")
        print("Avg Latency: " + str(average - sampleIntervalInMS) + " ms\n")

    #Reset totals
    startedSampling = False
    totalSampleCount = 0


def recordSessionStart():
    global expectedSessionTime, sessionStartTime

    expectedSessionTime = 0
    sessionStartTime = timeit.default_timer()

def addToSessionTime(amountInSeconds):
    global expectedSessionTime

    expectedSessionTime += amountInSeconds

def assessSessionTiming():
    sessionEndTime = timeit.default_timer()
    actualSessionTime = sessionEndTime - sessionStartTime
    latency = 100 * ((actualSessionTime - expectedSessionTime) / expectedSessionTime)

    if printPerformanceMeasurements:
        print("\nSession completed.")
        print("Expected time: " + str(expectedSessionTime) + " seconds")
        print("Actual time: " + str(actualSessionTime) + " seconds")
        print("Latency: " + str(latency) + "%\n")

def recordPauseStart():
    global pauseStart
    pauseStart = timeit.default_timer()

def recordPauseEnd():
    global sessionStartTime, startTime
    
    pauseEnd = timeit.default_timer()
    pauseDuration = pauseEnd - pauseStart
    
    #Factor time paused out of performance measurements
    sessionStartTime += pauseDuration #For total session time
    startTime += pauseDuration * 1000 #For single trial time

#Can be used during debugging to determine the time it takes for each basic operation
def testPerformance():
    if not printPerformanceMeasurements:
        return

    #Wait for things to settle down
    time.sleep(1)

    #Perform measurements
    getTime = timeit.timeit(stmt = testGet, number = 1000)
    putTime = timeit.timeit(stmt = testPut, number = 1000)
    busyWaitTime = timeit.timeit(stmt = testBusyWait, number = 1000)
    recordRSITime = timeit.timeit(stmt = recordTrialStart, number = 1000)

    #Run a thousand times + delay measured in seconds = Avg delay of 1 run of operation in ms
    print("MS delay for each operation...\n")

    #Print results
    print("Queue Get: " + str(getTime))
    print("Optimized Get: " + str(timeit.timeit(stmt = testGetOptimizied, number = 1000)))
    print("Queue Put: " + str(putTime))
    print("\nBusy Wait: " + str(busyWaitTime))
    print("Benchmarking: " + str(recordRSITime))

    print("Noise Read: " + str(timeit.timeit(stmt = dw.getNextSample, number = 1000)))

    #print("\nTotal: " + str(putTime + getTime + busyWaitTime + recordRSITime))

def testPut():

    sampleQueue.put(1)

def testGet():

    if not commandQueue.empty():

        commandQueue.get(block = False)

ticker = 0


def testGetOptimizied():

    global ticker

    ticker += 1

    if ticker == 10:
        ticker = 0

        if not commandQueue.empty():
            commandQueue.get(block = False)


def testBusyWait():
    startTime = timeit.default_timer()

    while timeit.default_timer() - startTime < 0.001:
        pass
