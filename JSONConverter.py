""" JSONConverter.py
    Last Modified: 6/2/2020
    Taha Arshad, Tennessee Bonner, Devin Mensah, Khalid Shaik, Collin Vaille

    This file's responsibilities are to:
    1. Save sessions as JSON files.
    2. Open the JSON saved session files.
    3. Save parameters as JSON files.
    4. Load parameters from JSON files.
    5. Provide a few common functionalities related to file management.
    
    At the top layer of the dictionary structure, there are two key-value pairs. The two keys are "header" and "trials"
    The value mapped to the "header" key is another dictionary containing key-value pairs that relate to the session-specific settings 
    ("name", "sex", "age", "trialDuration", etc.) The value mapped to the "trials" key is an array of dictionaries, where each dictionary 
    holds the information for a single trial. Within these trial dictionaries are a few key-value pairs, including a pair which contains 
    the stats of the trial (another dictionary), and a pair which maps a key to an array containing all of the sample data.
"""
import TheSession as ts
import DataAnalysis as da
import InputManager as im
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox
import json
from datetime import datetime
import os


#Initializes the JSONconverter(getting reference to main window, and resetting the savefilename)
def initialSetUp(theMainWindow):

    global mainWindow, saveFilename

    mainWindow = theMainWindow
    saveFilename = ""


#Called at the beginning of the data acquisition session to save the session settings and prepare for trial saving. Also determines the savefilename 
def startDataAcquisition():

    global trialsSaved, saveFilename, jsonObject
    	
    trialsSaved = 0

    name = str(ts.currentSession.sessionName)
    sex = str(ts.currentSession.subjectSex.name)
    age = str(ts.currentSession.subjectAge)
    now = datetime.now()
    date = str(now.strftime("%m-%d-%Y"))

    #Define location to save file in and make the directory if it doesn't exist
    desiredLocation = getSavedSessionDirectory(createIfNonexistent = True)

    #Define ideal filename
    if name:
        baseName = name + " (" + sex + " " + age + ") " + date

    else:
        baseName = "(" + sex + " " + age + ") " + date

    #Put filename, location and '.json' together
    idealFilename = os.path.join(desiredLocation, baseName)
    saveFilename = idealFilename + ".json"

    duplicateNumber = 0

    #Add an incrementing number in filename (if needed) until we find one that's not taken
    while (os.path.exists(saveFilename)):
        duplicateNumber += 1
        saveFilename = idealFilename + " (" + str(duplicateNumber) + ").json"

    #Create the JSON object (and fill out the header with session info)
    jsonObject = ts.currentSession.outputSettingsToJSON()


#Called at the end of a trial to save the just-completed trial
def saveTrial(trialDataArray, previousITI):

    global trialsSaved
    
    #If we stop the session prematurely, we need to know how many trials are in the saved session
    trialsSaved += 1

    #Convert trial data from numpy array to python list
    trialDataList = trialDataArray.tolist()

    #Create new trial (singular) object
    trialObject = {
                       "trialNumber": trialsSaved,
                       "previousITI": previousITI,
                       "stats": da.getTrialStats(ts.currentSession.minVoltage, ts.currentSession.thresholdSD, ts.currentSession.thresholdMinDuration),
                       "samples": trialDataList
                  }

    print(str(trialObject["previousITI"]))
    #Append trial (singular) object to trials (plural) array
    jsonObject["trials"].append(trialObject)


#Finalizes data acquisition by writing session (stored in JSON object) to JSON file(Before this point, data has been accumulating in the JSON object)
def endDataAcquisition():

    #If the data acquisition session was ended before completion, remember how many actually got saved
    jsonObject["header"]["trialCount"] = str(trialsSaved)

    #Only proceed with saving the session to file if it has a non-zero number of trials
    if trialsSaved > 0:

        #Open new file in write mode (overwrites any preexisting file with same name)
        sessionFile = open(saveFilename, "w")

        #Convert JSON object to string
        jsonString = json.dumps(jsonObject) 

        #Write string to file
        sessionFile.write(jsonString)

        #Close file
        sessionFile.close()


def saveAsParameterFile():

    #Pop up "Save As" window to retrieve file name and type to save as
    parameterFileName = QtGui.QFileDialog.getSaveFileName(parent = mainWindow.centralwidget,
                    caption = "Save Parameter File As",
                    directory = getParameterFileDirectory(createIfNonexistent = True),
                    filter = "JSON (*.json)")[0]

    #Save parameter file if user didn't click cancel
    if len(parameterFileName) > 0:

        #Get parameters to save
        #Can't use ts.acquisitionParameters b/c need to be able to save in playback as well...
        #and ts.acquisitionParameters only updates when play mode is changed
        toSave = ts.TheSession(mainWindow)

        #Convert to JSON object
        paramJSONObject = toSave.outputSettingsToJSON()

        #Convert to string
        jsonString = json.dumps(paramJSONObject)

        #Open new file in write mode (overwrites any preexisting file with same name)
        sessionFile = open(parameterFileName, "w")

        #Write string to file
        sessionFile.write(jsonString)

        #Close file
        sessionFile.close()


