""" TheSession.py
    Last Modified: 6/2/2020
    Taha Arshad, Tennessee Bonner, Devin Mensah, Khalid Shaik, Collin Vaille

    This file is responsible for encapsulating the basic information and operations
    related to a single session. It contains a class called TheSession which performs this encapsulation and a
    single, global instance of this class called currentSession which represents the session currently opened in the program.

    There is also a singleton instance used for remembering the most recent parameters used for data acquisition.
"""
from enum import Enum


#Singleton instance of session
currentSession = None


#Singleton instance of acquisition parameters
#Initialized on program start (in InputManager.py) and persists for duration of program
acquisitionParameters = None


#Sex options enum
class Sex(Enum):

    MALE = 0
    FEMALE = 1


class TheSession(object):

    #Default session settings
    sessionName = ""
    subjectAge = 30
    subjectSex = Sex.MALE
    sampleInterval = 100
    trialCount = 25
    iti = 5
    itiVariance = 3
    minVoltage = 500
    thresholdSD = 4
    thresholdMinDuration = 10

    #Default trial settings
    trialDuration = 12
    baselineDuration = 2
    csName = "Tone"
    csDuration = 2
    interstimulusInterval = 2
    usName = "Air Puff"
    usDuration = 2
    usDelay = 0

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

    #There can only be one constructor/initializer in python so this uses optional arguments to determine which "constructor" to call
    def __init__ (self, mainWindow, jsonSettings = None):

        if jsonSettings:
            self.openSessionConstructor(mainWindow, jsonSettings)

        else:
            self.newSessionConstructor(mainWindow)

    #Get session from JSON file
    def openSessionConstructor (self, mainWindow, jsonSettings):

        self.readInSettingsFromJSON(jsonSettings)
        self.outputSettingsToGUI(mainWindow)
        self.computeSampleMeasurements()

    #Create new Session
    def newSessionConstructor (self, mainWindow):

        self.readInSettingsFromGUI(mainWindow)
        self.computeSampleMeasurements()


    #Reads in values from settings panel and stores them in the session settings
    def readInSettingsFromGUI (self, mainWindow):

        self.sessionName = mainWindow.sessionNameLineEdit.text()
        self.subjectAge = mainWindow.subjectAgeSpinBox.value()
        self.subjectSex = Sex(mainWindow.subjectSexComboBox.currentIndex())
        self.sampleInterval = mainWindow.sampleIntervalSpinBox.value()
        self.trialCount = mainWindow.trialCountSpinBox.value()
        self.iti = mainWindow.itiSpinBox.value()
        self.itiVariance = mainWindow.itiVarianceSpinBox.value()
        self.minVoltage = mainWindow.minVoltageSpinBox.value()
        self.thresholdSD = mainWindow.thresholdSDSpinBox.value()
        self.thresholdMinDuration = mainWindow.thresholdMinDurSpinBox.value()

        #Trial duration settings
        self.trialDuration = mainWindow.trialDurationSpinBox.value()
        self.baselineDuration = mainWindow.baselineDurationSpinBox.value()
        self.csName = mainWindow.csNameLineEdit.text()
        self.csDuration = mainWindow.csDurationSpinBox.value()
        self.interstimulusInterval = mainWindow.interstimulusIntervalSpinBox.value()
        self.usName = mainWindow.usNameLineEdit.text()
        self.usDuration = mainWindow.usDurationSpinBox.value()
        self.usDelay = mainWindow.usDelaySpinBox.value()


    #Reads in values from JSON settings header and stores them in the session settings
    def readInSettingsFromJSON (self, jsonSettings):

        self.sessionName = jsonSettings["name"]
        self.subjectAge = int(jsonSettings["age"])
        self.subjectSex = Sex[jsonSettings["sex"]]
        self.sampleInterval = int(jsonSettings["sampleInterval"])
        self.trialCount = int(jsonSettings["trialCount"])
        self.iti = int(jsonSettings["iti"])
        self.itiVariance = int(jsonSettings["itiVariance"])
        self.minVoltage = int(jsonSettings["minVoltage"])
        self.thresholdSD = int(jsonSettings["thresholdSD"])
        self.thresholdMinDuration = int(jsonSettings["thresholdMinDuration"])

        #Trial duration settings
        self.trialDuration = int(jsonSettings["trialDuration"])
        self.baselineDuration = int(jsonSettings["baselineDuration"])
        self.csName = jsonSettings["csName"]
        self.csDuration = int(jsonSettings["csDuration"])
        self.interstimulusInterval = int(jsonSettings["isi"])
        self.usName = jsonSettings["usName"]
        self.usDuration = int(jsonSettings["usDuration"])
        self.usDelay = int(jsonSettings["usDelay"])


    #Outputs the values from this session object to the settings GUI panel
    def outputSettingsToGUI (self, mainWindow):

        mainWindow.sessionNameLineEdit.setText(self.sessionName)
        mainWindow.subjectAgeSpinBox.setValue(self.subjectAge)
        mainWindow.subjectSexComboBox.setCurrentIndex(self.subjectSex.value)
        mainWindow.sampleIntervalSpinBox.setValue(self.sampleInterval)
        mainWindow.trialCountSpinBox.setValue(self.trialCount)
        mainWindow.itiSpinBox.setValue(self.iti)
        mainWindow.itiVarianceSpinBox.setValue(self.itiVariance)
        mainWindow.minVoltageSpinBox.setValue(self.minVoltage)
        mainWindow.thresholdSDSpinBox.setValue(self.thresholdSD)
        mainWindow.thresholdMinDurSpinBox.setValue(self.thresholdMinDuration)

        #Trial duration settings
        mainWindow.trialDurationSpinBox.setValue(self.trialDuration)
        mainWindow.baselineDurationSpinBox.setValue(self.baselineDuration)
        mainWindow.csNameLineEdit.setText(self.csName)
        mainWindow.csDurationSpinBox.setValue(self.csDuration)
        mainWindow.interstimulusIntervalSpinBox.setValue(self.interstimulusInterval)
        mainWindow.usNameLineEdit.setText(self.usName)
        mainWindow.usDurationSpinBox.setValue(self.usDuration)
        mainWindow.usDelaySpinBox.setValue(self.usDelay)

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
                        "minVoltage": self.minVoltage,
                        "thresholdSD": self.thresholdSD,
                        "thresholdMinDuration": self.thresholdMinDuration,

                        "trialDuration": self.trialDuration,
                        "baselineDuration": self.baselineDuration,
                        "csName": self.csName,
                        "csDuration": self.csDuration,
                        "isi": self.interstimulusInterval,
                        "usName": self.usName,
                        "usDuration": self.usDuration,
                        "usDelay": self.usDelay
                    },
                    "trials": [],
                }


    #Used by the graph to convert from milliseconds to samples
    def computeSampleMeasurements(self):

        self.trialLengthInSamples = int(self.trialDuration / self.sampleInterval)

        self.csStartInSamples = int(self.baselineDuration / self.sampleInterval)
        self.csEndInSamples = self.csStartInSamples + int(self.csDuration / self.sampleInterval)

        self.usStartInSamples = self.csEndInSamples + int(self.interstimulusInterval / self.sampleInterval)
        self.usEndInSamples = self.usStartInSamples + int(self.usDuration / self.sampleInterval)

        self.usSignalStartInSamples = self.usStartInSamples - int(self.usDelay / self.sampleInterval)
        self.usSignalEndInSamples = self.usEndInSamples - int(self.usDelay / self.sampleInterval)


    #Returns "TRIAL [X] / [Y]"
    def getTrialProgressString(self):

        return "TRIAL " + str(self.currentTrial) + " / " + str(self.trialCount)
