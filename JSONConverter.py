
#This file's responsibilities are to...
#1. Save sessions as JSON files.
#2. Open the JSON saved session files.

import TheSession as ts
import DataAnalysis as da
import json
from datetime import datetime
import os

#Called on start of program to perform initialization (i.e. getting reference to main window)
def initialSetUp (theMainWindow):
    global mainWindow

    mainWindow = theMainWindow

#-----------------------------------------------------------------------------------------------------
#1. SAVE SESSION/DATA ACQUISITION MODE SUPPORT

#Called at the beginning of the data acquisition session to save the session settings and prepare...
#for trial saving. Also determines the save filename (performed at start of session versus end...
#because the start date is what we're interested in, not the end date).
def startDataAcquisition():
    global trialsSaved, saveFilename, jsonObject
    	
    trialsSaved = 0

    name = str(ts.currentSession.sessionName)
    sex = str(ts.currentSession.subjectSex.name)
    age = str(ts.currentSession.subjectAge)

    now = datetime.now()
    date = str(now.strftime("%m-%d-%Y"))

    '''
        month = now.strftime("%m")
        day = now.strftime("%d")
        year = now.strftime("%Y")
        hour = now.strftime("%H")
        minute = now.strftime("%M") 
        second = now.strftime("%S")
        #"timestamp": (month, day, year, hour, minute, second),
    '''

    #Define location to save file in and make the directory if it doesn't exist
    desiredLocation = getSavedSessionDirectory(createIfNonexistent = True)

    #Define ideal filename + location
    if name:
        baseName = name + " (" + sex + " " + age + ") " + date
    else:
        baseName = "(" + sex + " " + age + ") " + date
    idealFilename = os.path.join(desiredLocation, baseName)  #Put location and name together
    saveFilename = idealFilename + ".json"

    #Add an incrementing number in filename (if needed) until we find one that's not taken
    duplicateNumber = 0
    while (os.path.exists(saveFilename)):
        duplicateNumber += 1
        saveFilename = idealFilename + " (" + str(duplicateNumber) + ").json"

    #Define the structure of the JSON object (and fill out the header with session info)
    jsonObject = {
                    "header":   
                    {
                        "name": name,
                        "sex": sex,
                        "age": age,
                        "sampleInterval": ts.currentSession.sampleInterval,
                        "trialCount": ts.currentSession.trialCount,
                        "iti": ts.currentSession.iti,
                        "itiVariance": ts.currentSession.itiVariance,
                        "trialDuration": ts.currentSession.trialDuration,
                        "baselineDuration": ts.currentSession.baselineDuration,
                        "csName": ts.currentSession.csName,
                        "csDuration": ts.currentSession.csDuration,
                        "isi": ts.currentSession.interstimulusInterval,
                        "usName": ts.currentSession.usName,
                        "usDuration": ts.currentSession.usDuration
                    },

                    "trials": [],
                }

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
                       "stats": da.getTrialStats(),
                       "samples": trialDataList
                  }

    #Append trial (singular) object to trials (plural) array
    jsonObject["trials"].append(trialObject)

#Finalize data acquisition by writing session (stored in JSON object) out to JSON file
#Before this point, data has just been accumulating in the JSON object with no file saving
def endDataAcquisition():
    #If the data acquisition session was ended before completion, remember how many actually got saved
    jsonObject["header"]["trialCount"] = str(trialsSaved)

    #Only proceed with saving the session to file if it has a non-zero number of trials
    if trialsSaved > 0:
        #Open new file in write mode (overwrites any preexisting file with same name)
        sessionFile = open(saveFilename, "w")

        #Write JSON object to file
        jsonString = json.dumps(jsonObject) #Convert JSON object to string
        sessionFile.write(jsonString) #Write string to file

        #Close file
        sessionFile.close()

#This can be later extended to give the user the option to choose which directory is...
#the default directory, or have the system remember the last used directory
def getSavedSessionDirectory(createIfNonexistent):
    #Subfolder of current working dir
    savedSessionDirectory = os.path.join(os.getcwd(), "Saved Sessions")

    #Make the directory if required to exist
    if createIfNonexistent and (not os.path.exists(savedSessionDirectory)):
        os.makedirs(savedSessionDirectory)

    return savedSessionDirectory

#-----------------------------------------------------------------------------------------------------
#2. OPEN SESSION/PLAYBACK MODE SUPPORT

#Opens JSON file, reads in JSON data, recreates session object with data
#After this function is called, the user can press the play button to begin playback
def openSession(filename):
    global jsonObject

    #Open file, extract contents into string, and close the file
    try:
        sessionFile = open(file = filename, mode = "r")
        jsonString = sessionFile.read()
        sessionFile.close()
    except Exception:
        return "The file cannot be opened."

    #Convert string into python dictionary
    try:
        jsonObject = json.loads(jsonString)
    except Exception:
        return "The file is not in JSON format despite file extension."

    #Recreate session object using the settings in the header of the json file
    try:
        ts.currentSession = ts.TheSession(mainWindow, jsonObject["header"])
    except KeyError:
        errorMessage = "The JSON file does not have all applicable information.\n"
        errorMessage += "Was this session created in an older version of the program?"
        return errorMessage

    #Execution is finished and error-free so return empty quotes indicating no error message
    return ""

#Return the array of samples for the current trial
def openTrial():
    return jsonObject["trials"][ts.currentSession.currentTrial - 1]["samples"]