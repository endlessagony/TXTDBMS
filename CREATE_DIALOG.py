from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class CreateDialog(QDialog):
    accepted = pyqtSignal(str)

    def __init__(self, parent=None):
        super(CreateDialog, self).__init__(parent)
        self.columns = ''

        self.btn = QPushButton('OK')
        self.btn.setDisabled(False)
        self.btn.clicked.connect(self.ok_pressed)
        self.move(1430, 140)

        dialog = QInputDialog(parent)
        dialog.resize(50, 25)
        dialog.setWindowTitle('CREATE')
        dialog.setLabelText('ENTER QUANTITY OF ATTRIBUTES (WITHOUT PRIMARY, EX. ID):')
        dialog.setTextValue("")
        dialog.setInputMode(QInputDialog.TextInput)

        ok = dialog.exec_()
        number = dialog.textValue()

        if ok and number.__len__() != 0:
            form = QFormLayout(self)
            self.input_values = []
            for i in range(int(number)):
                line = QLineEdit()
                form.addRow('№'+str(i+1)+" ATTRIBUTE NAME", line)
                self.input_values.append(line)

            form.addRow(self.btn)
        else:
            QMessageBox(self, "PLEASE ENTER VALUES.")

    def unlock(self, text):
        if text:
            self.btn.setEnabled(True)
        else:
            self.btn.setDisabled(True)

    def ok_pressed(self):
        self.columns = (','.join([value.text() for value in self.input_values])+'\n').upper()
        self.accepted.emit(self.columns)
        self.accept()

    def get_inputs(self):
        return self.columns

