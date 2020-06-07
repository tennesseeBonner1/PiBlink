""" DataAnalysis.py
    Last Modified: 5/6/2020
    Taha Arshad, Tennessee Bonner, Devin Mensah, Khalid Shaik, Collin Vaille

    This program contains funtions that are used by the JSON Converter in order to make stat calculations. 
    These include calculations for the eyeblinks as well as all the calculations needed for it.
"""    
import math
import TheGraph as tg
import TheSession as ts

#maxArrowCount = 30

#Called by JSON converter to get the stats to save for each trial(data acquisition analysis)
def getTrialStats(minVoltage=0, minSD=4, minDuration=1, data=[]):
    #Fill data with the data in the graph if it is empty
    if len(data) == 0:
        data = tg.data

    #Compute analysis-related trial stats
    analyzeTrial(minVoltage, minSD, minDuration, data)

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
        "sampleRange": sampleRange,
        "onsetSamples": onsetSamples,
        "offsetSamples": offsetSamples,
    }

    #Return stats dictionary
    return statsDict


#This function analyses the data to calculate the onsets and offsets of the eyeblinks
def analyzeTrial(minVoltage=0, minSD=4, minDuration=1, data=[]):

    #Initialize global variables
    global baselineTotal, baselineAverage, standardDeviation, sampleRange, onsetSamples, offsetSamples

    #Initialize local variables
    baselineEnd = ts.currentSession.csStartInSamples
    blinking = False
    count = 0
    dataSize = tg.dataSize
    baselineTotal = 0.00
    baselineAverage = 0.00
    standardDeviation = 0.00
    sampleRange = 0.00
    onsetSamples = []
    offsetSamples = []

    #Fill data with the data in the graph if it is empty
    if len(data) == 0:
        data = tg.data

    #Get the range of the samples to see if it meets the minimum voltage
    #Casting to float turns it from a numpy.float32 type to a regular float type, so it can be encoded in JSON 
    sampleRange = float(max(data) - min(data))
    if sampleRange < minVoltage / 1000:
        return

    #Go through all samples in order
    for sampleIndex in range(dataSize):

        #For baseline samples, simply aggregate total amplitude (for computation of average later)
        if sampleIndex < baselineEnd:
            addToBaselineTotal(data[sampleIndex])

        #One time, at end of baseline, compute average and standard deviation (SD)
        elif sampleIndex == baselineEnd:
            computeAverageAndSD(data)

        #After baseline, compute onsets and offsets based on the minimum SDs and duration required to be counted as a blink
        else:

            #First, check to see if the value is above the threshold
            overThreshold = data[sampleIndex] > (baselineAverage + minSD * standardDeviation)

            #Adjust the count of consecutive values above the threshold accordingly
            count = (count + 1) * overThreshold

            #Check to see if a new onset should be registered
            if not blinking and (count >= minDuration):
                blinking = True

                #Subtract (minDuration - 1) to go back to the first sample of the onset
                #Add 1 to convert from array index to sample number
                onsetSamples.append(sampleIndex - minDuration + 2)

            #Check to see if a new offset should be registered
            elif blinking and not overThreshold:
                blinking = False

                #Add 1 to convert from array index to sample number
                offsetSamples.append(sampleIndex + 1)


#Add to the baseline in order to calculate the SD
def addToBaselineTotal(number):

    global baselineTotal

    baselineTotal += number


#Compute the Average and SD
def computeAverageAndSD(data):

    global baselineAverage, standardDeviation

    #Determine number of samples in baseline
    baselineSampleCount = ts.currentSession.csStartInSamples

    #Compute baseline average
    baselineAverage = baselineTotal / baselineSampleCount

    #Compute standard deviation (SD)
    number = 0.00
    for i in range(baselineSampleCount):
        number += math.pow(data[i] - baselineAverage, 2)

    number = number / baselineSampleCount
    standardDeviation = math.sqrt(number)
