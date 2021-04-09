from src.ui.GUI_General import GUI_Base, QtGui
import numpy as np
from functools import partial
from src.Canvas import Canvas, Qt, QWidget, QCheckBox
from scipy.signal import square
from scipy.fft import fft, fftfreq, ifft

_EXPO_TEXT = 'A * exp(- |5 * f * t|) ; [-1/f, 1/f]'
_SINE_TEXT = 'A * sin(2π * f * t / 5) ; [0, 15/2f]'
_COSN_TEXT = '   A * cos(2π * f * t) ; [0, 2π]    '
_AMMD_TEXT = '                AM                  '

_COS_IDX = 0
_SIN_IDX = 1
_EXP_IDX = 2
_AMM_IDX = 3

_CANT_PER = 7000
_MAX_DIF_F = 180

class GUI(QWidget, GUI_Base):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.y = np.array([])
        self.x = np.array([])
        self.checkBox : list[QCheckBox] = [self.FAABox, self.SHBox, self.AnalogKeyBox, self.FRBox]
        self.n_plots = 0

        self.osc = Canvas(title = 'Oscilloscope', xlabel = 'Time [ms]', ylabel = 'mV')
        self.spec = Canvas('Spectral Analyzer', xlabel = 'Frequency [kHz]', ylabel = 'dBm')

        self.connect_callback()
        self.repaint()

        self.iniStyle = self.checkBox[0].styleSheet()

        self.num = np.poly1d([1.71358972e+36])
        self.denom = np.poly1d([1.00000000e+00, 2.49631794e+05, 1.31958016e+11, 2.27862963e+16, 4.96508499e+21, 5.16926822e+26, 4.69945731e+31, 1.71358972e+36])

        self.filter = lambda f: self.num(2j * np.pi * f) / self.denom(2j * np.pi * f)

    def connect_callback(self):

        for i, check in enumerate(self.checkBox):
            check.toggled.connect(partial(self.toggle_box, i))

        self.PlotButton.clicked.connect(self.new_circuit)

        self.OscBox.toggled.connect(self.osc.setVisible)
        self.SpecBox.toggled.connect(self.spec.setVisible)

        self.osc.closed.connect(self.OscBox.setChecked)
        self.spec.closed.connect(self.SpecBox.setChecked)

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
            self.checkBox[position].setStyleSheet(self.iniStyle)

    def create_function(self):

        NPER = 6

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

        self.x = np.linspace(0, NPER / realFreq, num=_CANT_PER * NPER)
        self.y = func(self.x)

    def new_circuit(self):

        self.create_function()
        self.n_plots += 1

        fs = self.SampleFreq.value() * 1e3
        Th = min(1 / fs, 1/self.FreqSignal.value() / 2e3)

        timestep = (self.x.max() - self.x.min()) / (self.x.size - 1)
        freqs = fftfreq(self.x.size, d=timestep)
        self.add_both(self.x, self.y, freqs, "Input")

        # FAA
        if self.checkBox[0].isChecked():

            y_f = self.filter(freqs) * fft(self.y)
            self.y = np.real(ifft(y_f, n = self.x.size))

            self.add_both(self.x, self.y, freqs, "FAA")

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
            y_f = self.filter(freqs) * fft(self.y)
            self.y = np.real(ifft(y_f, n=self.x.size))

            self.add_both(self.x, self.y, freqs, "FR")

    def add_both(self, x, y, f, label : str):
        self.osc.add_plot(x * 1e3, y * 1e3, label, self.n_plots)
        pos_f = (f >= 0) & (f <= 10e3 * max(self.FreqSignal.value(), self.SampleFreq.value()))

        self.spec.add_plot(f[pos_f] / 1e3, self.to_dBm(fft(y)[pos_f]), label, ID = self.n_plots)

    def keyPressEvent(self, a0) -> None:
        if a0.key() == Qt.Key_Escape: self.close()
        return super().keyPressEvent(a0)

    def new_expo(self, NPER):
        fi = self.FreqSignal.value() * 1e3
        x_temp = np.linspace(-1/fi, 1/fi, num = _CANT_PER)

        y_temp = self.AmpSignal.value() / 1e3 * np.exp(-np.abs(5 * fi * x_temp))

        return fi/2, np.concatenate((y_temp[x_temp >= 0], np.tile(y_temp, NPER - 1), y_temp[x_temp < 0]))

    def new_sine(self, NPER):
        fi = self.FreqSignal.value() * 1e3
        x_temp = np.linspace(0, 15 / (2 * fi), num = _CANT_PER)

        y_temp = self.AmpSignal.value() / 1e3 * np.sin(2 * np.pi * x_temp * fi / 5)

        return 2 * fi / 15, np.tile(y_temp, NPER)

    def newText(self):
        if self.SignalSelection.currentIndex() == _SIN_IDX: self.SignalLabel.setText(_SINE_TEXT)

        elif self.SignalSelection.currentIndex() == _EXP_IDX: self.SignalLabel.setText(_EXPO_TEXT)

        elif self.SignalSelection.currentIndex() == _AMM_IDX: self.SignalLabel.setText(_AMMD_TEXT)

        elif self.SignalSelection.currentIndex() == _COS_IDX: self.SignalLabel.setText(_COSN_TEXT)

    def close(self):
        self.osc.close()
        self.spec.close()
        return QWidget.close(self)

    def clearPlots(self):
        self.osc.clear()
        self.spec.clear()
        self.n_plots = 0

    def adjust_freqs(self, which):
        if self.SampleFreq.value() > self.FreqSignal.value() * 250:
            if which == 1: self.SampleFreq.setValue(self.FreqSignal.value() * _MAX_DIF_F)

            else:
                self.FreqSignal.setValue(np.ceil(self.SampleFreq.value() / _MAX_DIF_F * 100) / 100)

    def adjust_duty(self):
        if self.DutySample.value() > 95: self.DutySample.setValue(95)

    @staticmethod
    def to_dBm(FFT):

        MIN_NOISE = 1e-5
        R_IN = 50

        dBm = lambda v: 10 * np.log10(v**2 / R_IN)

        FFT = np.abs(FFT)
        greater_than_noise = FFT >= MIN_NOISE
        FFT[greater_than_noise] = dBm(FFT[greater_than_noise])
        FFT[~greater_than_noise] = dBm(MIN_NOISE)
        return FFT

    def paintEvent(self, a0) -> None:
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 3))


        absPos = lambda check: check.pos() + check.parent().pos() + self.SignalPathFrame.pos() + self.GeneralSelectionFrame.pos() + self.FatherFrame.pos()

        wCheck = self.checkBox[0].width()
        hCheck = self.checkBox[0].height()
        wArr = hArr = hCheck / 2
        for i, check in enumerate(self.checkBox):
            if i != len(self.checkBox) - 1:
                posi = absPos(check)
                xi = posi.x() + 3 * wCheck
                yi = posi.y() + hCheck / 2
                xf = absPos(self.checkBox[i + 1]).x() - 2 * wCheck

                painter.drawLine(xi, yi, xf, yi)
                painter.drawLine(xf - wArr, yi - hArr, xf, yi)
                painter.drawLine(xf - wArr, yi + hArr, xf, yi)

        painter.end()
