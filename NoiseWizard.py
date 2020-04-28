
#Returns random noise to act as a substitute for getNextSample in Data Wizard.
#This is used on projects that run outside of the Pi that still need some kind of data...
#to be plot on the graph for debugging purposes.

#UPDATE: Revised to more closely imitate the look of real data for testing of data analysis.

#For random number generation
import numpy as np

#For simulating timing function of ADC library
import timeit

#-----------------------------------------------------------------------------------------------------
#GLOBAL VARIABLES

#Random initial baseline value
nextSample = nextSample = np.random.uniform(1, 4)

#-----------------------------------------------------------------------------------------------------
#METHODS

#Returns a number between 1 and 10 to plot on graph that is +/- 1 of the last number it returned
#Waits until data is ready to read and return value (new sample every ~1 ms)
timeOfLastSample = timeit.default_timer()
def getNextSample():
    global timeOfLastSample, nextSample

    #Wait until data is ready
    while timeit.default_timer() - timeOfLastSample < 0.001:
        pass

    #Record when we got this sample
    timeOfLastSample = timeit.default_timer()

    #Generate new value
    nextSample = np.random.uniform(-0.2, 0.2) + nextSample

    #Make sure value is within range
    nextSample = clamp(value = nextSample, minimum = 0, maximum = 5)

    return nextSample

def onTrialStart():
    pass

def setCSAmplitude(high):
    pass

def setUSAmplitude(high):
    pass

#-----------------------------------------------------------------------------------------------------
#HELPER METHODS

def clamp(value, minimum, maximum):
    return min(maximum, max(minimum, value))