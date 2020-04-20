
#Returns random noise to act as a substitute for getEyeblinkAmpitude in Data Wizard.
#This is used on projects that run outside of the Pi that still need some kind of data...
#to be plot on the graph for debugging purposes.

#UPDATE: Revised to more closely imitate the look of real data for testing of data analysis.

#For random number generation
import numpy as np

#-----------------------------------------------------------------------------------------------------
#GLOBAL VARIABLES

#Random initial baseline value
eyeblinkAmplitude = eyeblinkAmplitude = np.random.uniform(1, 4)

#samplesToNextBlink = np.random.uniform(200, 1200)

#-----------------------------------------------------------------------------------------------------
#METHODS

#Returns a number between 1 and 10 to plot on graph that is +/- 1 of the last number it returned
def getEyeblinkAmplitude():
    global eyeblinkAmplitude

    #Generate new value
    eyeblinkAmplitude = np.random.uniform(-0.2, 0.2) + eyeblinkAmplitude

    #Make sure value is within range
    eyeblinkAmplitude = clamp(value = eyeblinkAmplitude, minimum = 0, maximum = 5)

    return eyeblinkAmplitude

def setCSAmplitude(high):
    pass

def setUSAmplitude(high):
    pass

#-----------------------------------------------------------------------------------------------------
#HELPER METHODS

def clamp(value, minimum, maximum):
    return min(maximum, max(minimum, value))