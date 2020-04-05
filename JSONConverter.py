import TheSession as ts
import datetime as dt
import json
import os.path
from os import path
from datetime import datetime

#Called on start of program to perform initialization (i.e. getting reference to main window)
def initialSetUp (theMainWindow):
    global mainWindow

    mainWindow = theMainWindow

def startDataAcquisition():
    global trialsSaved, saveFileName, jsonObject
    
    trialsSaved = 0

    name = str(ts.currentSession.sessionName)
    if (name == ""):
        name = "NULLNAME"
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

    number = 1

    saveFileName = (name + str(number) + " (" + sex + " " + age + ") " + date + ".json")

    while (path.exists(saveFileName)):
        number += 1
        saveFileName = (name + str(number) + " (" + sex + " " + age + ") " + date + ".json")
        print("uh oh buster")

    jsonObject = {
                    "header":   {
                        "name" : name,
                        "sex" : sex,
                        "age" : age,
                        "sampleInterval": ts.currentSession.sampleInterval,
                        "trialCount": ts.currentSession.trialCount,
                        "iti" : ts.currentSession.iti,
                        "itiVariance" : ts.currentSession.itiVariance,
                        "trialDuration" : ts.currentSession.trialDuration,
                        "baselineDuration" : ts.currentSession.baselineDuration,
                        "csName" : ts.currentSession.csName,
                        "csDuration" : ts.currentSession.csDuration,
                        "isi" : ts.currentSession.interstimulusInterval,
                        "usName" : ts.currentSession.usName,
                        "usDuration" : ts.currentSession.usDuration
                    },

                    "trials": []
                }

def saveTrial(trialDataArray):
    global trialsSaved

    trialsSaved += 1

    #Convert trial data from numpy array to python list
    trialDataList = trialDataArray.tolist()

    #Convert python list to json string
    trialDataString = json.dumps(trialDataList)

    #Create trial object and append it to trials object (which is a part of the larger json object)
    jsonObject["trials"].append(trialDataList)

#Finalize data acquisition by writing session (stored in JSON object) out to JSON file
#Before this point, data has just been accumulating in the JSON object with no file saving
def endDataAcquisition():
    #If the data acquisition session was ended before completion, remember how many actually got saved
    jsonObject["header"]["trialCount"] = str(trialsSaved)

    #Only proceed with saving the session to file if it has a non-zero number of trials
    if trialsSaved > 0:
        #Open new file in write mode (overwrites any preexisting file with same name)
        sessionFile = open(saveFileName, "w")

        #Write JSON object to file
        jsonString = json.dumps(jsonObject) #Convert JSON object to string
        sessionFile.write(jsonString) #Write string to file

        #Close file
        sessionFile.close()

#Opens JSON file, reads in JSON data, recreates session object with data
#After this function is called, the user can press the play button to begin playback
def openSession(filename):
    global jsonObject

    #Open file, extract contents into string, and close the file
    sessionFile = open(file = filename, mode = "r")
    jsonString = sessionFile.read()
    sessionFile.close()

    #Convert string into python dictionary
    jsonObject = json.loads(jsonString)

    #Recreate session object using the settings in the header of the json file
    ts.currentSession = ts.TheSession(mainWindow, jsonObject["header"])

    openFirstTrial()

#Set read trackers to first sample of first trial
def openFirstTrial():
    global nextSample, nextTrial

    nextSample = -1
    nextTrial = -1

#Get next input value (sample)
def getEyeblinkAmplitude():
    global nextSample

    nextSample += 1

    return trialData[nextSample]

#Move trackers to read from the next trial
def openNextTrial():
    global nextSample, nextTrial, trialData

    nextSample = -1
    nextTrial += 1

    trialData = jsonObject["trials"][nextTrial]
