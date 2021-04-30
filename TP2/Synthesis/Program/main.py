from PyQt5.QtWidgets import QApplication
from GUIs.GUI import GUI

if __name__ == '__main__':

	app = QApplication([])
	gui = GUI()
	gui.show()

	app.exec()


