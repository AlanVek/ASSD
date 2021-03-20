from PyQt5.QtWidgets import QWidget
from src.ui.GUI_General import Ui_Form
import numpy as np
from functools import partial
from src.Canvas import Canvas, Qt
from scipy.signal import square
from scipy.fft import fft, fftfreq

class GUI(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


        #Variabes
        self.y = np.array([])
        self.x = np.array([])
        self.checkBox = [self.FAABox, self.SHBox, self.AnalogKeyBox, self.FRBox]
        self.n_plots = 0


        self.FreqSignal.setValue(1)

        self.osc, self.spec = Canvas(title = 'Oscilloscope', xlabel = 'Time [s]'), Canvas('Spectral Analyzer', xlabel = 'Frequency [Hz]')

        self.connect_callback()


    def connect_callback(self):

        for i, check in enumerate(self.checkBox):
            check.toggled.connect(partial(self.toggle_box, i))

        self.PlotButton.clicked.connect(self.new_circuit)

        self.OscBox.toggled.connect(lambda: self.osc.setVisible(self.OscBox.isChecked()))
        self.SpecBox.toggled.connect(lambda: self.spec.setVisible(self.SpecBox.isChecked()))

        self.osc.closed.connect(lambda: self.OscBox.setChecked(False))
        self.spec.closed.connect(lambda: self.SpecBox.setChecked(False))

        # self.osc.cleared.connect(lambda: self.n_osc_plots -= 0)

    def toggle_box(self, position):
        if self.checkBox[position].isChecked():
            self.checkBox[position].setStyleSheet("background-color: blue; border: 1px solid black;")
        else:
            self.checkBox[position].setStyleSheet("background-color: gray;")

    def create_function(self):
        if self.SignalSelection.currentText() == 'Sine':
            realFreq = self.FreqSignal.value() / 5
            func = lambda x: self.AmpSignal.value() * np.cos(2*np.pi*x*realFreq)
            self.SignalLabel.setText('A*sin(2π*f*t/5)')
        elif self.SignalSelection.currentText() == 'Exponential':
            func = lambda x: self.AmpSignal.value() * np.exp(-np.abs(5*self.FreqSignal.value()* x))
            self.SignalLabel.setText('A*exp(-|5*f*t|)')
            realFreq = self.FreqSignal() / 2
        elif self.SignalSelection.currentText() == 'AM':
            func = lambda x: self.AmpSignal.value() * (0.5 * np.cos(3.6*np.pi*self.FreqSignal.value()*self.x)+np.cos(4*np.pi*self.FreqSignal.value()*self.x)+0.5*np.cos(4.4*np.pi*self.FreqSignal.value()*self.x))
            self.SignalLabel.setText("AM")
            realFreq = 5 / self.FreqSignal.value()

        else: return

        NPER = 6
        self.x = np.linspace(0, max(NPER/realFreq, self.x.max() if self.x.size else 0), num = 5000 * NPER)
        self.y = func(self.x)

    def new_circuit(self):

        self.create_function()
        self.n_plots += 1

        fs = self.SampleFreq.value()
        Th = 1 / fs

        timestep = (self.x.max() - self.x.min()) / (self.x.size - 1)
        freqs = fftfreq(self.x.size, d=timestep)
        self.osc.add_plot(self.x, self.y, "Input")
        self.spec.add_plot(freqs, abs(fft(self.y)), "Input")

        # FAA
        if self.checkBox[0].isChecked():
            pass
        # S&H
        if self.checkBox[1].isChecked():
            jump = max(1, int(np.round(Th / timestep, 0)))
            self.y = np.repeat(self.y[::jump], jump)[: self.y.size]
            if self.y.size < self.x.size: self.y = np.append(self.y, np.full(self.x.size - self.y.size, self.y[-1]))

            self.add_both(self.x, self.y, freqs, "Hold")

        # Llave analógica
        if self.checkBox[2].isChecked():
            self.y *= (1 + square(2 * np.pi * fs * self.x, self.DutySample.value() / 100)) / 2

            self.add_both(self.x, self.y, freqs, "Switch")

        if self.checkBox[3].isChecked():
            pass


    def add_both(self, x, y, f, label : str):
        self.osc.add_plot(x, y, label, self.n_plots)
        self.spec.add_plot(f, abs(fft(y)), label, self.n_plots)

    def keyPressEvent(self, a0) -> None:
        if a0.key() == Qt.Key_Escape: self.close()
        return super().keyPressEvent(a0)