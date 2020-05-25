# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DisplaySettingsUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_displaySettingsWindow(object):
    def setupUi(self, displaySettingsWindow):
        displaySettingsWindow.setObjectName("displaySettingsWindow")
        displaySettingsWindow.resize(525, 577)
        self.gridLayout = QtWidgets.QGridLayout(displaySettingsWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setHorizontalSpacing(50)
        self.formLayout.setObjectName("formLayout")
        self.displaySettingsLabel = QtWidgets.QLabel(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.displaySettingsLabel.setFont(font)
        self.displaySettingsLabel.setObjectName("displaySettingsLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.displaySettingsLabel)
        spacerItem = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.formLayout.setItem(1, QtWidgets.QFormLayout.LabelRole, spacerItem)
        self.displayRateLabel = QtWidgets.QLabel(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.displayRateLabel.setFont(font)
        self.displayRateLabel.setObjectName("displayRateLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.displayRateLabel)
        self.displayRateSpinBox = QtWidgets.QSpinBox(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.displayRateSpinBox.setFont(font)
        self.displayRateSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.displayRateSpinBox.setMinimum(1)
        self.displayRateSpinBox.setMaximum(120)
        self.displayRateSpinBox.setSingleStep(5)
        self.displayRateSpinBox.setProperty("value", 10)
        self.displayRateSpinBox.setObjectName("displayRateSpinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.displayRateSpinBox)
        spacerItem1 = QtWidgets.QSpacerItem(50, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.formLayout.setItem(3, QtWidgets.QFormLayout.LabelRole, spacerItem1)
        self.antiAliasingLabel = QtWidgets.QLabel(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.antiAliasingLabel.setFont(font)
        self.antiAliasingLabel.setObjectName("antiAliasingLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.antiAliasingLabel)
        self.antiAliasingComboBox = QtWidgets.QComboBox(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.antiAliasingComboBox.setFont(font)
        self.antiAliasingComboBox.setObjectName("antiAliasingComboBox")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.antiAliasingComboBox)
        self.shadingLabel = QtWidgets.QLabel(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.shadingLabel.setFont(font)
        self.shadingLabel.setObjectName("shadingLabel")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.shadingLabel)
        self.shadingComboBox = QtWidgets.QComboBox(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.shadingComboBox.setFont(font)
        self.shadingComboBox.setObjectName("shadingComboBox")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.shadingComboBox)
        spacerItem2 = QtWidgets.QSpacerItem(50, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.formLayout.setItem(6, QtWidgets.QFormLayout.LabelRole, spacerItem2)
        self.backgroundColorLabel = QtWidgets.QLabel(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.backgroundColorLabel.setFont(font)
        self.backgroundColorLabel.setObjectName("backgroundColorLabel")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.backgroundColorLabel)
        self.backgroundColorButton = QtWidgets.QPushButton(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.backgroundColorButton.setFont(font)
        self.backgroundColorButton.setText("")
        self.backgroundColorButton.setObjectName("backgroundColorButton")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.backgroundColorButton)
        self.dataColorLabel = QtWidgets.QLabel(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.dataColorLabel.setFont(font)
        self.dataColorLabel.setObjectName("dataColorLabel")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.dataColorLabel)
        self.dataColorButton = QtWidgets.QPushButton(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.dataColorButton.setFont(font)
        self.dataColorButton.setText("")
        self.dataColorButton.setObjectName("dataColorButton")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.dataColorButton)
        self.textColorLabel = QtWidgets.QLabel(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textColorLabel.setFont(font)
        self.textColorLabel.setObjectName("textColorLabel")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.textColorLabel)
        self.textColorButton = QtWidgets.QPushButton(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textColorButton.setFont(font)
        self.textColorButton.setText("")
        self.textColorButton.setObjectName("textColorButton")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.textColorButton)
        self.stimulusColorLabel = QtWidgets.QLabel(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.stimulusColorLabel.setFont(font)
        self.stimulusColorLabel.setObjectName("stimulusColorLabel")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.stimulusColorLabel)
        self.stimulusColorButton = QtWidgets.QPushButton(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.stimulusColorButton.setFont(font)
        self.stimulusColorButton.setText("")
        self.stimulusColorButton.setObjectName("stimulusColorButton")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.stimulusColorButton)
        self.axisColorLabel = QtWidgets.QLabel(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.axisColorLabel.setFont(font)
        self.axisColorLabel.setObjectName("axisColorLabel")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.axisColorLabel)
        self.axisColorButton = QtWidgets.QPushButton(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.axisColorButton.setFont(font)
        self.axisColorButton.setText("")
        self.axisColorButton.setObjectName("axisColorButton")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.axisColorButton)
        spacerItem3 = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.formLayout.setItem(12, QtWidgets.QFormLayout.LabelRole, spacerItem3)
        self.renderOffsetLabel = QtWidgets.QLabel(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.renderOffsetLabel.setFont(font)
        self.renderOffsetLabel.setObjectName("renderOffsetLabel")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.renderOffsetLabel)
        self.onsetArrowLabel = QtWidgets.QLabel(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.onsetArrowLabel.setFont(font)
        self.onsetArrowLabel.setObjectName("onsetArrowLabel")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.LabelRole, self.onsetArrowLabel)
        self.onsetArrowColorButton = QtWidgets.QPushButton(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.onsetArrowColorButton.setFont(font)
        self.onsetArrowColorButton.setText("")
        self.onsetArrowColorButton.setObjectName("onsetArrowColorButton")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.FieldRole, self.onsetArrowColorButton)
        self.offsetArrowLabel = QtWidgets.QLabel(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.offsetArrowLabel.setFont(font)
        self.offsetArrowLabel.setObjectName("offsetArrowLabel")
        self.formLayout.setWidget(15, QtWidgets.QFormLayout.LabelRole, self.offsetArrowLabel)
        self.offsetArrowColorButton = QtWidgets.QPushButton(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.offsetArrowColorButton.setFont(font)
        self.offsetArrowColorButton.setText("")
        self.offsetArrowColorButton.setObjectName("offsetArrowColorButton")
        self.formLayout.setWidget(15, QtWidgets.QFormLayout.FieldRole, self.offsetArrowColorButton)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.renderOffsetCheckBox = QtWidgets.QCheckBox(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.renderOffsetCheckBox.setFont(font)
        self.renderOffsetCheckBox.setText("")
        self.renderOffsetCheckBox.setObjectName("renderOffsetCheckBox")
        self.horizontalLayout.addWidget(self.renderOffsetCheckBox)
        spacerItem5 = QtWidgets.QSpacerItem(35, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.formLayout.setLayout(13, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(displaySettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.RestoreDefaults)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(displaySettingsWindow)
        self.buttonBox.accepted.connect(displaySettingsWindow.accept)
        self.buttonBox.rejected.connect(displaySettingsWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(displaySettingsWindow)
        displaySettingsWindow.setTabOrder(self.displayRateSpinBox, self.antiAliasingComboBox)
        displaySettingsWindow.setTabOrder(self.antiAliasingComboBox, self.shadingComboBox)
        displaySettingsWindow.setTabOrder(self.shadingComboBox, self.backgroundColorButton)
        displaySettingsWindow.setTabOrder(self.backgroundColorButton, self.dataColorButton)
        displaySettingsWindow.setTabOrder(self.dataColorButton, self.textColorButton)
        displaySettingsWindow.setTabOrder(self.textColorButton, self.stimulusColorButton)
        displaySettingsWindow.setTabOrder(self.stimulusColorButton, self.axisColorButton)
        displaySettingsWindow.setTabOrder(self.axisColorButton, self.renderOffsetCheckBox)
        displaySettingsWindow.setTabOrder(self.renderOffsetCheckBox, self.onsetArrowColorButton)
        displaySettingsWindow.setTabOrder(self.onsetArrowColorButton, self.offsetArrowColorButton)

    def retranslateUi(self, displaySettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        displaySettingsWindow.setWindowTitle(_translate("displaySettingsWindow", "Graph Display Settings"))
        self.displaySettingsLabel.setText(_translate("displaySettingsWindow", "Graph Display Settings"))
        self.displayRateLabel.setToolTip(_translate("displaySettingsWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">How often the display of the graph updates</span></p></body></html>"))
        self.displayRateLabel.setText(_translate("displaySettingsWindow", "Display Refresh Rate (Hz)"))
        self.displayRateSpinBox.setToolTip(_translate("displaySettingsWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">How often the display of the graph updates</span></p></body></html>"))
        self.antiAliasingLabel.setToolTip(_translate("displaySettingsWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">Enabling antialiasing causes lines to be drawn with smooth edges at the cost of reduced performance.</span></p></body></html>"))
        self.antiAliasingLabel.setText(_translate("displaySettingsWindow", "Anti-Aliasing"))
        self.antiAliasingComboBox.setToolTip(_translate("displaySettingsWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">Enabling antialiasing causes lines to be drawn with smooth edges at the cost of reduced performance.</span></p></body></html>"))
        self.shadingLabel.setToolTip(_translate("displaySettingsWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">The color of the area under the graph (slows down graphing significantly)</span></p></body></html>"))
        self.shadingLabel.setText(_translate("displaySettingsWindow", "Shade Area Under Curve"))
        self.shadingComboBox.setToolTip(_translate("displaySettingsWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">The color of the area under the graph (slows down graphing significantly)</span></p></body></html>"))
        self.backgroundColorLabel.setToolTip(_translate("displaySettingsWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">Color of graph background</span></p></body></html>"))
        self.backgroundColorLabel.setText(_translate("displaySettingsWindow", "Background Color"))
        self.backgroundColorButton.setToolTip(_translate("displaySettingsWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">Color of graph background</span></p></body></html>"))
        self.dataColorLabel.setToolTip(_translate("displaySettingsWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">Color of the data line plotted</span></p></body></html>"))
        self.dataColorLabel.setText(_translate("displaySettingsWindow", "Data Color"))
        self.dataColorButton.setToolTip(_translate("displaySettingsWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">Color of the data line plotted</span></p></body></html>"))
        self.textColorLabel.setText(_translate("displaySettingsWindow", "Text Color"))
        self.stimulusColorLabel.setToolTip(_translate("displaySettingsWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">Color of area denoting conditioned and unconditioned stimulus </span></p></body></html>"))
        self.stimulusColorLabel.setText(_translate("displaySettingsWindow", "Stimulus Color"))
        self.stimulusColorButton.setToolTip(_translate("displaySettingsWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">Color of area denoting conditioned and unconditioned stimulus </span></p></body></html>"))
        self.axisColorLabel.setToolTip(_translate("displaySettingsWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">The color of the axis the graph is plotted on</span></p></body></html>"))
        self.axisColorLabel.setText(_translate("displaySettingsWindow", "Axis Color"))
        self.axisColorButton.setToolTip(_translate("displaySettingsWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">The color of the axis the graph is plotted on</span></p></body></html>"))
        self.renderOffsetLabel.setToolTip(_translate("displaySettingsWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">Whether or not to show arrows for the eyeblink offsets</span></p></body></html>"))
        self.renderOffsetLabel.setText(_translate("displaySettingsWindow", "Render Offset Arrows"))
        self.onsetArrowLabel.setText(_translate("displaySettingsWindow", "Onset Arrow Color"))
        self.offsetArrowLabel.setText(_translate("displaySettingsWindow", "Offset Arrow Color"))
