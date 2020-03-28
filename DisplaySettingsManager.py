
#Module for all management of the display settings. This management is comprised of 3 things...
#1. Managing the pop-up window (in DisplaySettingsWindow.py) for viewing and editing these settings.
#2. Managing the text file (Display Settings.txt) for saving these settings.
#3. Managing the program variables that hold the current state of these settings (ex: dsm.displayRate)

from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog
from enum import Enum
import DisplaySettingsWindow as dsw

class ColorAttribute(Enum):
    BACKGROUND = 0
    DATA = 1
    TEXT = 2
    STIMULUS = 3
    AXIS = 4

#Needs to be called at the very beginning of the program to load in settings from file
def initialSetUp ():
    global displayRate, antiAliasing, shading, colors

    #Give default values to all settings first (in case loading settings from file fails)...
    displayRate = 10
    
    antiAliasing = False
    shading = False

    #Default colors for each of the five color categories (see ColorAttribute enum for ordering)
    colors = (QtGui.QColor(255, 255, 255),
                QtGui.QColor(0, 0, 255),
                QtGui.QColor(0, 0, 0),
                QtGui.QColor(75, 75, 75),
                QtGui.QColor(0, 0, 0))

    #Then try to read in settings from file...
    try:
        #Open the display settings file in read mode
        displaySettingsFile = open(file = "Display Settings.txt", mode = "r")
    except Exception as e: #Error
        print("Error opening display settings file...\n")
        print(e) #Detailed error message
        print() #Extra line for spacing
    else: #Executed only if there is no error with opening the file
        #Parse line by line for settings
        for line in displaySettingsFile:
            parseDisplaySettingsFileLine(line)

        #Close the file when done to avoid file descriptor memory leaks
        displaySettingsFile.close()

def parseDisplaySettingsFileLine (line):
    global displayRate, antiAliasing, shading, colors

    #Split the line into key/value pair
    keyValuePair = line.split(sep = "=", maxsplit = 2)

    #Not a key/value pair so skip line (probably whitespace or a comment or something)
    if len(keyValuePair) != 2:
        return

    #Extract key, remove any surrounding whitespace, and make it all lower case (for case insensitivity)
    key = keyValuePair[0].strip().lower()

    #Same for value
    value = keyValuePair[1].strip().lower()

    #Examine key and save corresponding value
    if key == "refresh rate":
        displayRate = int(value)
    elif key == "anti-aliasing":
        antiAliasing = value == "true"
    elif key == "shading":
        shading = value == "true"
    elif key == "background color":
        colors[ColorAttribute.BACKGROUND.value].setNamedColor(value)
    elif key == "data color":
        colors[ColorAttribute.DATA.value].setNamedColor(value)
    elif key == "text color":
        colors[ColorAttribute.TEXT.value].setNamedColor(value)
    elif key == "stimulus color":
        colors[ColorAttribute.STIMULUS.value].setNamedColor(value)
    elif key == "axis color":
        colors[ColorAttribute.AXIS.value].setNamedColor(value)

#Called when "Edit -> Display Settings..." is pressed to pop up the display settings menu
def openDisplaySettingsMenu():
    global displaySettingsWrapper, colorButtons

    #Create the display settings menu (using the Qt Designer-generated Ui_displaySettings)
    displaySettingsWindow = QDialog()
    displaySettingsWrapper = dsw.Ui_displaySettingsWindow()
    displaySettingsWrapper.setupUi(displaySettingsWindow)

    #Now perform the rest of the set up in code below...

    #Detects when the "Restore Defaults" or "OK" buttons are pressed respectively
    #"Cancel" doesn't need one because no additional actions are needed (window closes automatically)
    #Used 0x08000000 instead of QtGui.QDialogButtonBox.Reset due to import issues (they're interchangeable)
    displaySettingsWrapper.buttonBox.button(0x08000000).clicked.connect(restoreDisplayDefaults)
    displaySettingsWrapper.buttonBox.accepted.connect(saveDisplaySettings)

    #Keep track of the color buttons in tuple format for easier access
    colorButtons = (displaySettingsWrapper.backgroundColorButton,
                    displaySettingsWrapper.dataColorButton,
                    displaySettingsWrapper.textColorButton,
                    displaySettingsWrapper.stimulusColorButton,
                    displaySettingsWrapper.axisColorButton)

    #Detects when the color buttons are pressed
    colorButtons[0].clicked.connect(lambda: colorButtonPressed(ColorAttribute.BACKGROUND))
    colorButtons[1].clicked.connect(lambda: colorButtonPressed(ColorAttribute.DATA))
    colorButtons[2].clicked.connect(lambda: colorButtonPressed(ColorAttribute.TEXT))
    colorButtons[3].clicked.connect(lambda: colorButtonPressed(ColorAttribute.STIMULUS))
    colorButtons[4].clicked.connect(lambda: colorButtonPressed(ColorAttribute.AXIS))

    #Make the menu not resizable
    displaySettingsWindow.setFixedSize(displaySettingsWindow.size())

    #Fill in the options for the combo boxes
    displaySettingsWrapper.antiAliasingComboBox.addItem("DISABLED (Faster)")
    displaySettingsWrapper.antiAliasingComboBox.addItem("ENABLED (Slower)")
    displaySettingsWrapper.shadingComboBox.addItem("DISABLED (Faster)")
    displaySettingsWrapper.shadingComboBox.addItem("ENABLED (Slower)")

    #Set the values of these settings to the currently selected values
    showDisplaySettings()

    #Display the menu
    displaySettingsWindow.exec()

