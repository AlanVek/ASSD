from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5.QtCore import Qt

from functools import partial

from PyQt5.QtWidgets import QWidget, QCheckBox
from src.ui.Osc_Freq import Ui_Form


class Osc_Freq(QWidget, Ui_Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.figure = Figure()
        self.Fcanvas = FigureCanvas(self.figure)
        self.Canvas.addWidget(NavigationToolbar(self.Fcanvas, self))
        self.Canvas.addWidget(self.Fcanvas)
        self.ax = self.figure.add_subplot(111)
        self.figure.tight_layout()
        self.Fcanvas.draw()

        self.plots = []
        self.checks : list[QCheckBox] = []


    def add_plot(self, x, y, label = ''):
        self.plots.append(self.ax.plot(x, y, label = label)[0])
        self.ax.legend()
        self.checks.append(QCheckBox())
        self.Toggles.addWidget(self.checks[-1])
        self.checks[-1].setText(f'Plot {len(self.checks)}')
        self.checks[-1].setChecked(True)
        self.checks[-1].toggled.connect(partial(self.toggle_plot, len(self.checks) - 1))
        self.Fcanvas.draw()

    def toggle_plot(self, number):
        self.plots[number].set_visible(self.checks[number].isChecked())
        self.Fcanvas.draw()

    def keyPressEvent(self, a0) -> None:
        if a0.key() == Qt.Key_Escape: self.close()
        else: return super().keyPressEvent(a0)