#Opens JSON file, reads in JSON data, recreates session (or parameter) object with data
#sessionObject = True means we're opening a saved session file
#sessionObject = False means we're opening a parameter file
def openJSONFile(filename, sessionObject):

    global jsonObject, saveFilename

    #Open file, extract contents into string, and close the file
    try:
        sessionFile = open(file = filename, mode = "r")

        if sessionObject:
            saveFilename = filename

        jsonString = sessionFile.read()

        sessionFile.close()

    except Exception:
        return "The file cannot be opened."

    #Convert string into python dictionary
    try:

        theJSONObject = json.loads(jsonString)
        
        if sessionObject:
            jsonObject = theJSONObject

    except Exception:
        return "The file is not in JSON format despite file extension."

    #Recreate session (or parameter) object using the settings in the header of the json file
    try:

        if sessionObject:
            ts.currentSession = ts.TheSession(mainWindow, theJSONObject["header"])
        else:
            loadedParameters = ts.TheSession(mainWindow, theJSONObject["header"])
            loadedParameters.outputSettingsToGUI(mainWindow)

    except KeyError:
        errorMessage = "The JSON file does not have all applicable information.\n"
        if sessionObject:
            errorMessage += "Was this session created in an older version of the program?"
        else:
            errorMessage += "Was this parameter file created in an older version of the program?"
        return errorMessage

    if sessionObject and len(theJSONObject["trials"]) == 0:
        return "This appears to be a parameter file, not a session file!"

    #Execution is finished and error-free so return empty quotes indicating no error message
    return ""


#Returns the array of samples for the current trial
def openTrial():

    return jsonObject["trials"][ts.currentSession.currentTrial - 1]["samples"]


#Returns the array of onsets for the current trial
def getOnsets():

    return jsonObject["trials"][ts.currentSession.currentTrial - 1]["stats"]["onsetSamples"]


#Returns the array of offsets for the current trial
def getOffsets():

    return jsonObject["trials"][ts.currentSession.currentTrial - 1]["stats"]["offsetSamples"]


def loadParameterFile():
    
    #Pop up "Open" window to retrieve file name
    parameterFileName = QtGui.QFileDialog.getOpenFileName(parent = mainWindow.centralwidget,
                            caption = "Open Parameter File",
                            directory = getParameterFileDirectory(createIfNonexistent = True),
                            filter = "JSON (*.json)")[0]

    #Open parameter file if user didn't click cancel
    if len(parameterFileName) > 0:
        errorMessage = openJSONFile(parameterFileName, False)

        if errorMessage:
            #Craft error message
            fullMessage = "Cannot read parameter file for the following reason...\n\n" + errorMessage

            #Notify user
            cannotReadSession = QMessageBox()
            cannotReadSession.setText(fullMessage)
            cannotReadSession.setWindowTitle("Error Opening Parameter File")
            cannotReadSession.setStandardButtons(QMessageBox.Ok)
            cannotReadSession.setIcon(QMessageBox.Critical)
            cannotReadSession.setFont(im.popUpFont)
            cannotReadSession.exec()


#Creates a saved session directory if one doesn't exist
def getSavedSessionDirectory(createIfNonexistent):

    #Subfolder of current working dir
    savedSessionDirectory = os.path.join(os.getcwd(), "Saved Sessions")

    #Make the directory if required to exist
    if createIfNonexistent and (not os.path.exists(savedSessionDirectory)):
        os.makedirs(savedSessionDirectory)

    return savedSessionDirectory


#Creates a parameter file directory if one doesn't exist
def getParameterFileDirectory(createIfNonexistent):

    #Subfolder of current working dir
    parameterFileDirectory = os.path.join(os.getcwd(), "Parameter Files")

    #Make the directory if required to exist
    if createIfNonexistent and (not os.path.exists(parameterFileDirectory)):
        os.makedirs(parameterFileDirectory)

    return parameterFileDirectory


#Gets the filename of the currently open file and returns it
def getCurrentFilename():

	#Partition the lengthy pathname to get only the file name (checking for both \ and / to be safe)
	justTheName = saveFilename.rpartition('\\')[2]
	justTheName = justTheName.rpartition('/')[2]

	#remove the file extension
	justTheName = justTheName.rpartition('.')[0]
	
	return justTheName