#Called when "Restore defaults" buttons is pressed on graph display settings menu
def restoreDisplayDefaults():
    displaySettingsWrapper.displayRateSpinBox.setValue(10)

    displaySettingsWrapper.antiAliasingComboBox.setCurrentIndex(0)
    displaySettingsWrapper.shadingComboBox.setCurrentIndex(0)

    #Set color to buttons
    displaySettingsWrapper.backgroundColorButton.setStyleSheet("background-color: white")
    displaySettingsWrapper.dataColorButton.setStyleSheet("background-color: blue")
    displaySettingsWrapper.textColorButton.setStyleSheet("background-color: black")
    displaySettingsWrapper.stimulusColorButton.setStyleSheet("background-color: rgb(75, 75, 75)")
    displaySettingsWrapper.axisColorButton.setStyleSheet("background-color: black")

#Called when "OK" button is pressed on graph display settings menu
def saveDisplaySettings():
    global displayRate, antiAliasing, shading, colors

    #First, extract display settings from menu...
    displayRate = displaySettingsWrapper.displayRateSpinBox.value()
    
    antiAliasing = displaySettingsWrapper.antiAliasingComboBox.currentIndex() == 1
    shading = displaySettingsWrapper.shadingComboBox.currentIndex() == 1

    colors = (colorButtons[0].palette().button().color(),
              colorButtons[1].palette().button().color(),
              colorButtons[2].palette().button().color(),
              colorButtons[3].palette().button().color(),
              colorButtons[4].palette().button().color())

    #Then, save settings to file...
    try:
        #Open the display settings file in write mode (overwrites anything already in it, no appending)
        displaySettingsFile = open(file = "Display Settings.txt", mode = "w")
    except Exception as e: #Error
        print("Error opening display settings file...\n")
        print(e) #Detailed error message
        print() #Extra empty line for spacing
    else: #Executed only if there is no error with opening the file
        displaySettingsFile.write("Note: Don't comment this file because it is regenerated on save.")

        displaySettingsFile.write("\n\nrefresh rate = " + str(displayRate))

        displaySettingsFile.write("\n\nanti-aliasing = " + ("true" if antiAliasing else "false"))
        displaySettingsFile.write("\nshading = " + ("true" if shading else "false"))

        displaySettingsFile.write("\n\nbackground color = " + colors[ColorAttribute.BACKGROUND.value].name())
        displaySettingsFile.write("\ndata color = " + colors[ColorAttribute.DATA.value].name())
        displaySettingsFile.write("\ntext color = " + colors[ColorAttribute.TEXT.value].name())
        displaySettingsFile.write("\nstimulus color = " + colors[ColorAttribute.STIMULUS.value].name())
        displaySettingsFile.write("\naxis color = " + colors[ColorAttribute.AXIS.value].name())

        #Close the file when done to avoid file descriptor memory leaks
        displaySettingsFile.close()

#Called when display menu is created to fill in the options with the current settings
def showDisplaySettings():
    displaySettingsWrapper.displayRateSpinBox.setValue(displayRate)

    displaySettingsWrapper.antiAliasingComboBox.setCurrentIndex(int(antiAliasing))
    displaySettingsWrapper.shadingComboBox.setCurrentIndex(int(shading))

    #Set color to button in background
    for x in range(0, 5):
        colorButtons[x].setStyleSheet("background-color: " + colors[x].name())

#Pulls up color picker for changing the color of the button
#This function is used by all color buttons, differentiating between buttons via parameter
def colorButtonPressed(colorAttribute):
    #Retrieve current color (of type QColor)
    color = colorButtons[colorAttribute.value].palette().button().color()

    #Open color picker (use current color as initial color in color picker)
    color = QtGui.QColorDialog.getColor(initial = color)
    
    #If the user didn't click cancel on color picker, set color to chosen color
    if color.isValid():
        colorButtons[colorAttribute.value].setStyleSheet("background-color: " + color.name())