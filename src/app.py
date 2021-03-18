# PyQt5 modules
from PyQt5.QtWidgets import QApplication
from src.Osc_Freq import Osc_Freq

def main():
    app = QApplication([])
    window = Osc_Freq()
    window.show()
    app.exec()
