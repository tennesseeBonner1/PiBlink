
from enum import Enum

#Singleton instance of session
currentSession = None

#Set gender for trial
class Sex(Enum):
    MALE = 0
    FEMALE = 1

class TheSession(object):
    #Default session settings
    sessionName = ""
    subjectAge = 30
    subjectSex = Sex.MALE
    sampleInterval = 100
    trialCount = 60
    iti = 5
    itiVariance = 3

    #Default trial settings
    trialDuration = 12
    baselineDuration = 2
    csName = "Tone"
    csDuration = 2
    interstimulusInterval = 2
    usName = "Air Puff"
    usDuration = 2

    #General variables
    currentTrial = 1

    #Precomputed values used by graph (for optimization and convenience)
    trialLengthInSamples = 0
    csStartInSamples = 0
    csEndInSamples = 0
    usStartInSamples = 0
    usEndInSamples = 0

    #Constructor for creation of brand new session
    def __init__(self, mainWindow):
        self.readInSettingsFromGUI(mainWindow)
        self.computeSampleMeasurements()

    #Reads in values from settings panel and stores them in the session settings
    def readInSettingsFromGUI (self, mainWindow):
        self.sessionName = mainWindow.sessionNameLineEdit.text()
        self.subjectAge = mainWindow.subjectAgeSpinBox.value()
        self.subjectSex = Sex(mainWindow.subjectSexComboBox.currentIndex())
        self.sampleInterval = mainWindow.sampleIntervalSpinBox.value()
        self.sampleInterval = mainWindow.sampleIntervalSpinBox.value()
        self.trialCount = mainWindow.trialCountSpinBox.value()
        self.iti = mainWindow.itiSpinBox.value()
        self.itiVariance = mainWindow.itiVarianceSpinBox.value()

        #Trial duration settings
        self.trialDuration = mainWindow.trialDurationSpinBox.value()
        self.baselineDuration = mainWindow.baselineDurationSpinBox.value()
        self.csName = mainWindow.csNameLineEdit.text()
        self.csDuration = mainWindow.csDurationSpinBox.value()
        self.interstimulusInterval = mainWindow.interstimulusIntervalSpinBox.value()
        self.usName = mainWindow.usNameLineEdit.text()
        self.usDuration = mainWindow.usDurationSpinBox.value()

    #Used by the graph to convert from milliseconds to samples
    def computeSampleMeasurements(self):
        self.trialLengthInSamples = int(self.trialDuration / self.sampleInterval)
        self.csStartInSamples = int(self.baselineDuration / self.sampleInterval)
        self.csEndInSamples = self.csStartInSamples + int(self.csDuration / self.sampleInterval)
        self.usStartInSamples = self.csEndInSamples + int(self.interstimulusInterval / self.sampleInterval)
        self.usEndInSamples = self.usStartInSamples + int(self.usDuration / self.sampleInterval)
