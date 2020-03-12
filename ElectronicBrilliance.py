
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
        
        #Complete set up of the main window (this file)
        self.subjectSexComboBox.addItem("MALE")
        self.subjectSexComboBox.addItem("FEMALE")
'''
#-------------------------------------------------------------------------------------------------------