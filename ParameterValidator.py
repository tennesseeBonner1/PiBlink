""" ParameterValidator.py
    Last Modified: 6/10/2020
    Taha Arshad, Tennessee Bonner, Devin Mensah, Khalid Shaik, Collin Vaille

    This file contains the verifySettingsValid function which is called when the settings panel is
    supposed to lock to determine whether it is allowed to. All other functions below are just
    helper methods called by verifySettingsValid.

    A global instance of TheSession is temporarily created called params. This instance is not used
    to represent real sessions, rather it is for ease of access to check the selected parameters.
"""
import TheSession as ts
import InputManager as im
from PyQt5.QtWidgets import QMessageBox


#Checks the current settings and brings up a message box if anything is invalid as well as return a boolean based on the validity
def verifySettingsValid():

    global params

    #Create temporary session object from parameter panel for easy access to parameters
    params = ts.TheSession(im.mainWindow)

    settingsValidityText = "Current settings are invalid for the following reasons:\n\n"
    invalidSettings = False

    paradigm = params.paradigm

    if paradigm == ts.Paradigm.PSEUDO:
        if not pseudoDurationIsValid():
            invalidSettings = True
            settingsValidityText += "Trial duration must be >= baseline + CS and baseline + US for pseudo paradigm\n"

        if not (params.trialCount % 2 == 0):
            invalidSettings = True
            settingsValidityText += "Number of trials must be even for pseudo paradigm\n"

    elif paradigm == ts.Paradigm.TRACE:
        if not traceDurationIsValid():
            invalidSettings = True
            settingsValidityText += "Trial duration must be >= baseline + CS + ISI + US for trace paradigm\n"

    elif paradigm == ts.Paradigm.EXTINCT:
        if not extinctDurationIsValid():
            invalidSettings = True
            settingsValidityText += "Trial duration must be >= baseline + CS for extinction paradigm\n"

    elif paradigm == ts.Paradigm.DELAY:
        if not extinctDurationIsValid(): #Extinction and delay have same duration check
            invalidSettings = True
            settingsValidityText += "Trial duration must be >= baseline + CS for delay paradigm\n"

        if params.usDuration > params.csDuration:
            invalidSettings = True
            settingsValidityText += "US duration must be <= CS duration for delay paradigm\n"

    if params.trialDuration < 100:
        invalidSettings = True
        settingsValidityText += "Trial duration must be >= 100 ms\n"

    if params.baselineDuration < 100:
        invalidSettings = True
        settingsValidityText += "Baseline duration must be >= 100 ms\n"

    if not usSignalStartIsValid():
        invalidSettings = True
        settingsValidityText += "US start - US signal delay must be >= 0\n"

    if not sessionNameIsValid():
        invalidSettings = True
        settingsValidityText += "Session name may not contain any of the following characters: \\ / : * ? \" < > |\n"

    if invalidSettings:
        invalidSettingsNotice = QMessageBox()
        invalidSettingsNotice.setText(settingsValidityText)
        invalidSettingsNotice.setWindowTitle("Invalid Settings")
        invalidSettingsNotice.setStandardButtons(QMessageBox.Ok)
        invalidSettingsNotice.setIcon(QMessageBox.Warning)
        invalidSettingsNotice.setFont(im.popUpFont)
        invalidSettingsNotice.exec()

    return not invalidSettings


def pseudoDurationIsValid():
    return extinctDurationIsValid() and params.baselineDuration + params.usDuration <= params.trialDuration


def traceDurationIsValid():
    beginningToEndOfUS = params.baselineDuration
    beginningToEndOfUS += params.csDuration
    beginningToEndOfUS += params.interstimulusInterval
    beginningToEndOfUS += params.usDuration

    return params.trialDuration >= beginningToEndOfUS


def extinctDurationIsValid():
    return params.baselineDuration + params.csDuration <= params.trialDuration


#Returns if the session name contains any characters that could cause problems in a file name
def sessionNameIsValid():
    sessionText = params.sessionName
    return not ("\\" in sessionText or "/" in sessionText or ":" in sessionText or "<" in sessionText or ">" in sessionText or "*" in sessionText or "?" in sessionText or "\"" in sessionText or "|" in sessionText)


def usSignalStartIsValid():
    usDelay = params.usDelay

    if params.paradigm == ts.Paradigm.EXTINCT:
        return True
    elif params.paradigm == ts.Paradigm.TRACE:
        return params.baselineDuration + params.csDuration + params.interstimulusInterval - usDelay >= 0
    else:
        return params.baselineDuration - usDelay >= 0