
'''
This file is responsible for spawning and managing the time-critical/sampling process.
Everything that is time-critical is run on this separate process, i.e. sampling and ITIs.

The main process issues commands to the sampling process via the command queue.
The sampling process sends samples to the main process via the sample queue.

The sampling process is spawned on program start and waits idle until data acquisition begins.

The sampling process is sent an END_PROCESS command (see code below) when the main process
ends (either by crashing or successful termination) so that it does not become a zombie.
'''

import multiprocessing as mp
import time
import os
import timeit
from enum import Enum
import TheSession as ts
import NoiseWizard as dw

#Command types that can be sent from main process to sampling process via the command queue
class Command(Enum):
    START_TRIAL = 0
    PAUSE_TRIAL = 1
    RESUME_TRIAL = 2
    STOP_TRIAL = 3
    END_PROCESS = 4

#Mutually exclusive states. At any time, sampling process must be in exactly one of them
class CurrentlyIn(Enum):
    MAIN_LOOP = 0
    TRIAL = 1
    PAUSE_LOOP = 2

#Called at start of program to launch other process, establish communication between it, and
#get it ready for use (will sit in low-powerish polling state until data acquisition begins)
def initialSetUp():
    #Queues used for inter-process communication
    sampleQueue = mp.Queue(2000) #Output of time critical process, input of main process
    commandQueue = mp.Queue(2000) #Output of main process, input of time critical process

    #Create and start time critical process (target is function called on time critical process to start it)
    timeCriticalProcess = mp.Process(target = startTimeCriticalProcess, args = (sampleQueue, commandQueue))

    timeCriticalProcess.start()

    #Save as global variables after starting time critical process so...
    #that process has no chance of gettings its global variables mixed up with ours
    saveQueuesAsGlobalVars(sampleQueue, commandQueue)

#This tells the time critical process to begin sampling with all the parameters it needs
def orderToStartTrial():
    commandQueue.put((Command.START_TRIAL,
                        (ts.currentSession.sampleInterval,
                        ts.currentSession.csStartInSamples,
                        ts.currentSession.csEndInSamples,
                        ts.currentSession.usSignalStartInSamples,
                        ts.currentSession.usSignalEndInSamples,
                        ts.currentSession.trialDuration,
                        ts.currentSession.trialLengthInSamples)))

def orderToSetPlaying(play):
    if play:
        commandQueue.put((Command.RESUME_TRIAL, None))
    else:
        commandQueue.put((Command.PAUSE_TRIAL, None))

def orderToStopTrial():
    commandQueue.put((Command.STOP_TRIAL, None))

def orderToStopProcess():
    commandQueue.put((Command.END_PROCESS, None))

#EVERYTHING ABOVE IS RUN ON THE MAIN PROCESS
#--------------------------------------------------------------------------------------------------------------
#The below function is called separately by both processes as part of set up

def saveQueuesAsGlobalVars (theSampleQueue, theCommandQueue):
    global sampleQueue, commandQueue

    sampleQueue = theSampleQueue
    commandQueue = theCommandQueue

#--------------------------------------------------------------------------------------------------------------
#EVERYTHING BELOW IS RUN ON THE TIME CRITICAL PROCESS

#Function called when time critical process is launched
def startTimeCriticalProcess(theSampleQueue, theCommandQueue):

    #Establish communication medium with main process
    saveQueuesAsGlobalVars(theSampleQueue, theCommandQueue)

    #testPerformance()

    mainLoop()

    print("\nEnd of time critical process.\n")

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

def runDataAcquisitionTrial(trialParameters):
    global stopTrial
    stopTrial = False

    #Start data acquisition trial...
    initializeTrial(trialParameters)

    #Used to implement sample interval parameter (see loop below for usage)
    msLeftInCurrentInterval = sampleIntervalInMS

    #Sampling loop
    samplingIteration = 0
    for msIteration in range(trialDurationInMS):
        #Process single command
        if not commandQueue.empty():
            breakOnReturn = processCommand(CurrentlyIn.TRIAL)
            if breakOnReturn:
                break

        #Get next sample (occurs every 1 ms)
        msLeftInCurrentInterval -= 1
        newSample = dw.getNextSample()  #Busy waits until sample is ready

        #If sample interval has expired, send sample to main process
        if msLeftInCurrentInterval == 0:
            #Send sample to main process
            sampleQueue.put(newSample)

            #Start new interval
            samplingIteration += 1
            msLeftInCurrentInterval = sampleIntervalInMS

            #Update analog outputs every sample interval
            manageAnalogOutputs(samplingIteration)

            #Record benchmarking information
            recordRealSampleInterval()

        #Otherwise, discard sample

    #End of data-acquisition trial...
    #(Turn off outputs and perform benchmarking)
    dw.setCSAmplitude(False)
    dw.setUSAmplitude(False)
    assessSamplingAccuracy()

