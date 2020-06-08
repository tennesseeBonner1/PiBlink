""" TheSession.py
    Last Modified: 6/7/2020
    Taha Arshad, Tennessee Bonner, Devin Mensah, Khalid Shaik, Collin Vaille

    This file is responsible for encapsulating the basic information and operations
    related to a single session. It contains a class called TheSession which performs this encapsulation and a
    single, global instance of this class called currentSession which represents the session currently opened in the program.

    There is also a singleton instance used for remembering the most recent parameters used for data acquisition.
"""
from enum import Enum
import random


#Singleton instance of session
currentSession = None


#Singleton instance of acquisition parameters
#Initialized on program start (in InputManager.py) and persists for duration of program
acquisitionParameters = None


class Sex(Enum):

    MALE = 0
    FEMALE = 1

class Paradigm(Enum):

    PSEUDO = 0
    TRACE = 1
    EXTINCT = 2
    DELAY = 3


class TheSession(object):

    sessionName = ""
    subjectAge = 30
    subjectSex = Sex.MALE
    sampleInterval = 100
    trialCount = 25
    iti = 5
    itiVariance = 3

    paradigm = Paradigm.PSEUDO
    trialDuration = 12
    baselineDuration = 2
    csName = "Tone"
    csDuration = 2
    interstimulusInterval = 2
    usName = "Air Puff"
    usDuration = 2
    usDelay = 0

    minVoltage = 500
    thresholdSD = 4
    thresholdMinDuration = 10

    #General variables
    currentTrial = 1
    sessionStarted = False  #Used by TheGraph to determine whether to create trial on play

    #Precomputed values used by graph (for optimization and convenience)
    trialLengthInSamples = 0
    csStartInSamples = 0
    csEndInSamples = 0
    usStartInSamples = 0
    usEndInSamples = 0
    usSignalStartInSamples = 0
    usSignalEndInSamples = 0

    #Only used in pseudo paradigm sessions
    #Index 0 = Trial 1, Index 1 = Trial 2, etc...
    #True = CS trial, False = US trial
    #Example: index 5 = False means trial 6 is a US trial
    pseudoTrialOrdering = []

    #There can only be one constructor/initializer in python so this uses optional arguments to determine which "constructor" to call
    def __init__ (self, mainWindow, jsonSettings = None, generatePseudoOrdering = False):

        if jsonSettings:
            self.openSessionConstructor(mainWindow, jsonSettings)

        else:
            self.newSessionConstructor(mainWindow, generatePseudoOrdering)

    #Get session from JSON file
    def openSessionConstructor (self, mainWindow, jsonSettings):

        self.readInSettingsFromJSON(jsonSettings)
        self.outputSettingsToGUI(mainWindow)
        self.computeSampleMeasurements()

    #Create new Session
    def newSessionConstructor (self, mainWindow, generatePseudoOrdering):

        self.readInSettingsFromGUI(mainWindow)
        self.computeSampleMeasurements()

        if generatePseudoOrdering and self.paradigm == Paradigm.PSEUDO:
            self.generatePseudoTrialOrdering()

    #Reads in values from settings panel and stores them in the session settings
    def readInSettingsFromGUI (self, mainWindow):

        self.sessionName = mainWindow.sessionNameLineEdit.text()
        self.subjectAge = mainWindow.subjectAgeSpinBox.value()
        self.subjectSex = Sex(mainWindow.subjectSexComboBox.currentIndex())
        self.sampleInterval = mainWindow.sampleIntervalSpinBox.value()
        self.trialCount = mainWindow.trialCountSpinBox.value()
        self.iti = mainWindow.itiSpinBox.value()
        self.itiVariance = mainWindow.itiVarianceSpinBox.value()

        self.paradigm = Paradigm(mainWindow.paradigmComboBox.currentIndex())
        self.trialDuration = mainWindow.trialDurationSpinBox.value()
        self.baselineDuration = mainWindow.baselineDurationSpinBox.value()
        self.csName = mainWindow.csNameLineEdit.text()
        self.csDuration = mainWindow.csDurationSpinBox.value()
        self.interstimulusInterval = mainWindow.interstimulusIntervalSpinBox.value()
        self.usName = mainWindow.usNameLineEdit.text()
        self.usDuration = mainWindow.usDurationSpinBox.value()
        self.usDelay = mainWindow.usDelaySpinBox.value()

        self.minVoltage = mainWindow.minVoltageSpinBox.value()
        self.thresholdSD = mainWindow.thresholdSDSpinBox.value()
        self.thresholdMinDuration = mainWindow.thresholdMinDurSpinBox.value()


    #Reads in values from JSON settings header and stores them in the session settings
    def readInSettingsFromJSON (self, jsonSettings):

        self.sessionName = jsonSettings["name"]
        self.subjectAge = int(jsonSettings["age"])
        self.subjectSex = Sex[jsonSettings["sex"]]
        self.sampleInterval = int(jsonSettings["sampleInterval"])
        self.trialCount = int(jsonSettings["trialCount"])
        self.iti = int(jsonSettings["iti"])
        self.itiVariance = int(jsonSettings["itiVariance"])

        self.paradigm = Paradigm[jsonSettings["paradigm"]]
        self.trialDuration = int(jsonSettings["trialDuration"])
        self.baselineDuration = int(jsonSettings["baselineDuration"])
        self.csName = jsonSettings["csName"]
        self.csDuration = int(jsonSettings["csDuration"])
        self.interstimulusInterval = int(jsonSettings["isi"])
        self.usName = jsonSettings["usName"]
        self.usDuration = int(jsonSettings["usDuration"])
        self.usDelay = int(jsonSettings["usDelay"])

        self.minVoltage = int(jsonSettings["minVoltage"])
        self.thresholdSD = int(jsonSettings["thresholdSD"])
        self.thresholdMinDuration = int(jsonSettings["thresholdMinDuration"])


    #Outputs the values from this session object to the settings GUI panel
    def outputSettingsToGUI (self, mainWindow):

        mainWindow.sessionNameLineEdit.setText(self.sessionName)
        mainWindow.subjectAgeSpinBox.setValue(self.subjectAge)
        mainWindow.subjectSexComboBox.setCurrentIndex(self.subjectSex.value)
        mainWindow.sampleIntervalSpinBox.setValue(self.sampleInterval)
        mainWindow.trialCountSpinBox.setValue(self.trialCount)
        mainWindow.itiSpinBox.setValue(self.iti)
        mainWindow.itiVarianceSpinBox.setValue(self.itiVariance)

        mainWindow.paradigmComboBox.setCurrentIndex(self.paradigm.value)
        mainWindow.trialDurationSpinBox.setValue(self.trialDuration)
        mainWindow.baselineDurationSpinBox.setValue(self.baselineDuration)
        mainWindow.csNameLineEdit.setText(self.csName)
        mainWindow.csDurationSpinBox.setValue(self.csDuration)
        mainWindow.interstimulusIntervalSpinBox.setValue(self.interstimulusInterval)
        mainWindow.usNameLineEdit.setText(self.usName)
        mainWindow.usDurationSpinBox.setValue(self.usDuration)
        mainWindow.usDelaySpinBox.setValue(self.usDelay)

        mainWindow.minVoltageSpinBox.setValue(self.minVoltage)
        mainWindow.thresholdSDSpinBox.setValue(self.thresholdSD)
        mainWindow.thresholdMinDurSpinBox.setValue(self.thresholdMinDuration)

    #Outputs the values from this session object as a new JSON object
    def outputSettingsToJSON(self):

        return {
                    "header":   
                    {
                        "name": self.sessionName,
                        "age": self.subjectAge,
                        "sex": self.subjectSex.name,
                        "sampleInterval": self.sampleInterval,
                        "trialCount": self.trialCount,
                        "iti": self.iti,
                        "itiVariance": self.itiVariance,

                        "paradigm": self.paradigm.name,
                        "trialDuration": self.trialDuration,
                        "baselineDuration": self.baselineDuration,
                        "csName": self.csName,
                        "csDuration": self.csDuration,
                        "isi": self.interstimulusInterval,
                        "usName": self.usName,
                        "usDuration": self.usDuration,
                        "usDelay": self.usDelay,

                        "minVoltage": self.minVoltage,
                        "thresholdSD": self.thresholdSD,
                        "thresholdMinDuration": self.thresholdMinDuration
                    },
                    "trials": []
                }


    #Used by the graph to convert from milliseconds to samples
    def computeSampleMeasurements(self):

        self.trialLengthInSamples = int(self.trialDuration / self.sampleInterval)

        self.csStartInSamples = int(self.baselineDuration / self.sampleInterval)
        self.csEndInSamples = self.csStartInSamples + int(self.csDuration / self.sampleInterval)

        if self.paradigm == Paradigm.PSEUDO:

            #US uses basline
            self.usStartInSamples = int(self.baselineDuration / self.sampleInterval)
            self.usEndInSamples = self.usStartInSamples + int(self.usDuration / self.sampleInterval)
        
        elif self.paradigm == Paradigm.TRACE:

            #US comes after CS
            self.usStartInSamples = self.csEndInSamples + int(self.interstimulusInterval / self.sampleInterval)
            self.usEndInSamples = self.usStartInSamples + int(self.usDuration / self.sampleInterval)

        elif self.paradigm == Paradigm.EXTINCT:

            #No US
            self.usStartInSamples = -100000
            self.usEndInSamples = -100000

        elif self.paradigm == Paradigm.DELAY:

            #US coterminates with CS
            self.usEndInSamples = self.csEndInSamples
            self.usStartInSamples = self.usEndInSamples - int(self.usDuration / self.sampleInterval)

        #Compute the US signal timing
        if self.usStartInSamples >= 0: #Normal computation
            self.usSignalStartInSamples = self.usStartInSamples - int(self.usDelay / self.sampleInterval)
            self.usSignalEndInSamples = self.usEndInSamples - int(self.usDelay / self.sampleInterval)
        else: #No US
            self.usSignalStartInSamples = -100000
            self.usSignalEndInSamples = -100000


    #Populates pseudoTrialOrdering list with new randomized generation
    def generatePseudoTrialOrdering(self):

        #Populate list with alternating True/False so there's an equal number of each
        for x in range(self.trialCount):
            self.pseudoTrialOrdering.append(x % 2 == 0)

        #Randomize ordering
        random.shuffle(self.pseudoTrialOrdering)

        #Ensure no more than X in a row are the same value
        maxConsecutive = 3
        trialIndex = 1
        consecutiveCount = 1
        previousValue = self.pseudoTrialOrdering[0]
        while trialIndex < self.trialCount:
            
            if previousValue == self.pseudoTrialOrdering[trialIndex]:
                
                consecutiveCount += 1

                #Reached consecutive limit
                if consecutiveCount == maxConsecutive:
                    
                    #Find random other index that has opposite value
                    swapIndex = random.randint(0, self.trialCount - 1)

                    #Swap with index
                    values = self.pseudoTrialOrdering[swapIndex], self.pseudoTrialOrdering[trialIndex]
                    self.pseudoTrialOrdering[trialIndex], self.pseudoTrialOrdering[swapIndex] = values

            else:

                consecutiveCount = 1
            
            #No issues, move onto next trial
            previousValue = self.pseudoTrialOrdering[trialIndex]
            trialIndex += 1


    #Returns "TRIAL [X] / [Y]"
    def getTrialProgressString(self):

        return "TRIAL " + str(self.currentTrial) + " / " + str(self.trialCount)
