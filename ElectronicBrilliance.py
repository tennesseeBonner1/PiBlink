
#Paste this into the bottom of MainWindow's setupUi method on regeneration of the file (from Qt Designer)...
#...to make it work with the graph.
#Note the paths of the image files might have to be updated as well.
#-------------------------------------------------------------------------------------------------------
'''
        #Set up the input manager
        import InputManager as im
        im.initialSetUp(self, icon1, icon)

        #Set up the graph
        import TheGraph as tg
        tg.initialSetUp(self)

        #Set up the display settings
        import DisplaySettingsManager as dsm
        dsm.initialSetUp()

        #Set up the json converter
        import JSONConverter as jc
        jc.initialSetUp(self)

        #Launch the time critical process
        import TimeCriticalOperations as tco
        tco.initialSetUp()
'''
#-------------------------------------------------------------------------------------------------------

#For the DisplaySettings.py regeneration, simply delete the main method at the bottom of the file.