# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TrackInfo.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.hiddenLayout = QtWidgets.QVBoxLayout(Form)
        self.hiddenLayout.setObjectName("hiddenLayout")
        self.Full_Frame = QtWidgets.QFrame(Form)
        self.Full_Frame.setObjectName("Full_Frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.Full_Frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Track_Label = QtWidgets.QCheckBox(self.Full_Frame)
        self.Track_Label.setObjectName("Track_Label")
        self.verticalLayout.addWidget(self.Track_Label, 0, QtCore.Qt.AlignHCenter)
        self.Instrument_Options = QtWidgets.QComboBox(self.Full_Frame)
        self.Instrument_Options.setObjectName("Instrument_Options")
        self.verticalLayout.addWidget(self.Instrument_Options)
        self.hiddenLayout.addWidget(self.Full_Frame, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Track_Label.setText(_translate("Form", "CheckBox"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())