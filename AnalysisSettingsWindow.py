""" AnalysisSettingsWindow.py
    Last Modified: 5/6/2020
    Taha Arshad, Tennessee Bonner, Devin Mensah, Khalid Shaik, Collin Vaille
    
    This program sets up all of the UI in the Analysis Settings Window
"""
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AnalysisSettingsWindow(object):
    def setupUi(self, AnalysisSettingsWindow):
        AnalysisSettingsWindow.setObjectName("AnalysisSettingsWindow")
        AnalysisSettingsWindow.resize(297, 370)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AnalysisSettingsWindow.sizePolicy().hasHeightForWidth())
        AnalysisSettingsWindow.setSizePolicy(sizePolicy)
        AnalysisSettingsWindow.setMinimumSize(QtCore.QSize(297, 370))
        AnalysisSettingsWindow.setMaximumSize(QtCore.QSize(297, 370))
        AnalysisSettingsWindow.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(AnalysisSettingsWindow)
        self.verticalLayout.setContentsMargins(20, 15, 20, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_ThresholdSettings = QtWidgets.QLabel(AnalysisSettingsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ThresholdSettings.sizePolicy().hasHeightForWidth())
        self.label_ThresholdSettings.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_ThresholdSettings.setFont(font)
        self.label_ThresholdSettings.setWhatsThis("")
        self.label_ThresholdSettings.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_ThresholdSettings.setObjectName("label_ThresholdSettings")
        self.verticalLayout.addWidget(self.label_ThresholdSettings)
        self.formLayout_Threshold = QtWidgets.QFormLayout()
        self.formLayout_Threshold.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_Threshold.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_Threshold.setContentsMargins(10, -1, -1, 10)
        self.formLayout_Threshold.setHorizontalSpacing(20)
        self.formLayout_Threshold.setVerticalSpacing(15)
        self.formLayout_Threshold.setObjectName("formLayout_Threshold")
        self.label_StdDev = QtWidgets.QLabel(AnalysisSettingsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_StdDev.sizePolicy().hasHeightForWidth())
        self.label_StdDev.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_StdDev.setFont(font)
        self.label_StdDev.setMouseTracking(False)
        self.label_StdDev.setToolTip("")
        self.label_StdDev.setWordWrap(False)
        self.label_StdDev.setObjectName("label_StdDev")
        self.formLayout_Threshold.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_StdDev)
        self.label_MinDuration = QtWidgets.QLabel(AnalysisSettingsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_MinDuration.sizePolicy().hasHeightForWidth())
        self.label_MinDuration.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_MinDuration.setFont(font)
        self.label_MinDuration.setToolTip("")
        self.label_MinDuration.setStatusTip("")
        self.label_MinDuration.setWordWrap(True)
        self.label_MinDuration.setObjectName("label_MinDuration")
        self.formLayout_Threshold.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_MinDuration)
        self.spinBox_MinDuration = QtWidgets.QSpinBox(AnalysisSettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.spinBox_MinDuration.setFont(font)
        self.spinBox_MinDuration.setToolTip("")
        self.spinBox_MinDuration.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_MinDuration.setMinimum(1)
        self.spinBox_MinDuration.setMaximum(1000)
        self.spinBox_MinDuration.setSingleStep(1)
        self.spinBox_MinDuration.setProperty("value", 10)
        self.spinBox_MinDuration.setObjectName("spinBox_MinDuration")
        self.formLayout_Threshold.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBox_MinDuration)
        self.spinBox_StdDev = QtWidgets.QSpinBox(AnalysisSettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.spinBox_StdDev.setFont(font)
        self.spinBox_StdDev.setMouseTracking(True)
        self.spinBox_StdDev.setToolTip("")
        self.spinBox_StdDev.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_StdDev.setMinimum(1)
        self.spinBox_StdDev.setMaximum(20)
        self.spinBox_StdDev.setProperty("value", 4)
        self.spinBox_StdDev.setObjectName("spinBox_StdDev")
        self.formLayout_Threshold.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBox_StdDev)
        self.verticalLayout.addLayout(self.formLayout_Threshold)
        self.label_FileSettings = QtWidgets.QLabel(AnalysisSettingsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_FileSettings.sizePolicy().hasHeightForWidth())
        self.label_FileSettings.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_FileSettings.setFont(font)
        self.label_FileSettings.setObjectName("label_FileSettings")
        self.verticalLayout.addWidget(self.label_FileSettings)
        self.gridLayout_File = QtWidgets.QGridLayout()
        self.gridLayout_File.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_File.setContentsMargins(10, 0, 10, 15)
        self.gridLayout_File.setHorizontalSpacing(5)
        self.gridLayout_File.setVerticalSpacing(0)
        self.gridLayout_File.setObjectName("gridLayout_File")
        self.label_Overwrite = QtWidgets.QLabel(AnalysisSettingsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Overwrite.sizePolicy().hasHeightForWidth())
        self.label_Overwrite.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_Overwrite.setFont(font)
        self.label_Overwrite.setWordWrap(True)
        self.label_Overwrite.setObjectName("label_Overwrite")
        self.gridLayout_File.addWidget(self.label_Overwrite, 0, 0, 1, 1)
        self.radioButton_Overwrite = QtWidgets.QRadioButton(AnalysisSettingsWindow)
        self.radioButton_Overwrite.setMinimumSize(QtCore.QSize(0, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.radioButton_Overwrite.setFont(font)
        self.radioButton_Overwrite.setText("")
        self.radioButton_Overwrite.setCheckable(True)
        self.radioButton_Overwrite.setChecked(True)
        self.radioButton_Overwrite.setObjectName("radioButton_Overwrite")
        self.gridLayout_File.addWidget(self.radioButton_Overwrite, 0, 1, 1, 1)
        self.radioButton_GenerateNew = QtWidgets.QRadioButton(AnalysisSettingsWindow)
        self.radioButton_GenerateNew.setText("")
        self.radioButton_GenerateNew.setObjectName("radioButton_GenerateNew")
        self.gridLayout_File.addWidget(self.radioButton_GenerateNew, 1, 1, 1, 1)
        self.label_GenerateNew = QtWidgets.QLabel(AnalysisSettingsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_GenerateNew.sizePolicy().hasHeightForWidth())
        self.label_GenerateNew.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_GenerateNew.setFont(font)
        self.label_GenerateNew.setWordWrap(True)
        self.label_GenerateNew.setObjectName("label_GenerateNew")
        self.gridLayout_File.addWidget(self.label_GenerateNew, 1, 0, 1, 1)
        self.lineEdit_customSaveName = QtWidgets.QLineEdit(AnalysisSettingsWindow)
        self.lineEdit_customSaveName.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_customSaveName.setFont(font)
        self.lineEdit_customSaveName.setFrame(True)
        self.lineEdit_customSaveName.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_customSaveName.setPlaceholderText("")
        self.lineEdit_customSaveName.setObjectName("lineEdit_customSaveName")
        self.gridLayout_File.addWidget(self.lineEdit_customSaveName, 2, 0, 1, 2)
        self.gridLayout_File.setColumnStretch(0, 5)
        self.gridLayout_File.setRowStretch(0, 3)
        self.gridLayout_File.setRowStretch(1, 3)
        self.gridLayout_File.setRowStretch(2, 1)
        self.verticalLayout.addLayout(self.gridLayout_File)
        self.line = QtWidgets.QFrame(AnalysisSettingsWindow)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_buttons = QtWidgets.QHBoxLayout()
        self.horizontalLayout_buttons.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_buttons.setObjectName("horizontalLayout_buttons")
        self.pushButton_ReAnalyze = QtWidgets.QPushButton(AnalysisSettingsWindow)
        self.pushButton_ReAnalyze.setObjectName("pushButton_ReAnalyze")
        self.horizontalLayout_buttons.addWidget(self.pushButton_ReAnalyze)
        self.pushButton_Cancel = QtWidgets.QPushButton(AnalysisSettingsWindow)
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.horizontalLayout_buttons.addWidget(self.pushButton_Cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_buttons)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 3)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 3)
        self.verticalLayout.setStretch(4, 1)
        self.verticalLayout.setStretch(5, 1)

        self.retranslateUi(AnalysisSettingsWindow)
        self.pushButton_Cancel.released.connect(AnalysisSettingsWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(AnalysisSettingsWindow)

    def retranslateUi(self, AnalysisSettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        AnalysisSettingsWindow.setWindowTitle(_translate("AnalysisSettingsWindow", "Analysis Settings"))
        self.label_ThresholdSettings.setText(_translate("AnalysisSettingsWindow", "Threshold Settings"))
        self.label_StdDev.setWhatsThis(_translate("AnalysisSettingsWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">The number of standard deviations away from the average that the sample must be in order to be above the eyeblink threshold</span></p></body></html>"))
        self.label_StdDev.setText(_translate("AnalysisSettingsWindow", "Standard Deviations"))
        self.label_MinDuration.setWhatsThis(_translate("AnalysisSettingsWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">The minimum amount of time that the signal must be above the threshold in order to register as an eyeblink onset.</span></p><p><span style=\" font-size:12pt;\">Higher values make the analysis less susceptible to noise</span></p></body></html>"))
        self.label_MinDuration.setText(_translate("AnalysisSettingsWindow", "Minimum Duration Required (ms)"))
        self.spinBox_MinDuration.setWhatsThis(_translate("AnalysisSettingsWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">The minimum amount of time that the signal must be above the threshold in order to register as an eyeblink onset.</span></p><p><span style=\" font-size:12pt;\">Higher values make the analysis less susceptible to noise</span></p></body></html>"))
        self.spinBox_StdDev.setWhatsThis(_translate("AnalysisSettingsWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">The number of standard deviations away from the average that the sample must be in order to be above the eyeblink threshold</span></p></body></html>"))
        self.label_FileSettings.setText(_translate("AnalysisSettingsWindow", "File Settings"))
        self.label_Overwrite.setWhatsThis(_translate("AnalysisSettingsWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Replaces the current onset and offsest values of the file with the new ones. </span></p></body></html>"))
        self.label_Overwrite.setText(_translate("AnalysisSettingsWindow", "Overwrite Current File"))
        self.radioButton_Overwrite.setWhatsThis(_translate("AnalysisSettingsWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Replaces the current onset and offsest values of the file with the new ones. </span></p></body></html>"))
        self.radioButton_GenerateNew.setWhatsThis(_translate("AnalysisSettingsWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">The file generated will be saved under the name specified in the following line editor</span></p></body></html>"))
        self.label_GenerateNew.setWhatsThis(_translate("AnalysisSettingsWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">The file generated will be saved under the name specified in the following line editor</span></p></body></html>"))
        self.label_GenerateNew.setText(_translate("AnalysisSettingsWindow", "Save as Custom Name"))
        self.lineEdit_customSaveName.setWhatsThis(_translate("AnalysisSettingsWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Holds the custom filename that the generated file will be saved under (if &quot;Save as Custom Name&quot; is enabled). The &quot;.json&quot; does not need to be included.</span></p><p><span style=\" font-size:12pt;\">Please note that the filename is </span><span style=\" font-size:12pt; font-weight:600;\">not</span><span style=\" font-size:12pt;\"> the same as the session name.</span></p><p><span style=\" font-size:12pt;\">May not contain any of the following characters: \\ / : * ? &quot; &lt; &gt; |</span></p></body></html>"))
        self.pushButton_ReAnalyze.setText(_translate("AnalysisSettingsWindow", "Re-Analyze"))
        self.pushButton_Cancel.setText(_translate("AnalysisSettingsWindow", "Cancel"))
