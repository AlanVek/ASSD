from src.ui.GUI_General import GUI_Base
import numpy as np
from functools import partial
from src.Canvas import Canvas, Qt, QWidget
from scipy.signal import square
from scipy.fft import fft, fftfreq

_EXPO_TEXT = 'A * exp(- |5 * f * t|) ; [-1/f, 1/f]'
_SINE_TEXT = 'A * sin(2π * f * t / 5) ; [0, 15/2f]'
_COSN_TEXT = '   A * cos(2π * f * t) ; [0, 2π]    '

_COS_IDX = 0
_SIN_IDX = 1
_EXP_IDX = 2
_AMM_IDX = 3

class GUI(QWidget, GUI_Base):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


        #Variabes
        self.y = np.array([])
        self.x = np.array([])
        self.checkBox = [self.FAABox, self.SHBox, self.AnalogKeyBox, self.FRBox]
        self.n_plots = 0

        self.osc = Canvas(title = 'Oscilloscope', xlabel = 'Time [ms]', ylabel = 'mV')
        self.spec = Canvas('Spectral Analyzer', xlabel = 'Frequency [kHz]')

        self.connect_callback()


    def connect_callback(self):

        for i, check in enumerate(self.checkBox):
            check.toggled.connect(partial(self.toggle_box, i))

        self.PlotButton.clicked.connect(self.new_circuit)

        self.OscBox.toggled.connect(lambda: self.osc.setVisible(self.OscBox.isChecked()))
        self.SpecBox.toggled.connect(lambda: self.spec.setVisible(self.SpecBox.isChecked()))

        self.osc.closed.connect(lambda: self.OscBox.setChecked(False))
        self.spec.closed.connect(lambda: self.SpecBox.setChecked(False))

        self.SignalSelection.currentIndexChanged.connect(self.newText)
        self.Exit.clicked.connect(self.close)
        self.ClearButton.clicked.connect(self.clearPlots)

        self.SampleFreq.valueChanged.connect(partial(self.adjust_freqs, 0))
        self.FreqSignal.valueChanged.connect(partial(self.adjust_freqs, 1))

        self.DutySample.valueChanged.connect(self.adjust_duty)

    def toggle_box(self, position):
        if self.checkBox[position].isChecked():
            self.checkBox[position].setStyleSheet("background-color: blue; border: 1px solid black;")
        else:
            self.checkBox[position].setStyleSheet("background-color: gray;")

    def create_function(self):

        NPER = 6
        print(self.SignalSelection.currentIndex())

        if self.SignalSelection.currentIndex() == _COS_IDX:
            realFreq = self.FreqSignal.value() * 1000
            func = lambda x : self.AmpSignal.value() / 1e3 * np.cos(2 * np.pi * x * realFreq)

        elif self.SignalSelection.currentIndex() == _SIN_IDX:
            realFreq, self.y = self.new_sine(NPER)
            func = lambda x: self.y

        elif self.SignalSelection.currentIndex() == _EXP_IDX:
            realFreq, self.y = self.new_expo(NPER)
            func = lambda x: self.y

        elif self.SignalSelection.currentIndex() == _AMM_IDX:
            f = self.FreqSignal.value() * 1000
            func = lambda x: self.AmpSignal.value() / 1e3 * (0.5 * np.cos(3.6*np.pi*f*x)+np.cos(4*np.pi*f*x)+0.5*np.cos(4.4*np.pi*f*x))
            realFreq = f / 5

        else: return

        self.x = np.linspace(0, NPER / realFreq, num=5000 * NPER)
        self.y = func(self.x)

    def new_circuit(self):

        self.create_function()
        self.n_plots += 1

        fs = self.SampleFreq.value() * 1e3
        Th = 1 / fs

        timestep = (self.x.max() - self.x.min()) / (self.x.size - 1)
        freqs = fftfreq(self.x.size, d=timestep)
        self.add_both(self.x, self.y, freqs, "Input")

        # FAA
        if self.checkBox[0].isChecked():
            pass

        # S&H
        if self.checkBox[1].isChecked():
            jump = max(1, int(np.round(Th / timestep, 0)))
            self.y = np.repeat(self.y[::jump], jump)[: self.y.size]
            if self.y.size < self.x.size:
                self.y = np.append(self.y, np.full(self.x.size - self.y.size, self.y[-1]))

            self.add_both(self.x, self.y, freqs, "Hold")

        # Llave analógica
        if self.checkBox[2].isChecked():
            self.y *= (1 + square(2 * np.pi * fs * self.x, self.DutySample.value() / 100)) / 2

            self.add_both(self.x, self.y, freqs, "Switch")

        if self.checkBox[3].isChecked():
            pass

    def add_both(self, x, y, f, label : str):
        self.osc.add_plot(x * 1e3, y * 1e3, label, self.n_plots)
        pos_f = (f >= 0) & (f <= 10e3 * max(self.FreqSignal.value(), self.SampleFreq.value()))
        self.spec.add_plot(f[pos_f] / 1e3, np.abs(fft(y))[pos_f], label, ID = self.n_plots)

    def keyPressEvent(self, a0) -> None:
        if a0.key() == Qt.Key_Escape: self.close()
        return super().keyPressEvent(a0)

    def new_expo(self, NPER):
        fi = self.FreqSignal.value() * 1e3
        x_temp = np.linspace(-1/fi, 1/fi, num = 5000)

        y_temp = self.AmpSignal.value() / 1e3 * np.exp(-np.abs(5 * fi * x_temp))

        return fi/2, np.concatenate((y_temp[x_temp >= 0], np.tile(y_temp, NPER - 1), y_temp[x_temp < 0]))

    def new_sine(self, NPER):
        fi = self.FreqSignal.value() * 1e3
        x_temp = np.linspace(0, 15 / (2 * fi), num = 5000)

        y_temp = self.AmpSignal.value() / 1e3 * np.cos(2 * np.pi * x_temp * fi / 5)

        return 2 * fi / 15, np.tile(y_temp, NPER)

    def newText(self):
        if self.SignalSelection.currentIndex() == _SIN_IDX: self.SignalLabel.setText(_SINE_TEXT)

        elif self.SignalSelection.currentIndex() == _EXP_IDX: self.SignalLabel.setText(_EXPO_TEXT)

        elif self.SignalSelection.currentIndex() == _AMM_IDX: self.SignalLabel.setText('AM')

        elif self.SignalSelection.currentIndex() == _COS_IDX: self.SignalLabel.setText(_COSN_TEXT)

    def close(self):
        self.osc.close()
        self.spec.close()
        return QWidget.close(self)

    def clearPlots(self):
        self.osc.clear()
        self.spec.clear()

    def adjust_freqs(self, which):
        if self.SampleFreq.value() > self.FreqSignal.value() * 250:
            if which == 1: self.SampleFreq.setValue(self.FreqSignal.value() * 250)

            else:
                self.FreqSignal.setValue(np.ceil(self.SampleFreq.value() / 2.5) / 100)

    def adjust_duty(self):
        if self.DutySample.value() > 95: self.DutySample.setValue(95)