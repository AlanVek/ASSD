# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\GUI_General.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1193, 906)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.FatherFrame = QtWidgets.QFrame(Form)
        self.FatherFrame.setObjectName("FatherFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.FatherFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.InputFrame = QtWidgets.QGroupBox(self.FatherFrame)
        # self.InputFrame.setStyleSheet('border: 1px solid black;')
        self.InputFrame.setTitle('INPUT')
        # self.InputFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.InputFrame.setLineWidth(2)
        self.InputFrame.setObjectName("InputFrame")
        self.InputLayout = QtWidgets.QVBoxLayout(self.InputFrame)
        self.InputLayout.setObjectName("InputLayout")
        self.SignalSelectFrame = QtWidgets.QFrame(self.InputFrame)
        self.SignalSelectFrame.setObjectName("SignalSelectFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.SignalSelectFrame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.SignalSelection = QtWidgets.QComboBox(self.SignalSelectFrame)
        self.SignalSelection.setObjectName("SignalSelection")
        self.SignalSelection.addItem("")
        self.SignalSelection.addItem("")
        self.SignalSelection.addItem("")
        self.verticalLayout_3.addWidget(self.SignalSelection)
        self.SignalLabel = QtWidgets.QLabel(self.SignalSelectFrame)
        self.SignalLabel.setObjectName("SignalLabel")
        self.verticalLayout_3.addWidget(self.SignalLabel)
        self.InputLayout.addWidget(self.SignalSelectFrame, 0, QtCore.Qt.AlignHCenter)
        self.ParameterSignalFrame = QtWidgets.QFrame(self.InputFrame)
        self.ParameterSignalFrame.setObjectName("ParameterSignalFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.ParameterSignalFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.AmplitudFrame = QtWidgets.QFrame(self.ParameterSignalFrame)
        self.AmplitudFrame.setObjectName("AmplitudFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.AmplitudFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.AmpLabel = QtWidgets.QLabel(self.AmplitudFrame)
        self.AmpLabel.setObjectName("AmpLabel")
        self.horizontalLayout.addWidget(self.AmpLabel, 0, QtCore.Qt.AlignRight)
        self.AmpSignal = QtWidgets.QDoubleSpinBox(self.AmplitudFrame)
        self.AmpSignal.setObjectName("AmpSignal")
        self.horizontalLayout.addWidget(self.AmpSignal)
        self.AmpUnit = QtWidgets.QLabel(self.AmplitudFrame)
        self.AmpUnit.setObjectName("AmpUnit")
        self.horizontalLayout.addWidget(self.AmpUnit, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_4.addWidget(self.AmplitudFrame)
        self.FreqFrame = QtWidgets.QFrame(self.ParameterSignalFrame)
        self.FreqFrame.setObjectName("FreqFrame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.FreqFrame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.FreqLabel = QtWidgets.QLabel(self.FreqFrame)
        self.FreqLabel.setObjectName("FreqLabel")
        self.horizontalLayout_3.addWidget(self.FreqLabel, 0, QtCore.Qt.AlignRight)
        self.FreqSignal = QtWidgets.QDoubleSpinBox(self.FreqFrame)
        self.FreqSignal.setObjectName("FreqSignal")
        self.horizontalLayout_3.addWidget(self.FreqSignal)
        self.FreqUnit = QtWidgets.QLabel(self.FreqFrame)
        self.FreqUnit.setObjectName("FreqUnit")
        self.horizontalLayout_3.addWidget(self.FreqUnit, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_4.addWidget(self.FreqFrame)
        self.InputLayout.addWidget(self.ParameterSignalFrame, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.InputFrame)
        # self.SampleFrame = QtWidgets.QFrame(self.FatherFrame)
        self.SampleFrame = QtWidgets.QGroupBox(self.FatherFrame)
        self.SampleFrame.setTitle('SAMPLING')
        # self.SampleFrame.setStyleSheet('border: 1px solid black;')
        # self.SampleFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.SampleFrame.setLineWidth(2)
        self.SampleFrame.setObjectName("SampleFrame")
        self.SampleLayout = QtWidgets.QVBoxLayout(self.SampleFrame)
        self.SampleLayout.setObjectName("SampleLayout")
        self.DutyFrame = QtWidgets.QFrame(self.SampleFrame)
        self.DutyFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.DutyFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.DutyFrame.setObjectName("DutyFrame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.DutyFrame)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.DutyLabel = QtWidgets.QLabel(self.DutyFrame)
        self.DutyLabel.setObjectName("DutyLabel")
        self.horizontalLayout_4.addWidget(self.DutyLabel)
        self.DutySample = QtWidgets.QDoubleSpinBox(self.DutyFrame)
        self.DutySample.setObjectName("DutySample")
        self.horizontalLayout_4.addWidget(self.DutySample)
        self.DutyUnit = QtWidgets.QLabel(self.DutyFrame)
        self.DutyUnit.setObjectName("DutyUnit")
        self.horizontalLayout_4.addWidget(self.DutyUnit)
        self.SampleLayout.addWidget(self.DutyFrame, 0, QtCore.Qt.AlignHCenter)
        self.FreqSampleFrame = QtWidgets.QFrame(self.SampleFrame)
        self.FreqSampleFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.FreqSampleFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.FreqSampleFrame.setObjectName("FreqSampleFrame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.FreqSampleFrame)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.SampFreqLabel = QtWidgets.QLabel(self.FreqSampleFrame)
        self.SampFreqLabel.setObjectName("SampFreqLabel")
        self.horizontalLayout_5.addWidget(self.SampFreqLabel)
        self.SampleFreq = QtWidgets.QDoubleSpinBox(self.FreqSampleFrame)
        self.SampleFreq.setObjectName("SampleFreq")
        self.horizontalLayout_5.addWidget(self.SampleFreq)
        self.SampFreqUnit = QtWidgets.QLabel(self.FreqSampleFrame)
        self.SampFreqUnit.setObjectName("SampFreqUnit")
        self.horizontalLayout_5.addWidget(self.SampFreqUnit)
        self.SampleLayout.addWidget(self.FreqSampleFrame, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.SampleFrame)
        self.GeneralSelectionFrame = QtWidgets.QGroupBox(self.FatherFrame)
        # self.GeneralSelectionFrame.setStyleSheet('border: 1px solid black;')
        self.GeneralSelectionFrame.setTitle('PARAMETERS')
        # self.GeneralSelectionFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.GeneralSelectionFrame.setLineWidth(2)
        self.GeneralSelectionFrame.setObjectName("GeneralSelectionFrame")
        self.GeneralSelectionLayout = QtWidgets.QVBoxLayout(self.GeneralSelectionFrame)
        self.GeneralSelectionLayout.setObjectName("GeneralSelectionLayout")
        self.PlotFrame = QtWidgets.QFrame(self.GeneralSelectionFrame)
        self.PlotFrame.setObjectName("PlotFrame")
        self.PlotLayout = QtWidgets.QHBoxLayout(self.PlotFrame)
        self.PlotLayout.setSpacing(50)
        self.PlotLayout.setObjectName("PlotLayout")
        self.OscBox = QtWidgets.QCheckBox(self.PlotFrame)
        self.OscBox.setObjectName("OscBox")
        self.PlotLayout.addWidget(self.OscBox)
        self.SpecBox = QtWidgets.QCheckBox(self.PlotFrame)
        self.SpecBox.setObjectName("SpecBox")
        self.PlotLayout.addWidget(self.SpecBox)
        self.PlotButton = QtWidgets.QPushButton(self.PlotFrame)
        self.PlotButton.setObjectName("PlotButton")
        self.PlotLayout.addWidget(self.PlotButton)
        self.GeneralSelectionLayout.addWidget(self.PlotFrame, 0, QtCore.Qt.AlignHCenter)
        self.SignalPathFrame = QtWidgets.QFrame(self.GeneralSelectionFrame)
        self.SignalPathFrame.setObjectName("SignalPathFrame")
        self.SignalPathLayout = QtWidgets.QHBoxLayout(self.SignalPathFrame)
        self.SignalPathLayout.setObjectName("SignalPathLayout")
        self.FAAFrame = QtWidgets.QFrame(self.SignalPathFrame)
        self.FAAFrame.setObjectName("FAAFrame")
        self.FAALayout = QtWidgets.QVBoxLayout(self.FAAFrame)
        self.FAALayout.setSpacing(15)
        self.FAALayout.setObjectName("FAALayout")
        self.FAALabel = QtWidgets.QLabel(self.FAAFrame)
        self.FAALabel.setObjectName("FAALabel")
        self.FAALayout.addWidget(self.FAALabel)
        self.FAABox = QtWidgets.QCheckBox(self.FAAFrame)
        self.FAABox.setText("")
        self.FAABox.setObjectName("FAABox")
        self.FAALayout.addWidget(self.FAABox, 0, QtCore.Qt.AlignHCenter)
        self.SignalPathLayout.addWidget(self.FAAFrame, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.SHFrame = QtWidgets.QFrame(self.SignalPathFrame)
        self.SHFrame.setObjectName("SHFrame")
        self.SHLayout = QtWidgets.QVBoxLayout(self.SHFrame)
        self.SHLayout.setSpacing(15)
        self.SHLayout.setObjectName("SHLayout")
        self.SHLabel = QtWidgets.QLabel(self.SHFrame)
        self.SHLabel.setObjectName("SHLabel")
        self.SHLayout.addWidget(self.SHLabel)
        self.SHBox = QtWidgets.QCheckBox(self.SHFrame)
        self.SHBox.setText("")
        self.SHBox.setObjectName("SHBox")
        self.SHLayout.addWidget(self.SHBox, 0, QtCore.Qt.AlignHCenter)
        self.SignalPathLayout.addWidget(self.SHFrame, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.AnalogKeyFrame = QtWidgets.QFrame(self.SignalPathFrame)
        self.AnalogKeyFrame.setObjectName("AnalogKeyFrame")
        self.AnalogKeyLayout = QtWidgets.QVBoxLayout(self.AnalogKeyFrame)
        self.AnalogKeyLayout.setSpacing(15)
        self.AnalogKeyLayout.setObjectName("AnalogKeyLayout")
        self.AnalogKayLabel = QtWidgets.QLabel(self.AnalogKeyFrame)
        self.AnalogKayLabel.setObjectName("AnalogKayLabel")
        self.AnalogKeyLayout.addWidget(self.AnalogKayLabel)
        self.AnalogKeyBox = QtWidgets.QCheckBox(self.AnalogKeyFrame)
        self.AnalogKeyBox.setText("")
        self.AnalogKeyBox.setObjectName("AnalogKeyBox")
        self.AnalogKeyLayout.addWidget(self.AnalogKeyBox, 0, QtCore.Qt.AlignHCenter)
        self.SignalPathLayout.addWidget(self.AnalogKeyFrame, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.FRFrame = QtWidgets.QFrame(self.SignalPathFrame)
        self.FRFrame.setObjectName("FRFrame")
        self.FRLayout = QtWidgets.QVBoxLayout(self.FRFrame)
        self.FRLayout.setSpacing(15)
        self.FRLayout.setObjectName("FRLayout")
        self.FRLabel = QtWidgets.QLabel(self.FRFrame)
        self.FRLabel.setObjectName("FRLabel")
        self.FRLayout.addWidget(self.FRLabel)
        self.FRBox = QtWidgets.QCheckBox(self.FRFrame)
        self.FRBox.setText("")
        self.FRBox.setObjectName("FRBox")
        self.FRLayout.addWidget(self.FRBox, 0, QtCore.Qt.AlignHCenter)
        self.SignalPathLayout.addWidget(self.FRFrame, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.GeneralSelectionLayout.addWidget(self.SignalPathFrame)
        self.verticalLayout.addWidget(self.GeneralSelectionFrame)
        self.verticalLayout_2.addWidget(self.FatherFrame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.SignalSelection.setItemText(0, _translate("Form", "Sine"))
        self.SignalSelection.setItemText(1, _translate("Form", "Exponential"))
        self.SignalSelection.setItemText(2, _translate("Form", "AM"))
        self.SignalLabel.setText(_translate("Form", "A*sin(2π*f*t/5)"))
        self.AmpLabel.setText(_translate("Form", "Amplitud  "))
        self.AmpUnit.setText(_translate("Form", "V"))
        self.FreqLabel.setText(_translate("Form", "Frequency"))
        self.FreqUnit.setText(_translate("Form", "Hz"))
        self.DutyLabel.setText(_translate("Form", "Duty cycle"))
        self.DutyUnit.setText(_translate("Form", "%"))
        self.SampFreqLabel.setText(_translate("Form", "Frequency"))
        self.SampFreqUnit.setText(_translate("Form", "Hz"))
        self.OscBox.setText(_translate("Form", "Osciloscope"))
        self.SpecBox.setText(_translate("Form", "Spectrum"))
        self.PlotButton.setText(_translate("Form", "Plot"))
        self.FAALabel.setText(_translate("Form", "FAA"))
        self.SHLabel.setText(_translate("Form", "S&H"))
        self.AnalogKayLabel.setText(_translate("Form", "Switch"))
        self.FRLabel.setText(_translate("Form", "Restore Filter"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
