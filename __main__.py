
'''
    Run this file to start the program.

    This file contains...
    1. The main function
    2. The error handler for all otherwise uncaught exceptions
    
    The main function calls all the initialSetUp functions, manages and opens the main window,
    hooks up the error handler (described below), and starts the Qt event loop (used for UI
    input handling).

    The error handler ensures that all necessary clean up is performed before exiting on a crash.
'''

from traceback import format_exception
from PyQt5 import QtWidgets

import MainWindow as mw
import InputManager as im
import TheGraph as tg
import DisplaySettingsManager as dsm
import JSONConverter as jc
import TimeCriticalOperations as tco

#Called whenever there is an error in the main process
def mainProcessErrorHandler(exceptionType, exceptionValue, exceptionTraceback):
    #Print error
    print(format_exception(exceptionType, exceptionValue, exceptionTraceback))
    
    #End sampling process
    tco.orderToStopProcess()

    #Tell PyQt system to quit (otherwise the windows hang)
    im.closeWindowsOnCrash()

    #End main process
    sys.exit(0)

#Main method
if __name__ == "__main__":
    #Necessary initialization for Qt system
    import sys
    app = QtWidgets.QApplication(sys.argv)

    #Create and set up the main window
    MainWindow = QtWidgets.QMainWindow()
    ui = mw.Ui_MainWindow()
    ui.setupUi(MainWindow)

    #If there's an error in the main process, we need special error handling to close the...
    #child process, i.e. the sampling process, so it doesn't become a zombie.
    sys.excepthook = mainProcessErrorHandler

    #Perform all necessary set up including launching the time critical (sampling) process
    im.initialSetUp(ui)
    tg.initialSetUp(ui)
    dsm.initialSetUp()
    jc.initialSetUp(ui)
    tco.initialSetUp()

    #Start of program
    MainWindow.show()
    app.exec_() #Run the main Qt Event loop (for listening to UI input)
    
    #End of program
    tco.orderToStopProcess() #Make sure the sampling process terminates
    sys.exit(0) #Exit program with no errors