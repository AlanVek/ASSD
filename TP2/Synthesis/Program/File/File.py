from PyQt5.QtWidgets import QFileDialog, QApplication

def open_file(ext = '*', app = True) -> str:

	# Creates a PyQt5 QApplication to run the QFileDialog
	if app: _app = QApplication([])

	# Gets file path with the given extension (all files if non given)
	res = QFileDialog.getOpenFileName(filter = f'*.{ext}')[0]

	if app: _app.exit()

	return res