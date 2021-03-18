# PyQt5 modules
from PyQt5.QtWidgets import QApplication
from src.Osc_Freq import Osc_Freq

import numpy as np

def main():
    app = QApplication([])
    window = Osc_Freq()
    window.show()

    x = np.linspace(-5, 5, 1000)
    y = np.cos(x)

    window.add_plot(x, y + 2)
    window.add_plot(x, y + 4)
    window.add_plot(x, y + 6)
    window.add_plot(x, y + 8)
    app.exec()
