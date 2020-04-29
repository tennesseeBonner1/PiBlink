import math
import TheGraph as tg
import TheSession as ts

maxArrowCount = 30

#Called by JSON converter to get the stats to save for each trial
#(data acquisition analysis)
def getTrialStats(minSD=4, minDuration=1, data=None):
    if data == None:
        data = tg.data

    #Compute analysis-related trial stats
    analyzeTrial(minSD, minDuration, data)

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
        "onsetSamples": onsetSamples,
        "offsetSamples": offsetSamples,
    }

    #Return stats dictionary
    return statsDict

#Don't think this function is necessary anymore -toDelete
#Called after playback view of trial is generated to place arrows where blinking starts
#(playback analysis)
def addEyeblinkArrows():
    #Needed to compute eyeblink onset samples
    analyzeTrial()

    #For each eyeblink onset, add an arrow marking it on the graph
    #The number of arrows added is capped at maxArrowCount
    numberOfArrows = min(len(onsetSamples), maxArrowCount)
    for x in range(numberOfArrows):
        tg.addArrow(onsetSamples[x] - 1) #Decrement by one to convert to indices

    #print("Onsets: " + str(len(onsetSamples)))
    #print("SD: " + str(standardDeviation))
    #print("Avg: " + str(baselineAverage) + "\n")

#ABOVE ARE THE BIG BOY FUNCTIONS
#-----------------------------------------------------------------------------------------------------
#BELOW ARE THE HELPER FUNCTIONS

def analyzeTrial(minSD=4, minDuration=1, data=None):
    #Initialize local variables
    baselineEnd = ts.currentSession.csStartInSamples
    blinking = False
    count = 0
    dataSize = tg.dataSize

    #Initialize global variables
    global baselineTotal, onsetSamples, offsetSamples

    if data == None:
        data = tg.data
    
    baselineTotal = 0.00
    onsetSamples = []
    offsetSamples = []

    #Go through all samples in order...
    for sampleIndex in range(dataSize):
        #For baseline samples, simply aggregate total amplitude (for computation of average later)
        if sampleIndex < baselineEnd:
            addToBaselineTotal(data[sampleIndex])

        #One time, at end of baseline, compute average and standard deviation (SD)
        elif sampleIndex == baselineEnd:
            computeAverageAndSD(data)

        #After baseline, compute onsets and offsets based on the minimum SDs and duration
        #required to be counted as a blink
        else:
            #First, check to see if the value is above the threshold
            overThreshold = data[sampleIndex] > (baselineAverage + minSD * standardDeviation)

            #Adjust the count of consecutive values above the threshold accordingly
            count = (count + 1) * overThreshold

            #Then check if we can confirm any onsets/offsets
            #Check to see if a new onset should be registered
            if not blinking and (count >= minDuration):
                blinking = True
                onsetSamples.append(sampleIndex - minDuration + 2)

            #Check to see if a new offset should be registered
            elif blinking and not overThreshold:
                blinking = False
                offsetSamples.append(sampleIndex + 1)

def addToBaselineTotal(number):
    global baselineTotal
    baselineTotal += number

def computeAverageAndSD(data):
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

#-toDelete
#Returns whether eyeblink amplitude is high enough to be considered "blinking"
def checkForBlink(value):
    return (value > (baselineAverage + (4 * standardDeviation)))