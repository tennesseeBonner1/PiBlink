""" SuperNoiseWizard.py
    Last Modified: 6/6/2020
    Taha Arshad, Tennessee Bonner, Devin Mensah, Khalid Shaik, Collin Vaille

    Returns quazi-random emulated eyeblinks as a substitute for getNextSample in Data Wizard.
    Like NoiseWizard, this is run on computers that do not have data collection abilities but
    still need to debug the program. SuperNoiseWizard is used in place of NoiseWizard when
    you need sample data that acts like real data such as when testing analysis capabilities.
"""
import numpy as np
import timeit


#Blink emulation parameters
ibiMin = 500   #Inter-blink interval, in samples
ibiMax = 1250   #Inter-blink interval, in samples
baseAmp = np.random.uniform(0.5, 1.0)
blinkDurMin = 200   #In samples
blinkDurMax = 350   #In samples
blinkAmpMin = 1.0   #Added onto base amp, in volts
blinkAmpMax = 3.0   #Added onto base amp, in volts
transitionDur = 100    #Must be less than ibiMin and less than blinkDurMin, in samples


#Random initial "baseline" value
nextSample = baseAmp

#Used to emulate the timing functionality of DataWizard's getNextSample
timeOfLastSample = timeit.default_timer()

#Generates the next sample
def getNextSample():

    global timeOfLastSample, nextSample

    #Wait until data is ready
    while timeit.default_timer() - timeOfLastSample < 0.001:
        pass

    #Record when we got this sample
    timeOfLastSample = timeit.default_timer()

    #Used for emulating eyeblink
    updateEyeblinkStatus()

    #Generate new value
    nextSample += np.random.uniform(-noiseOomph, noiseOomph)

    #Make sure value is within range
    nextSample = clamp(value = nextSample, minimum = 0, maximum = 5)

    return nextSample


def onTrialStart():
    pass


def setCSAmplitude(high):
    pass


def setUSAmplitude(high):
    pass


def clamp(value, minimum, maximum):
    return min(maximum, max(minimum, value))


blinking = False
blinkCountdown = np.random.uniform(ibiMin, ibiMax)
noiseOomph = 0.005
transitionCountdown = 0.0
transitionOomph = 0.0   #Per sample

sampleIndex = 0

def updateEyeblinkStatus():
    global blinking, blinkCountdown, noiseOomph, nextSample, transitionCountdown, transitionOomph

    global sampleIndex

    #Apply smooth transition  to/from blinking
    if transitionCountdown > 0:
        transitionCountdown -= 1
        nextSample += transitionOomph

    #Continue either blinking or not blinking
    if blinkCountdown > 0:
        blinkCountdown -= 1

    #Switch to/from blinking
    else:
        if blinking: #Stop blinking
            blinkCountdown = np.random.uniform(ibiMin, ibiMax)
            transitionOomph = (baseAmp - nextSample) / transitionDur
            noiseOomph = 0.005
        else: #Start blinking
            blinkCountdown = np.random.uniform(blinkDurMin, blinkDurMax)
            transitionOomph = (np.random.uniform(blinkAmpMin, blinkAmpMax)) / transitionDur
            noiseOomph = 0.02

        blinking = not blinking
        transitionCountdown = transitionDur

    sampleIndex += 1