def pauseLoop():
    #Turn off outputs while paused
    dw.setCSAmplitude(False)
    dw.setUSAmplitude(False)

    print(2 + "error")

    #Keep looping until we should leave pause state
    while (not stopProcess):
        #Waiting for command
        while commandQueue.empty():
            blockWait() #Can afford innacuracy in reaction to resuming trial

        #Process single command
        breakOnReturn = processCommand(CurrentlyIn.PAUSE_LOOP)
        if breakOnReturn:
            break

def initializeTrial(trialParameters):
    #Prepare ADC library for sampling
    dw.onTrialStart()

    #Give default values to trial status variables
    global startedCS, csInProgress, startedUS, usInProgress
    startedCS = False
    csInProgress = False
    startedUS = False
    usInProgress = False

    #Get sample interval
    global sampleIntervalInMS
    sampleIntervalInMS = trialParameters[0]

    #Get CS/US start/end
    global csStart, csEnd, usStart, usEnd
    csStart = trialParameters[1]
    csEnd = trialParameters[2]
    usStart = trialParameters[3]
    usEnd = trialParameters[4]

    #Get trial duration in MS
    global trialDurationInMS
    trialDurationInMS = trialParameters[5]

    #Get trial length
    global trialLength
    trialLength = trialParameters[6]

#Process a single command from main process like resume trial or end process
def processCommand(currentlyIn):
    global stopTrial

    #Extract the command
    fullCommand = commandQueue.get(block = False)
    command = fullCommand[0]
    commandArguments = fullCommand[1]

    breakOnReturn = False

    #Identify the command and process it if applicable to current situation
    #for example: ignore pause command when no trial is running
    if command == Command.START_TRIAL and currentlyIn == CurrentlyIn.MAIN_LOOP:
        runDataAcquisitionTrial(commandArguments)
    elif command == Command.PAUSE_TRIAL and currentlyIn == CurrentlyIn.TRIAL:
        pauseLoop()
        if stopTrial:   #If stop button was pressed while in pause loop
            breakOnReturn = True
    elif command == Command.RESUME_TRIAL and currentlyIn == CurrentlyIn.PAUSE_LOOP:
        breakOnReturn = True
    elif command == Command.STOP_TRIAL and (
        currentlyIn == CurrentlyIn.TRIAL or currentlyIn == CurrentlyIn.PAUSE_LOOP):
        stopTrial = True
        breakOnReturn = True
    elif command == Command.END_PROCESS:
        onEndProcess()

    #May need to climb out of multiple levels of recursion to stop process
    #i.e. pause loop -> trial -> main loop -> (fall through to end process)
    #This is achieved by checking the global var stopProcess
    if stopProcess:
        breakOnReturn = True

    return breakOnReturn

#Called every sample interval to manage analog (both CS and US) outputs
#This function was designed with optimization in mind
#I could, and maybe should, have written it in a few lines, but that would have been slower!
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
#(Sampling intervals are achieved automatically when reading the samples)
def busyWait():
    startTime = timeit.default_timer()

    while timeit.default_timer() - startTime < 0.1:
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




























#Must be set before p.start is called
#Main process terminates all daemons immediately on exit, waits for (joins) all non-daemons.
#https://stackoverflow.com/questions/25391025/what-exactly-is-python-multiprocessing-modules-join-method-doing
#p.daemon = True

#print("Module name: " + __name__) #Main/GUI process: "__main__", Sampling process: "__mp_main__"

#print("PID: " + str(os.getpid()))

#p.join()

















#--------------------------------------------------------------------------------------------------------------
#Below section is for tracking the actual sample rate for performance monitoring...
#(still on time critical process)
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
    if totalSampleCount == 0:
        return

    #Record end time (in ms)
    endTime = timeit.default_timer() * 1000

    #Average sample interval duration (in ms)
    average = (endTime - startTime) / totalSampleCount

    print("Avg Interval: " + str(average) + " ms")

    #Latency: different between expected and actual interval on average (in ms)
    print("Avg Latency: " + str(average - sampleIntervalInMS) + " ms\n")

    #Reset totals
    startedSampling = False
    totalSampleCount = 0


#Below is alternate tool for performance measurement...


#Can be used during debugging to determine the time it takes for each basic operation
def testPerformance():
    #Wait for things to settle down
    time.sleep(1)

    #Perform measurements
    getTime = timeit.timeit(stmt = testGet, number = 1000)
    putTime = timeit.timeit(stmt = testPut, number = 1000)
    busyWaitTime = timeit.timeit(stmt = testBusyWait, number = 1000)
    recordRSITime = timeit.timeit(stmt = recordRealSampleInterval, number = 1000)

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

'''
sampleTicker = 0
    batchOfSamples = q.Queue()
    def testPutOptimized():
        global sampleTicker

        sampleTicker += 1
        batchOfSamples.put(1)

        if sampleTicker == 10:
            sampleTicker = 0

            sampleQueue.put(babatchOfSamples)
            batchOfSamples.clear()
'''

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

    '''
        try:
            commandQueue.get(block = False)
        except Exception:
            pass
        else:
            pass
    '''

def testBusyWait():
    startTime = timeit.default_timer()

    while timeit.default_timer() - startTime < 0.001:
        pass