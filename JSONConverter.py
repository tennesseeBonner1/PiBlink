""" JSONConverter.py
    Last Modified: 5/4/2020
    Taha Arshad, Tennessee Bonner, Devin Mensah Khalid Shaik, Collin Vaille

    This file's responsibilities are to:
    1. Save sessions as JSON files.
    2. Open the JSON saved session files.
    3. Provide a few common functionalities related to file management.
    
    At the top layer of the dictionary structure, there are two key-value pairs. The two keys are "header" and "trials"
    The value mapped to the "header" key is another dictionary containing key-value pairs that relate to the session-specific settings 
    ("name", "sex", "age", "trialDuration", etc.) The value mapped to the "trials" key is an array of dictionaries, where each dictionary 
    holds the information for a single trial. Within these trial dictionaries are a few key-value pairs, including a pair which contains 
    the stats of the trial (another dictionary), and a pair which maps a key to an array containing all of the sample data.
"""
import TheSession as ts
import DataAnalysis as da
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
                        "usDuration": ts.currentSession.usDuration,
                        "usDelay": ts.currentSession.usDelay,
                        "thresholdStdDev": ts.currentSession.thresholdStdDev,
                        "thresholdMinDuration": ts.currentSession.thresholdMinDuration
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
                       "stats": da.getTrialStats(ts.currentSession.thresholdStdDev, ts.currentSession.thresholdMinDuration),
                       "samples": trialDataList
                  }

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


#Opens JSON file, reads in JSON data, recreates session object with data
def openSession(filename):

    global jsonObject, saveFilename

    #Open file, extract contents into string, and close the file
    try:
        sessionFile = open(file = filename, mode = "r")
        saveFilename = filename
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


#Returns the array of samples for the current trial
def openTrial():

    return jsonObject["trials"][ts.currentSession.currentTrial - 1]["samples"]


#Returns the array of onsets for the current trial
def getOnsets():

    return jsonObject["trials"][ts.currentSession.currentTrial - 1]["stats"]["onsetSamples"]


#Returns the array of offsets for the current trial
def getOffsets():

    return jsonObject["trials"][ts.currentSession.currentTrial - 1]["stats"]["offsetSamples"]


#Creates a saved session directory if one doesn't exist
def getSavedSessionDirectory(createIfNonexistent):

    #Subfolder of current working dir
    savedSessionDirectory = os.path.join(os.getcwd(), "Saved Sessions")

    #Make the directory if required to exist
    if createIfNonexistent and (not os.path.exists(savedSessionDirectory)):
        os.makedirs(savedSessionDirectory)

    return savedSessionDirectory


#Gets the filename of the currently open file and returns it
def getCurrentFilename():

	#Partition the lengthy pathname to get only the file name (checking for both \ and / to be safe)
	justTheName = saveFilename.rpartition('\\')[2]
	justTheName = justTheName.rpartition('/')[2]

	#remove the file extension
	justTheName = justTheName.rpartition('.')[0]
	
	return justTheName
