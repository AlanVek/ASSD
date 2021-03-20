# PyQt5 modules
from PyQt5.QtWidgets import QApplication

from src.GUI_General import GUI

def main():
    app = QApplication([])

    window = GUI()

    window.show()

    app.exec()
