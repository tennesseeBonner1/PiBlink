# CsCrMachineCode
As of 5/2/2020, the project is comprised of the files listed below.\
The general categories of files are:
- Main Files
- Reference Files
- UI Files
- UI Manager Files
- Session Files

---
### Main Files
- **DataAnalysis.py**:

- **DataWizard.py**:
    Handles all of the analog input and outputs.

- **ElectronicBrilliance.py**:
    Contains a few lines of code that are added to a .py file after it is converted from 
    a .ui file.

- **GraphExporter.py**:
    Exports a screenshot of the graph as an image file.

- **InputManager.py**:
    This file controls the majority of the program and waits for input from one of the 
	top three buttons. Once the settings for the session are set, the program will mostly 
	operate through TheGraph.py.

- **JSONConverter.py**:
    Used to save sessions as JSON files and open them back up for playback. TheGraph.py
	uses this file to save/read trials and InputManager.py uses this file to save/read
	session settings and start/end the save/read process for the whole session.

- **MainWindow.py**:
    All of the settings for the main window are initialized and all of the 
	various text elements are modified and updated in this file.

- **NoiseWizard.py**:
    Used instead of DataWizard to generate a set of random data to test the program 
	without the use of the data read from the DAC and DAC converter.

- **TheGraph.py**:
    This file controls all of the visuals in the graph and displays the information as 
	it updates.

- **TheSession.py**:
    This session file is a singleton instance that saves all of the settings for 
	the session (the series of trials). The file also has the initial constructor for a 
	new session (which reads in the settings from the GUI and coverts all mesurements 
	from seconds and milliseconds to samples).

- **TimeCriticalOperations.py**:

	
### Reference Files
- **DAC8552_default_config.py**:
    Part of the default files included for the DAC conversion (needed to output the 
	signals for the CS and US).

- **dac8552.py**:
    Part of the default files included for the DAC conversion (needed to output the 
	signals for the US and UCS).	


### UI Files
These are the editable pyqt5 files that can be updated in the pyqt5 designer. These 
are then converted to .py files. There are also image files for the buttons used in GUIs
that are included but not listed here. 

- **AnalysisSettingsUI.ui** & **AnalysisSettingsWindow.py**:

- **DisplaySettingsUI.ui** & **DisplaySettingsWindow.py**:
    All the settings for the display settings window are initialized and all of the 
	various text elements of this window are modified and updated.

- **MainUI.ui** & **MainWindow.py**:

- **MatrixParametersUI.ui** & **MatrixParametersWindow.py**:

- **MatrixViewUI.ui** & **MatrixViewWindow.py**:


### UI Manager Files
- **AnalysisSettingsManager.py**:

- **DisplaySettingsManager.py**:
    Sets up all the display settings and parses the display settings text file to set them.

- **Display Settings.txt**:
    This is read to set the settings for the graph. This file is edited by the display 
	settings window. The file is currently regenerated on save.

- **MainWindow.py**:

- **MatrixManager.py**:


### Session Files	
- **.json files**:
    These are the saved session files. If the user tries to save a session with the same name as
	an already saved session, a numbering scheme will ensure the new session is given a new name
	and the old one is not overwritten.

- **Capture Files**
