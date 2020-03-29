# CsCrMachineCode
The following are all of the data files included in this project as of 3/29/2020

DAC8552_default_config.py
	Part of the default files included for the DAC conversion (needed to output the 
	signals for the US and UCS) 

DataWizard.py
	Handles all of the analog input and outputs.

Display Settings.txt
	This is read to set the settings for the graph. This file is edited by the display 
	settings window. The file is currently regenerated on save.

DisplaySettingsManager.py
	Sets up all the display settings and parses the display settings text file to set them
	
DisplaySettingsWindow.py 
	All the settings for the display settings window are initialized and all of the 
	varios text elements of this window are modified and updated

ElectronicBrilliance.py
	Contains a few lines of code that are added to a .py file after it is converted from 
	a .ui file.

GraphExporter.py
	Exports a screenshot of the graph as a image file. 

InputManager.py
	This file controls the majority of the program and waits for input from one of the 
	top three buttons. Once the settings for the session are set, the program will mostly 
	operate through the graph.py

MainWindow.py
	All of the settings for the main window are initialized and all of the 
	various text elements are modified and updated in this file.

NoiseWizard.py
	Used instead of DataWizard to generate a set of random data to test the program 
	without the use of the data read from the DAC and DAC converter

TheGraph.py
	This file controlls all of the visuals in the graph and displays the information as 
	it updates.

TheSession.py
	This session file is a singleton instance that saves all of the settings for 
	the session (the series of trials). The file also has the initial constructor for a 
	new session (which reads in the settings from the GUI and coverts all mesurements 
	from seconds and milliseconds to samples)

dac8552.py
	Part of the default files included for the DAC conversion (needed to output the 
	signals for the US and UCS) 

.ui files
	These are the editable pyqt5 files that can be updated in the pyqt5 designer. These 
	are then converted to .py files
