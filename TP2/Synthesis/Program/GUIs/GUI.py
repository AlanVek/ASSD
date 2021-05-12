from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QSpinBox, QHBoxLayout, QLabel
from GUIs.Player_GUI.Player import Player
from GUIs.GUI_QT import Ui_Form
from File.File import open_file
from mido import MidiFile
from GUIs.TrackInfo.TrackInfo import TrackInfo
from Instruments.Karplus_Strong.KSInstrument import Guitar, Drum, Harp
import numpy as np
from threading import Thread
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from Instruments.Sample_Based.Sample_Based_Synth import SampleBasedGuitar, SampleBasedPiano, SampleBasedBanjo, SampleBasedSaxophone, SampleBasedBassoon
from scipy.io import wavfile
from Instruments.Additive_Synthesis.ADSR_Generator import Piano2

class GUI(QWidget, Ui_Form):

    instrument_names = [
        'Guitar',
        'Harp',
        'Drum',
        'Acoustic Guitar',
        'Piano',
        'Banjo',
        'Saxophone',
        'Bassoon',
        'Piano2',
    ]

    instruments = [
        Guitar(),
        Harp(),
        Drum(),
        SampleBasedGuitar(),
        Piano2(),
        SampleBasedBanjo(),
        SampleBasedSaxophone(),
        SampleBasedBassoon(),
        SampleBasedPiano(),
    ]

    new_synth = pyqtSignal('int')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.File_Button.clicked.connect(self.get_file)
        self.Synth_Button.clicked.connect(self.synthesize)
        self.Synth_Button.setEnabled(False)
        self.file = self.filename = ''
        self.track_tracker : list[TrackInfo] = []

        self.newlay = QVBoxLayout()
        self.tonelay = QHBoxLayout()

        self.player = Player(self.GUI_Frame)
        self.newlay.addWidget(self.player, 0, Qt.AlignHCenter)

        self.progress = QProgressBar(self.GUI_Frame)
        self.lowtone = QSpinBox(self.GUI_Frame)
        self.toneLabel = QLabel(self.GUI_Frame)
        self.toneLabel.setText('Low tone: ')

        self.progress.setValue(0)
        self.lowtone.setMinimum(-2)
        self.lowtone.setMaximum(2)
        self.lowtone.setValue(0)

        self.newlay.addWidget(self.progress)
        self.tonelay.addWidget(self.toneLabel)
        self.tonelay.addWidget(self.lowtone)

        self.newlay.addLayout(self.tonelay)

        self.Buttons_Layout.addLayout(self.newlay)
        self.th = Thread(target = self._synth)

        self.scroller.setFixedWidth(250)
        self.sound = np.array([])
        self.stop = False

        self.new_synth.connect(self.progress.setValue)

    def get_file(self):
        self.Synth_Button.setEnabled(False)
        self.filename = open_file('mid', app = False)
        if not len(self.filename): return

        self.Synth_Button.setEnabled(True)
        self.progress.setValue(0)
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

            self.player.stop()
            self.player.Play_Button.setEnabled(False)
            self.Synth_Button.setEnabled(False)
            self.File_Button.setEnabled(False)

            self.th = Thread(target = self._synth)
            self.th.start()

    def _synth(self):

        used, tot, curr = [], 0, 0
        for track in self.track_tracker:
            if track.isChecked(): tot += 1
        self.new_synth.emit(0)

        if tot:
            for i, track in enumerate(self.track_tracker):
                if track.isChecked():
                    index = self.instrument_names.index(track.current_option())
                    print(f'Synthesizing track {curr + 1} of {tot} with: {self.instrument_names[index]}')

                    if index in used:
                        self.instruments[index].synthesize(fs = 48000, track = i, add = True, lowtone = self.lowtone.value())
                    else:
                        self.instruments[index].load(self.file)
                        self.instruments[index].synthesize(fs = 48000, track = i, lowtone = self.lowtone.value())
                        used.append(index)
                    curr += 1
                    self.new_synth.emit(int(curr / tot * 100))

                    if self.stop:
                        self.stop = False
                        break

            for pos, i in enumerate(used):
                if not pos: self.sound = self.sound[ : self.instruments[i].sound.size]

                if self.sound.size < self.instruments[i].sound.size:
                    self.sound = np.append(self.sound, np.zeros(self.instruments[i].sound.size - self.sound.size))

                if pos: self.sound[ : self.instruments[i].sound.size] += self.instruments[i].sound
                else: self.sound[ : self.instruments[i].sound.size] = self.instruments[i].sound

            self.player.load(self.sound, 48000)
            print('Synthesized')

            wavfile.write('Test.wav', 48000, (self.sound / np.abs(self.sound).max() * (2**16 - 1)).astype(np.int16))

            self.Synth_Button.setEnabled(True)
            self.File_Button.setEnabled(True)

    def keyPressEvent(self, a0) -> None:
        if a0.key() == Qt.Key_Escape: self.close()
        return super().keyPressEvent(a0)

    def close(self):
        self.player.close()
        self.stop = True
        if self.th.is_alive(): self.th.join()
        return super().close()


