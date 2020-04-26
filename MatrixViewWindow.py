# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\colli\source\repos\CsCrMachineCode\MatrixViewUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1069, 763)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.masterVerticalLayout = QtWidgets.QVBoxLayout()
        self.masterVerticalLayout.setObjectName("masterVerticalLayout")
        self.generalButtonsLayout = QtWidgets.QHBoxLayout()
        self.generalButtonsLayout.setObjectName("generalButtonsLayout")
        self.saveButton = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.saveButton.setFont(font)
        self.saveButton.setObjectName("saveButton")
        self.generalButtonsLayout.addWidget(self.saveButton)
        self.regenerateButton = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.regenerateButton.setFont(font)
        self.regenerateButton.setObjectName("regenerateButton")
        self.generalButtonsLayout.addWidget(self.regenerateButton)
        self.sessionNameLabel = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sessionNameLabel.setFont(font)
        self.sessionNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.sessionNameLabel.setObjectName("sessionNameLabel")
        self.generalButtonsLayout.addWidget(self.sessionNameLabel)
        self.closeButton = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.closeButton.setFont(font)
        self.closeButton.setObjectName("closeButton")
        self.generalButtonsLayout.addWidget(self.closeButton)
        self.masterVerticalLayout.addLayout(self.generalButtonsLayout)
        self.generalButtonsLine = QtWidgets.QFrame(Dialog)
        self.generalButtonsLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.generalButtonsLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.generalButtonsLine.setObjectName("generalButtonsLine")
        self.masterVerticalLayout.addWidget(self.generalButtonsLine)
        self.trialGridLayout = QtWidgets.QGridLayout()
        self.trialGridLayout.setObjectName("trialGridLayout")
        self.masterVerticalLayout.addLayout(self.trialGridLayout)
        self.pageButtonsLine = QtWidgets.QFrame(Dialog)
        self.pageButtonsLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.pageButtonsLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.pageButtonsLine.setObjectName("pageButtonsLine")
        self.masterVerticalLayout.addWidget(self.pageButtonsLine)
        self.horizontalButtonLayout = QtWidgets.QHBoxLayout()
        self.horizontalButtonLayout.setObjectName("horizontalButtonLayout")
        self.previousButton = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.previousButton.setFont(font)
        self.previousButton.setObjectName("previousButton")
        self.horizontalButtonLayout.addWidget(self.previousButton)
        self.pageNumberLabel = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pageNumberLabel.setFont(font)
        self.pageNumberLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.pageNumberLabel.setObjectName("pageNumberLabel")
        self.horizontalButtonLayout.addWidget(self.pageNumberLabel)
        self.nextButton = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.nextButton.setFont(font)
        self.nextButton.setObjectName("nextButton")
        self.horizontalButtonLayout.addWidget(self.nextButton)
        self.masterVerticalLayout.addLayout(self.horizontalButtonLayout)
        self.verticalLayout_2.addLayout(self.masterVerticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.saveButton.setText(_translate("Dialog", "Save As Image"))
        self.regenerateButton.setText(_translate("Dialog", "Change Parameters"))
        self.sessionNameLabel.setText(_translate("Dialog", "Sample Session Name"))
        self.closeButton.setText(_translate("Dialog", "Close"))
        self.previousButton.setText(_translate("Dialog", "Previous Page"))
        self.pageNumberLabel.setText(_translate("Dialog", "Page 1 / 1"))
        self.nextButton.setText(_translate("Dialog", "Next Page"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
