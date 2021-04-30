from PyQt5.QtWidgets import QWidget
from GUIs.TrackInfo.TrackInfo_QT import Ui_Form


class TrackInfo(QWidget, Ui_Form):

    def __init__(self, number, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.number = number
        self.options = options

        self.Track_Label.setText('Track ' + str(self.number))

        for option in self.options:
            self.Instrument_Options.addItem(option)

    def current_option(self):
        return self.Instrument_Options.currentText()

    def delete(self):
        self.verticalLayout_2.removeWidget(self.Track_Label)
        self.verticalLayout_2.removeWidget(self.Instrument_Options)
        self.verticalLayout_2.removeWidget(self.Full_Frame)

        self.Track_Label.deleteLater()
        self.Instrument_Options.deleteLater()
        self.Full_Frame.deleteLater()
