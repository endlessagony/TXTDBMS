from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class AddDialog(QDialog):
    accepted = pyqtSignal(dict)

    def __init__(self, parent=None, previous_values=None):
        super(AddDialog, self).__init__(parent)
        if previous_values is None:
            self.setWindowTitle('ADD ELEMENT')
        else:
            self.setWindowTitle('EDIT ELEMENT')
        self.values = {}
        self.move(1430, 140)

        self.btn = QPushButton('OK')
        self.btn.setDisabled(False)
        self.btn.clicked.connect(self.ok_pressed)

        self.attributes = parent.__dict__['headers']

        form = QFormLayout(self)
        self.input_values = []
        if previous_values is None:
            for i, attr in enumerate(self.attributes):
                lineEdit = QLineEdit()
                form.addRow(attr, lineEdit)
                self.input_values.append(lineEdit)
        else:
            for value, attr in zip(previous_values, self.attributes):
                value = value.replace('\n', '')
                lineEdit = QLineEdit(value, parent)
                form.addRow(attr, lineEdit)
                self.input_values.append(lineEdit)

        form.addRow(self.btn)

    def unlock(self, text):
        if text:
            self.btn.setEnabled(True)
        else:
            self.btn.setDisabled(True)

    def ok_pressed(self):
        for i, attr in enumerate(self.attributes):
            if self.input_values[i].text() == '':
                self.values[attr] = 'null'
            else:
                self.values[attr] = self.input_values[i].text()
        self.accepted.emit(self.values)
        self.accept()

    def get_inputs(self):
        return self.values