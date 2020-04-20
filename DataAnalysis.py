
import math
import TheGraph as tg
import TheSession as ts

maxArrowCount = 30

#Called by JSON converter to get the stats to save for each trial
#(data acquisition analysis)
def getTrialStats():
    #Compute analysis-related trial stats
    analyzeTrial()

    #Compute CS/US onset/offset
    csOnset = ts.currentSession.baselineDuration
    csOffset = csOnset + ts.currentSession.csDuration
    usOnset = csOffset + ts.currentSession.interstimulusInterval
    usOffset = usOnset + ts.currentSession.usDuration

    #Compile dictionary with all stats
    statsDict = {
        "baselineDuration": ts.currentSession.baselineDuration,
        "csOnset": csOnset,
        "csOffset": csOffset,
        "usOnset": usOnset,
        "usOffset": usOffset,
        "trialDuration": ts.currentSession.trialDuration,
        "baselineAvg": baselineAverage,
        "baselineSD": standardDeviation,
        "onsetIndices": onsetIndices,
        "offsetIndices": offsetIndices,
    }

    #Return stats dictionary
    return statsDict

#Called after playback view of trial is generated to place arrows where blinking starts
#(playback analysis)
def addEyeblinkArrows():
    #Needed to compute eyeblink onset samples
    analyzeTrial()

    #For each eyeblink onset, add an arrow marking it on the graph
    #The number of arrows added is capped at maxArrowCount
    numberOfArrows = min(len(onsetIndices), maxArrowCount)
    for x in range(numberOfArrows):
        tg.addArrow(onsetIndices[x])

    #print("Onsets: " + str(len(onsetIndices)))
    #print("SD: " + str(standardDeviation))
    #print("Avg: " + str(baselineAverage) + "\n")

#ABOVE ARE THE BIG BOY FUNCTIONS
#-----------------------------------------------------------------------------------------------------
#BELOW ARE THE HELPER FUNCTIONS

def analyzeTrial():
    #Initialize local variables
    baselineEnd = ts.currentSession.csStartInSamples
    blinkStarted = False
    dataSize = tg.dataSize

    #Initialize global variables
    global data, baselineTotal, onsetIndices, offsetIndices
    data = tg.data
    baselineTotal = 0.00
    onsetIndices = []
    offsetIndices = []

    #Go through all samples in order...
    for sampleIndex in range(dataSize):
        #For baseline samples, simply aggregate total amplitude (for computation of average later)
        if sampleIndex < baselineEnd:
            addToBaselineTotal(data[sampleIndex])

        #One time, at end of baseline, compute average and standard deviation (SD)
        elif sampleIndex == baselineEnd:
            computeAverageAndSD()

        #After baseline track when samples go in and out of two SD from average
        #and place an arrow when samples become greater than two SD from average
        else:
            #Is current sample "blinking", AKA greater than two SD from average?
            blinkValue = checkForBlink(data[sampleIndex])

            #Previously blinking, so see if we need to change state to not blinking
            if blinkStarted:
                if not blinkValue:
                    blinkStarted = False
                    offsetIndices.append(sampleIndex)

            #Previously not blinking, so see if we need to change state to blinking
            else:
                if blinkValue:
                    blinkStarted = True
                    onsetIndices.append(sampleIndex)

def addToBaselineTotal(number):
    global baselineTotal
    baselineTotal += number

def computeAverageAndSD():
    global baselineAverage, standardDeviation

    #Determine number of samples in baseline
    baselineSampleCount = ts.currentSession.csStartInSamples

    #Compute baseline average
    baselineAverage = baselineTotal / baselineSampleCount

    #Compute standard deviation (SD)...
    number = 0.00
    for i in range(baselineSampleCount):
        number += math.pow(data[i] - baselineAverage, 2)

    number = number / baselineSampleCount
    standardDeviation = math.sqrt(number)

#Returns whether eyeblink amplitude is high enough to be considered "blinking"
def checkForBlink(value):
    return (value > (baselineAverage + (2 * standardDeviation)))