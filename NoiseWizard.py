
#Returns random noise to act as a substitute for getEyeblinkAmpitude in Data Wizard.
#This is used on projects that run outside of the Pi that still need some kind of data...
#to be plot on the graph for debugging purposes.

#For random number generation
import numpy as np

#-1 is initial value to indicate that it is undefined
eyeblinkAmplitude = -1

#Helper method
def clamp(value, minimum, maximum):
    return min(maximum, max(minimum, value))

#Returns a number between 1 and 10 to plot on graph that is +/- 1 of the last number it returned
def getEyeblinkAmplitude():
    global eyeblinkAmplitude

    if eyeblinkAmplitude == -1:
        eyeblinkAmplitude = np.random.uniform(0, 6)
        return eyeblinkAmplitude
    else:
        eyeblinkAmplitude = clamp(value = np.random.uniform(-1, 1) + eyeblinkAmplitude,
                              minimum = 0,
                              maximum = 5)
        return eyeblinkAmplitude

def setCSAmplitude(high):
    pass

def setUSAmplitude(high):
    pass