from PyQt5.QtWidgets import QWidget
from GUIs.TrackInfo.TrackInfo_QT import Ui_Form


class TrackInfo(QWidget, Ui_Form):

    def __init__(self, number, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.number = number
        self.options = options

        self.Track_Label.setText('Track ' + str(self.number))
        self.Instrument_Options.addItems(self.options)

    def current_option(self):
        return self.Instrument_Options.currentText()

    def delete(self):
        self.hiddenLayout.removeWidget(self.Track_Label)
        self.hiddenLayout.removeWidget(self.Instrument_Options)
        self.hiddenLayout.removeWidget(self.Full_Frame)

        self.Track_Label.deleteLater()
        self.Instrument_Options.deleteLater()
        self.Full_Frame.deleteLater()

    def isChecked(self): return self.Track_Label.isChecked()
