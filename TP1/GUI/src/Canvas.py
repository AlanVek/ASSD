from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.lines import Line2D

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QCheckBox

from src.ui.Canvas import Ui_Form

class Canvas(QWidget, Ui_Form):

    closed = pyqtSignal(bool)

    def __init__(self, title = '', xlabel = '', ylabel = '', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.setMinimumSize(500, 500)

        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.figure = Figure(tight_layout=True)
        self.Fcanvas = FigureCanvas(self.figure)
        self.Canvas.addWidget(NavigationToolbar(self.Fcanvas, self), alignment = Qt.AlignHCenter)
        self.Canvas.addWidget(self.Fcanvas)
        self.ax = self.figure.add_subplot(111)
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

        self.new_ax()

        self.Fcanvas.draw()

        self.Clear.clicked.connect(self.clear)
        self.LogCheck.toggled.connect(self.new_scale)

        self.plots : list[Line2D] = []
        self.checks : list[QCheckBox] = []

    def add_plot(self, x, y, label = ' ', ID = None, scale = None):
        txt = label + (f' {ID}' if ID else '')
        self.plots.append(self.ax.plot(x, y, label = txt)[0])
        self.ax.legend()

        if scale: self.ax.set_xscale(scale)

        self.checks.append(QCheckBox(txt))
        self.Toggles.addWidget(self.checks[-1], alignment = Qt.AlignHCenter)
        self.checks[-1].setChecked(True)
        # self.checks[-1].toggled.connect(partial(self.toggle_plot, len(self.checks) - 1))
        self.checks[-1].toggled.connect(self.plots[-1].set_visible)
        self.checks[-1].toggled.connect(self.Fcanvas.draw)

        self.Fcanvas.draw()
        self.checks[-1].setStyleSheet(f'color: {self.plots[-1].get_color()}; font-weight: bold')

    # def toggle_plot(self, number):
    #     self.plots[number].set_visible(self.checks[number].isChecked())
        # self.plots[number].set_visible(self.checks[number].isChecked())
        # self.Fcanvas.draw()

    def keyPressEvent(self, a0) -> None:
        if a0.key() == Qt.Key_Escape: self.close()
        else: return super().keyPressEvent(a0)

    def closeEvent(self, a0) -> None:
        self.closed.emit(False)
        return super().closeEvent(a0)

    def clear(self):
        self.new_ax()
        self.plots.clear()
        for check in self.checks: self.Toggles.removeWidget(check)
        self.checks.clear()
        self.Fcanvas.draw()

    def new_ax(self):
        self.ax.clear()
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.grid()
        self.new_scale()

    def new_scale(self):
        if self.LogCheck.isChecked():
            self.ax.set_xscale('log')
        else:
            self.ax.set_xscale('linear')

        self.Fcanvas.draw()