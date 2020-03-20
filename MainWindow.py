# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\colli\source\repos\NMOne\NMOne\MainUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1324, 733)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.rootHorizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.rootHorizontalLayout.setObjectName("rootHorizontalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(485, 0))
        self.scrollArea.setMaximumSize(QtCore.QSize(500, 16777215))
        self.scrollArea.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 462, 801))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.formLayout_2 = QtWidgets.QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout_2.setObjectName("formLayout_2")
        self.sessionSettings = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.sessionSettings.setFont(font)
        self.sessionSettings.setObjectName("sessionSettings")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.sessionSettings)
        self.sessionName = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sessionName.setFont(font)
        self.sessionName.setObjectName("sessionName")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.sessionName)
        self.sampleIntervalLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sampleIntervalLabel.setFont(font)
        self.sampleIntervalLabel.setObjectName("sampleIntervalLabel")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.sampleIntervalLabel)
        self.sampleIntervalSpinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.sampleIntervalSpinBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sampleIntervalSpinBox.sizePolicy().hasHeightForWidth())
        self.sampleIntervalSpinBox.setSizePolicy(sizePolicy)
        self.sampleIntervalSpinBox.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sampleIntervalSpinBox.setFont(font)
        self.sampleIntervalSpinBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.sampleIntervalSpinBox.setSuffix("")
        self.sampleIntervalSpinBox.setMinimum(1)
        self.sampleIntervalSpinBox.setMaximum(1000)
        self.sampleIntervalSpinBox.setProperty("value", 1)
        self.sampleIntervalSpinBox.setObjectName("sampleIntervalSpinBox")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.sampleIntervalSpinBox)
        self.trialCountLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.trialCountLabel.setFont(font)
        self.trialCountLabel.setObjectName("trialCountLabel")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.trialCountLabel)
        self.trialCountSpinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trialCountSpinBox.sizePolicy().hasHeightForWidth())
        self.trialCountSpinBox.setSizePolicy(sizePolicy)
        self.trialCountSpinBox.setMinimumSize(QtCore.QSize(125, 0))
        self.trialCountSpinBox.setMaximumSize(QtCore.QSize(125, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.trialCountSpinBox.setFont(font)
        self.trialCountSpinBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.trialCountSpinBox.setSuffix("")
        self.trialCountSpinBox.setMinimum(1)
        self.trialCountSpinBox.setMaximum(10000000)
        self.trialCountSpinBox.setSingleStep(5)
        self.trialCountSpinBox.setProperty("value", 60)
        self.trialCountSpinBox.setObjectName("trialCountSpinBox")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.trialCountSpinBox)
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.formLayout_2.setItem(9, QtWidgets.QFormLayout.LabelRole, spacerItem)
        self.itiLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.itiLabel.setFont(font)
        self.itiLabel.setObjectName("itiLabel")
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.itiLabel)
        self.itiSpinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.itiSpinBox.sizePolicy().hasHeightForWidth())
        self.itiSpinBox.setSizePolicy(sizePolicy)
        self.itiSpinBox.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.itiSpinBox.setFont(font)
        self.itiSpinBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.itiSpinBox.setSuffix("")
        self.itiSpinBox.setMaximum(9999)
        self.itiSpinBox.setProperty("value", 15)
        self.itiSpinBox.setObjectName("itiSpinBox")
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.itiSpinBox)
        self.itiVarianceLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.itiVarianceLabel.setFont(font)
        self.itiVarianceLabel.setObjectName("itiVarianceLabel")
        self.formLayout_2.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.itiVarianceLabel)
        self.itiVarianceSpinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.itiVarianceSpinBox.sizePolicy().hasHeightForWidth())
        self.itiVarianceSpinBox.setSizePolicy(sizePolicy)
        self.itiVarianceSpinBox.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.itiVarianceSpinBox.setFont(font)
        self.itiVarianceSpinBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.itiVarianceSpinBox.setSuffix("")
        self.itiVarianceSpinBox.setMaximum(9999)
        self.itiVarianceSpinBox.setProperty("value", 3)
        self.itiVarianceSpinBox.setObjectName("itiVarianceSpinBox")
        self.formLayout_2.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.itiVarianceSpinBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.formLayout_2.setItem(12, QtWidgets.QFormLayout.LabelRole, spacerItem1)
        self.trialSettings = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.trialSettings.setFont(font)
        self.trialSettings.setObjectName("trialSettings")
        self.formLayout_2.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.trialSettings)
        self.trialDurationLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.trialDurationLabel.setFont(font)
        self.trialDurationLabel.setObjectName("trialDurationLabel")
        self.formLayout_2.setWidget(14, QtWidgets.QFormLayout.LabelRole, self.trialDurationLabel)
        self.trialDurationSpinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trialDurationSpinBox.sizePolicy().hasHeightForWidth())
        self.trialDurationSpinBox.setSizePolicy(sizePolicy)
        self.trialDurationSpinBox.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.trialDurationSpinBox.setFont(font)
        self.trialDurationSpinBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.trialDurationSpinBox.setSuffix("")
        self.trialDurationSpinBox.setMinimum(0)
        self.trialDurationSpinBox.setMaximum(10000000)
        self.trialDurationSpinBox.setSingleStep(1000)
        self.trialDurationSpinBox.setProperty("value", 3000)
        self.trialDurationSpinBox.setObjectName("trialDurationSpinBox")
        self.formLayout_2.setWidget(14, QtWidgets.QFormLayout.FieldRole, self.trialDurationSpinBox)
        self.baselineDurationLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.baselineDurationLabel.setFont(font)
        self.baselineDurationLabel.setObjectName("baselineDurationLabel")
        self.formLayout_2.setWidget(15, QtWidgets.QFormLayout.LabelRole, self.baselineDurationLabel)
        self.baselineDurationSpinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.baselineDurationSpinBox.sizePolicy().hasHeightForWidth())
        self.baselineDurationSpinBox.setSizePolicy(sizePolicy)
        self.baselineDurationSpinBox.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.baselineDurationSpinBox.setFont(font)
        self.baselineDurationSpinBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.baselineDurationSpinBox.setSuffix("")
        self.baselineDurationSpinBox.setMinimum(0)
        self.baselineDurationSpinBox.setMaximum(10000000)
        self.baselineDurationSpinBox.setSingleStep(1000)
        self.baselineDurationSpinBox.setProperty("value", 1000)
        self.baselineDurationSpinBox.setObjectName("baselineDurationSpinBox")
        self.formLayout_2.setWidget(15, QtWidgets.QFormLayout.FieldRole, self.baselineDurationSpinBox)
        spacerItem2 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.formLayout_2.setItem(16, QtWidgets.QFormLayout.LabelRole, spacerItem2)
        self.csNameLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.csNameLabel.setFont(font)
        self.csNameLabel.setObjectName("csNameLabel")
        self.formLayout_2.setWidget(17, QtWidgets.QFormLayout.LabelRole, self.csNameLabel)
        self.csNameLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.csNameLineEdit.sizePolicy().hasHeightForWidth())
        self.csNameLineEdit.setSizePolicy(sizePolicy)
        self.csNameLineEdit.setMinimumSize(QtCore.QSize(1, 0))
        self.csNameLineEdit.setMaximumSize(QtCore.QSize(132, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.csNameLineEdit.setFont(font)
        self.csNameLineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.csNameLineEdit.setText("")
        self.csNameLineEdit.setObjectName("csNameLineEdit")
        self.formLayout_2.setWidget(17, QtWidgets.QFormLayout.FieldRole, self.csNameLineEdit)
        self.csDurationLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.csDurationLabel.setFont(font)
        self.csDurationLabel.setObjectName("csDurationLabel")
        self.formLayout_2.setWidget(18, QtWidgets.QFormLayout.LabelRole, self.csDurationLabel)
        self.csDurationSpinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.csDurationSpinBox.sizePolicy().hasHeightForWidth())
        self.csDurationSpinBox.setSizePolicy(sizePolicy)
        self.csDurationSpinBox.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.csDurationSpinBox.setFont(font)
        self.csDurationSpinBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.csDurationSpinBox.setSuffix("")
        self.csDurationSpinBox.setMinimum(0)
        self.csDurationSpinBox.setMaximum(10000000)
        self.csDurationSpinBox.setSingleStep(100)
        self.csDurationSpinBox.setProperty("value", 100)
        self.csDurationSpinBox.setObjectName("csDurationSpinBox")
        self.formLayout_2.setWidget(18, QtWidgets.QFormLayout.FieldRole, self.csDurationSpinBox)
        spacerItem3 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.formLayout_2.setItem(19, QtWidgets.QFormLayout.LabelRole, spacerItem3)
        self.interstimulusIntervalLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.interstimulusIntervalLabel.setFont(font)
        self.interstimulusIntervalLabel.setObjectName("interstimulusIntervalLabel")
        self.formLayout_2.setWidget(20, QtWidgets.QFormLayout.LabelRole, self.interstimulusIntervalLabel)
        self.interstimulusIntervalSpinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.interstimulusIntervalSpinBox.sizePolicy().hasHeightForWidth())
        self.interstimulusIntervalSpinBox.setSizePolicy(sizePolicy)
        self.interstimulusIntervalSpinBox.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.interstimulusIntervalSpinBox.setFont(font)
        self.interstimulusIntervalSpinBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.interstimulusIntervalSpinBox.setSuffix("")
        self.interstimulusIntervalSpinBox.setMaximum(10000000)
        self.interstimulusIntervalSpinBox.setSingleStep(500)
        self.interstimulusIntervalSpinBox.setProperty("value", 500)
        self.interstimulusIntervalSpinBox.setObjectName("interstimulusIntervalSpinBox")
        self.formLayout_2.setWidget(20, QtWidgets.QFormLayout.FieldRole, self.interstimulusIntervalSpinBox)
        spacerItem4 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.formLayout_2.setItem(21, QtWidgets.QFormLayout.LabelRole, spacerItem4)
        self.usNameLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.usNameLabel.setFont(font)
        self.usNameLabel.setObjectName("usNameLabel")
        self.formLayout_2.setWidget(22, QtWidgets.QFormLayout.LabelRole, self.usNameLabel)
        self.usNameLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usNameLineEdit.sizePolicy().hasHeightForWidth())
        self.usNameLineEdit.setSizePolicy(sizePolicy)
        self.usNameLineEdit.setMinimumSize(QtCore.QSize(1, 0))
        self.usNameLineEdit.setMaximumSize(QtCore.QSize(132, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.usNameLineEdit.setFont(font)
        self.usNameLineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.usNameLineEdit.setText("")
        self.usNameLineEdit.setObjectName("usNameLineEdit")
        self.formLayout_2.setWidget(22, QtWidgets.QFormLayout.FieldRole, self.usNameLineEdit)
        self.usDurationLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.usDurationLabel.setFont(font)
        self.usDurationLabel.setObjectName("usDurationLabel")
        self.formLayout_2.setWidget(23, QtWidgets.QFormLayout.LabelRole, self.usDurationLabel)
        self.usDurationSpinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usDurationSpinBox.sizePolicy().hasHeightForWidth())
        self.usDurationSpinBox.setSizePolicy(sizePolicy)
        self.usDurationSpinBox.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.usDurationSpinBox.setFont(font)
        self.usDurationSpinBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.usDurationSpinBox.setSuffix("")
        self.usDurationSpinBox.setMinimum(0)
        self.usDurationSpinBox.setMaximum(10000000)
        self.usDurationSpinBox.setSingleStep(100)
        self.usDurationSpinBox.setProperty("value", 100)
        self.usDurationSpinBox.setObjectName("usDurationSpinBox")
        self.formLayout_2.setWidget(23, QtWidgets.QFormLayout.FieldRole, self.usDurationSpinBox)
        self.subjectAgeLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.subjectAgeLabel.setFont(font)
        self.subjectAgeLabel.setObjectName("subjectAgeLabel")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.subjectAgeLabel)
        self.subjectAgeSpinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subjectAgeSpinBox.sizePolicy().hasHeightForWidth())
        self.subjectAgeSpinBox.setSizePolicy(sizePolicy)
        self.subjectAgeSpinBox.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.subjectAgeSpinBox.setFont(font)
        self.subjectAgeSpinBox.setMaximum(999)
        self.subjectAgeSpinBox.setProperty("value", 30)
        self.subjectAgeSpinBox.setObjectName("subjectAgeSpinBox")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.subjectAgeSpinBox)
        self.subjectSexLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.subjectSexLabel.setFont(font)
        self.subjectSexLabel.setObjectName("subjectSexLabel")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.subjectSexLabel)
        self.subjectSexComboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subjectSexComboBox.sizePolicy().hasHeightForWidth())
        self.subjectSexComboBox.setSizePolicy(sizePolicy)
        self.subjectSexComboBox.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.subjectSexComboBox.setFont(font)
        self.subjectSexComboBox.setObjectName("subjectSexComboBox")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.subjectSexComboBox)
        spacerItem5 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.formLayout_2.setItem(6, QtWidgets.QFormLayout.LabelRole, spacerItem5)
        spacerItem6 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.formLayout_2.setItem(3, QtWidgets.QFormLayout.LabelRole, spacerItem6)
        self.sessionNameLineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sessionNameLineEdit.sizePolicy().hasHeightForWidth())
        self.sessionNameLineEdit.setSizePolicy(sizePolicy)
        self.sessionNameLineEdit.setMinimumSize(QtCore.QSize(1, 0))
        self.sessionNameLineEdit.setMaximumSize(QtCore.QSize(125, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sessionNameLineEdit.setFont(font)
        self.sessionNameLineEdit.setMaxLength(12)
        self.sessionNameLineEdit.setObjectName("sessionNameLineEdit")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.sessionNameLineEdit)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.rootHorizontalLayout.addWidget(self.scrollArea)
        self.middleVerticalLine = QtWidgets.QFrame(self.centralwidget)
        self.middleVerticalLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.middleVerticalLine.setFrameShadow(QtWidgets.QFrame.Raised)
        self.middleVerticalLine.setLineWidth(2)
        self.middleVerticalLine.setMidLineWidth(0)
        self.middleVerticalLine.setObjectName("middleVerticalLine")
        self.rootHorizontalLayout.addWidget(self.middleVerticalLine)
        self.rightSide = QtWidgets.QVBoxLayout()
        self.rightSide.setObjectName("rightSide")
        self.graphButtonLayout = QtWidgets.QHBoxLayout()
        self.graphButtonLayout.setObjectName("graphButtonLayout")
        self.lockButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lockButton.sizePolicy().hasHeightForWidth())
        self.lockButton.setSizePolicy(sizePolicy)
        self.lockButton.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lockButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/Unlocked Button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lockButton.setIcon(icon)
        self.lockButton.setIconSize(QtCore.QSize(100, 75))
        self.lockButton.setObjectName("lockButton")
        self.graphButtonLayout.addWidget(self.lockButton)
        self.playButton = QtWidgets.QPushButton(self.centralwidget)
        self.playButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playButton.sizePolicy().hasHeightForWidth())
        self.playButton.setSizePolicy(sizePolicy)
        self.playButton.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.playButton.setAutoFillBackground(False)
        self.playButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Images/Play Button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playButton.setIcon(icon1)
        self.playButton.setIconSize(QtCore.QSize(100, 75))
        self.playButton.setCheckable(False)
        self.playButton.setObjectName("playButton")
        self.graphButtonLayout.addWidget(self.playButton)
        spacerItem7 = QtWidgets.QSpacerItem(75, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.graphButtonLayout.addItem(spacerItem7)
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stopButton.sizePolicy().hasHeightForWidth())
        self.stopButton.setSizePolicy(sizePolicy)
        self.stopButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.stopButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Images/Stop Button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stopButton.setIcon(icon2)
        self.stopButton.setIconSize(QtCore.QSize(100, 75))
        self.stopButton.setObjectName("stopButton")
        self.graphButtonLayout.addWidget(self.stopButton)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.graphButtonLayout.addItem(spacerItem8)
        self.sessionInfoLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.sessionInfoLabel.setFont(font)
        self.sessionInfoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.sessionInfoLabel.setObjectName("sessionInfoLabel")
        self.graphButtonLayout.addWidget(self.sessionInfoLabel)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.graphButtonLayout.addItem(spacerItem9)
        spacerItem10 = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.graphButtonLayout.addItem(spacerItem10)
        self.rightSide.addLayout(self.graphButtonLayout)
        self.horizontalLine = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalLine.sizePolicy().hasHeightForWidth())
        self.horizontalLine.setSizePolicy(sizePolicy)
        self.horizontalLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontalLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLine.setObjectName("horizontalLine")
        self.rightSide.addWidget(self.horizontalLine)
        self.graphWidget = GraphicsLayoutWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphWidget.sizePolicy().hasHeightForWidth())
        self.graphWidget.setSizePolicy(sizePolicy)
        self.graphWidget.setObjectName("graphWidget")
        self.rightSide.addWidget(self.graphWidget)
        self.rootHorizontalLayout.addLayout(self.rightSide)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1324, 37))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.actionOpen.setFont(font)
        self.actionOpen.setObjectName("actionOpen")
        self.actionCaptureWindow = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.actionCaptureWindow.setFont(font)
        self.actionCaptureWindow.setObjectName("actionCaptureWindow")
        self.actionClose = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.actionClose.setFont(font)
        self.actionClose.setObjectName("actionClose")
        self.actionDisplaySettings = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.actionDisplaySettings.setFont(font)
        self.actionDisplaySettings.setObjectName("actionDisplaySettings")
        self.actionCaptureGraph = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.actionCaptureGraph.setFont(font)
        self.actionCaptureGraph.setObjectName("actionCaptureGraph")
        self.actionCaptureScreen = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.actionCaptureScreen.setFont(font)
        self.actionCaptureScreen.setObjectName("actionCaptureScreen")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionCaptureGraph)
        self.menuFile.addAction(self.actionCaptureWindow)
        self.menuFile.addAction(self.actionCaptureScreen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuEdit.addAction(self.actionDisplaySettings)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.sessionNameLineEdit, self.subjectAgeSpinBox)
        MainWindow.setTabOrder(self.subjectAgeSpinBox, self.subjectSexComboBox)
        MainWindow.setTabOrder(self.subjectSexComboBox, self.sampleIntervalSpinBox)
        MainWindow.setTabOrder(self.sampleIntervalSpinBox, self.trialCountSpinBox)
        MainWindow.setTabOrder(self.trialCountSpinBox, self.itiSpinBox)
        MainWindow.setTabOrder(self.itiSpinBox, self.itiVarianceSpinBox)
        MainWindow.setTabOrder(self.itiVarianceSpinBox, self.trialDurationSpinBox)
        MainWindow.setTabOrder(self.trialDurationSpinBox, self.baselineDurationSpinBox)
        MainWindow.setTabOrder(self.baselineDurationSpinBox, self.csNameLineEdit)
        MainWindow.setTabOrder(self.csNameLineEdit, self.csDurationSpinBox)
        MainWindow.setTabOrder(self.csDurationSpinBox, self.interstimulusIntervalSpinBox)
        MainWindow.setTabOrder(self.interstimulusIntervalSpinBox, self.usNameLineEdit)
        MainWindow.setTabOrder(self.usNameLineEdit, self.usDurationSpinBox)
        MainWindow.setTabOrder(self.usDurationSpinBox, self.lockButton)
        MainWindow.setTabOrder(self.lockButton, self.playButton)

        #Set up the input manager
        import InputManager as im
        im.initialSetUp(self, icon1, icon)

        #Set up the graph
        import TheGraph as tg
        tg.initialSetUp(self)

        #Set up the display settings
        import DisplaySettingsManager as dsm
        dsm.initialSetUp()
        
        #Complete set up of the main window (this file)
        self.subjectSexComboBox.addItem("MALE")
        self.subjectSexComboBox.addItem("FEMALE")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Phoenix Conditioning Stimuli Device"))
        self.sessionSettings.setText(_translate("MainWindow", "Session Settings"))
        self.sessionName.setText(_translate("MainWindow", "Session Name"))
        self.sampleIntervalLabel.setText(_translate("MainWindow", "Sample Interval (ms)"))
        self.trialCountLabel.setText(_translate("MainWindow", "Number of Trials"))
        self.itiLabel.setText(_translate("MainWindow", "Intertrial Interval (s)"))
        self.itiVarianceLabel.setText(_translate("MainWindow", "ITI Variance (s)"))
        self.itiVarianceSpinBox.setPrefix(_translate("MainWindow", "± "))
        self.trialSettings.setText(_translate("MainWindow", "Trial Settings"))
        self.trialDurationLabel.setText(_translate("MainWindow", "Trial Duration (ms)"))
        self.baselineDurationLabel.setText(_translate("MainWindow", "Baseline Duration (ms)"))
        self.csNameLabel.setText(_translate("MainWindow", "CS Name"))
        self.csNameLineEdit.setPlaceholderText(_translate("MainWindow", "Tone"))
        self.csDurationLabel.setText(_translate("MainWindow", "CS Duration (ms)"))
        self.interstimulusIntervalLabel.setText(_translate("MainWindow", "Interstimulus Interval (ms)"))
        self.usNameLabel.setText(_translate("MainWindow", "US Name"))
        self.usNameLineEdit.setPlaceholderText(_translate("MainWindow", "Air Puff"))
        self.usDurationLabel.setText(_translate("MainWindow", "US Duration (ms)"))
        self.subjectAgeLabel.setText(_translate("MainWindow", "Subject Age (yr)"))
        self.subjectSexLabel.setText(_translate("MainWindow", "Subject Sex"))
        self.sessionInfoLabel.setText(_translate("MainWindow", "DATA ACQUISITION\n""\n""TRIAL 000 / 000"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionOpen.setText(_translate("MainWindow", "Open..."))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionCaptureWindow.setText(_translate("MainWindow", "Capture Window..."))
        self.actionCaptureWindow.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionDisplaySettings.setText(_translate("MainWindow", "Display Settings..."))
        self.actionDisplaySettings.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.actionCaptureGraph.setText(_translate("MainWindow", "Capture Graph..."))
        self.actionCaptureGraph.setShortcut(_translate("MainWindow", "Ctrl+G"))
        self.actionCaptureScreen.setText(_translate("MainWindow", "Capture Screen..."))
        self.actionCaptureScreen.setShortcut(_translate("MainWindow", "Ctrl+S"))
from pyqtgraph import GraphicsLayoutWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
