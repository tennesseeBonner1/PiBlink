#from multiprocessing import Process, Queue
import multiprocessing as mp
#import queue as q

import time
import os
import timeit
from enum import Enum

import TheSession as ts
import NoiseWizard as dw
import DisplaySettingsManager as dsm

class Command(Enum):
    START_TRIAL = 0
    PAUSE_TRIAL = 1
    RESUME_TRIAL = 2
    STOP_TRIAL = 3
    END_PROCESS = 4

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
    commandQueue.put(Command.START_TRIAL)

    commandQueue.put((ts.currentSession.sampleInterval,
                              dsm.displayRate,
                              ts.currentSession.csStartInSamples,
                              ts.currentSession.csEndInSamples,
                              ts.currentSession.usStartInSamples,
                              ts.currentSession.usEndInSamples,
                              ts.currentSession.trialLengthInSamples))

def orderToSetPlaying(play):
    if play:
        commandQueue.put(Command.RESUME_TRIAL)
    else:
        commandQueue.put(Command.PAUSE_TRIAL)

def orderToStopTrial():
    commandQueue.put(Command.STOP_TRIAL)

def orderToStopProcess():
    commandQueue.put(Command.END_PROCESS)

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

    print("\nEnd of time critical process.")

def mainLoop():
    global stopProcess
    stopProcess = False

    while (not stopProcess):
        #Wait to be commanded to do something
        while commandQueue.empty():
            blockWait() #Don't need to busy wait when no data acquisition is running

        #Process commands from main process like start trial and end process
        command = commandQueue.get(block = False)

        if command == Command.START_TRIAL:
            runDataAcquisitionTrial()

        if stopProcess or command == Command.END_PROCESS:
            onEndProcess()
            break

def runDataAcquisitionTrial():
    global stopTrial
    stopTrial = False

    #Start data-acquisition trial...
    getTrialParameters()

    #Sampling loop
    for samplingIteration in range(trialLength):
        #Wait during sample interval
        busyWait()

        #Process commands from main process like pause, stop, and end process
        if not commandQueue.empty():
            command = commandQueue.get(block = False)

            if command == Command.PAUSE_TRIAL:
                pauseLoop()
                if stopTrial:
                    break
            elif command == Command.STOP_TRIAL:
                stopTrial = True
                break

            if stopProcess or command == Command.END_PROCESS:
                onEndProcess()
                break

        #Get next sample
        sampleQueue.put(dw.getEyeblinkAmplitude())

        #Record benchmarking information
        recordRealSampleInterval()

    #End of data-acquisition trial...
    #(Turn off outputs and perform benchmarking)
    dw.setCSAmplitude(False)
    dw.setUSAmplitude(False)
    assessSamplingAccuracy()

def pauseLoop():
    #Turn off outputs while paused
    dw.setCSAmplitude(False)
    dw.setUSAmplitude(False)

    #Keep looping until we should leave pause state
    while (not stopProcess):
        #Waiting for command
        while commandQueue.empty():
            blockWait() #Can afford innacuracy in reaction to resuming trial

        #Process commands from main process like resume trial and end process
        command = commandQueue.get(block = False)

        if command == Command.RESUME_TRIAL:
            break
        if command == Command.STOP_TRIAL:
            global stopTrial
            stopTrial = True
            break

        if stopProcess or command == Command.END_PROCESS:
            onEndProcess()
            break

def getTrialParameters():
    #Get trial parameters as tuple from command queue
    trialParameters = commandQueue.get(block = False)

    #Get sample interval
    global sampleIntervalInMS, sampleIntervalInS
    sampleIntervalInMS = trialParameters[0]
    sampleIntervalInS = sampleIntervalInMS / 1000

    #Get display interval
    global displayIntervalInMS
    displayIntervalInMS = trialParameters[1]

    #Get CS/US start/end
    global csStart, csEnd, usStart, usEnd
    csStart = trialParameters[2]
    csEnd = trialParameters[3]
    usStart = trialParameters[4]
    usEnd = trialParameters[5]

    #Get trial length
    global trialLength
    trialLength = trialParameters[6]

#Fast version of wait used when time is critical (more CPU-intensive)
def busyWait():
    startTime = timeit.default_timer()

    while timeit.default_timer() - startTime < sampleIntervalInS:
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
    busyWaitTime = timeit.timeit(stmt = busyWait, number = 1000)
    recordRSITime = timeit.timeit(stmt = recordRealSampleInterval, number = 1000)

    #Run a thousand times + delay measured in seconds = Avg delay of 1 run of operation in ms
    print("MS delay for each operation...\n")

    #Print results
    print("Queue Get: " + str(getTime))
    print("Optimized Get: " + str(timeit.timeit(stmt = testGetOptimizied, number = 1000)))
    print("Queue Put: " + str(putTime))
    print("\nBusy Wait: " + str(busyWaitTime))
    print("Benchmarking: " + str(recordRSITime))

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