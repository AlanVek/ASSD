from PyQt5.QtWidgets import QWidget, QVBoxLayout
from GUIs.Player_GUI.Player import Player
from GUIs.GUI_QT import Ui_Form
from File.File import open_file
from mido import MidiFile
from GUIs.TrackInfo.TrackInfo import TrackInfo
from Instruments.Karplus_Strong.KSInstrument import Guitar, Drum, Harp
import numpy as np
from threading import Thread
from PyQt5.QtCore import Qt, QSize


class GUI(QWidget, Ui_Form):

    instrument_names = ['Guitar', 'Harp', 'Drum']
    instruments = [Guitar(), Harp(), Drum()]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.File_Button.clicked.connect(self.get_file)
        self.Synth_Button.clicked.connect(self.synthesize)
        self.Synth_Button.setEnabled(False)
        self.file = self.filename = ''
        self.track_tracker : list[TrackInfo] = []

        self.newlay = QVBoxLayout()
        self.player = Player(self.GUI_Frame)
        self.newlay.addWidget(self.player, 0, Qt.AlignHCenter)
        self.Buttons_Layout.addLayout(self.newlay)
        self.th = Thread(target = self._synth)

        self.scroller.setFixedWidth(250)

    def get_file(self):
        self.Synth_Button.setEnabled(False)
        self.filename = open_file('mid', app = False)
        if not len(self.filename): return

        self.Synth_Button.setEnabled(True)
        for i, track in enumerate(self.track_tracker):
            self.track_layout.removeWidget(track)
            track.delete()

        self.track_tracker.clear()
        self.file = MidiFile(self.filename)

        for i, track in enumerate(self.file.tracks):
            self.track_tracker.append(TrackInfo(i + 1, self.instrument_names))
            self.track_layout.addWidget(self.track_tracker[-1])

    def synthesize(self):
        if len(self.filename):
            if self.th.is_alive(): self.th.join()
            self.th = Thread(target = self._synth)
            self.th.start()

    def _synth(self):
        if len(self.filename):
            self.player.stop()
            self.player.Play_Button.setEnabled(False)

            used = []

            for i, track in enumerate(self.track_tracker):
                if track.isChecked():
                    index = self.instrument_names.index(track.current_option())
                    print(f'Synthesizing track {i+1} of {len(self.track_tracker)} with: {self.instrument_names[index]}')

                    if index in used:
                        self.instruments[index].synthesize(fs = 48000, track = i, add = True)
                    else:
                        self.instruments[index].load(self.file)
                        self.instruments[index].synthesize(fs = 48000, track = i)
                        used.append(index)

            for pos, i in enumerate(used):
                if not pos: self.sound = self.instruments[i].sound.copy()
                else:
                    if self.sound.size < self.instruments[i].sound.size:
                        self.sound = np.append(self.sound, np.zeros(self.instruments[i].sound.size - self.sound.size))

                    self.sound[ : self.instruments[i].sound.size] += self.instruments[i].sound

            self.player.load(self.sound, 48000)
            print('Synthesized')

    def keyPressEvent(self, a0) -> None:
        if a0.key() == Qt.Key_Escape: self.close()
        return super().keyPressEvent(a0)

    def close(self):
        self.player.close()
        return super().close()


