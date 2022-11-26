import PyQt5.QtGui
import sys
import pandas as pd
import os
import numpy as np
import shutil
import qdarkstyle
from HELPFUL_FUNCTIONS import *
from ADD_EDIT_DIALOG import *
from CREATE_DIALOG import *
import time

DMBS = QApplication(sys.argv)


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.w_width = 1000
        self.w_height = 800
        self.main_root = r'C:\Users\nikita\PycharmProjects\DB_LAB1'
        self.db_name = ''
        self.file_path = ''
        self.backup_dir = os.path.join(self.main_root, 'backups')
        self.backup_file = ''
        self.temp_dir = os.path.join(self.main_root, 'temp')
        self.databases = [f.replace('.txt', '').lower() for f in os.listdir(self.main_root) if f.endswith('.txt')]
        self.save_dir = os.path.join(self.main_root, 'saves')

        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.init_ui()

        self.table = QTableWidget(self)
        self.headers = []
        self.edges = []
        self.num_lines = 0
        self.primary_key = ''

    def init_ui(self):
        # window appearance
        self.resize(self.w_width, self.w_height)
        self.center()
        self.setWindowTitle('ERDMBS')
        self.setWindowIcon(PyQt5.QtGui.QIcon('hse.png'))

        # buttons
        # done
        find_btn = QPushButton('FIND', self)
        find_btn.move(self.w_width - 100, 20)
        find_btn.clicked.connect(self.find_el)
        find_btn.resize(80, 20)
        find_btn.setFont(PyQt5.QtGui.QFont('Comic Sans', 10, PyQt5.QtGui.QFont.Bold))

        # done
        add_btn = QPushButton('ADD', self)
        add_btn.move(self.w_width - 100, 50)
        add_btn.clicked.connect(self.add_el)
        add_btn.resize(80, 20)
        add_btn.setFont(PyQt5.QtGui.QFont('Comic Sans', 10, PyQt5.QtGui.QFont.Bold))

        # done
        drop_btn = QPushButton('DROP', self)
        drop_btn.move(self.w_width - 100, 80)
        drop_btn.resize(80, 20)
        drop_btn.clicked.connect(self.drop_el)
        drop_btn.setFont(PyQt5.QtGui.QFont('Comic Sans', 10, PyQt5.QtGui.QFont.Bold))

        # done
        edit_btn = QPushButton("EDIT", self)
        edit_btn.move(self.w_width - 100, 110)
        edit_btn.resize(80, 20)
        edit_btn.clicked.connect(self.edit_db)
        edit_btn.setFont(PyQt5.QtGui.QFont('Comic Sans', 10, PyQt5.QtGui.QFont.Bold))

        # done
        delete_btn = QPushButton('DELETE', self)
        delete_btn.move(self.w_width - 100, 230)
        delete_btn.clicked.connect(self.delete_db)
        delete_btn.resize(80, 20)
        delete_btn.setFont(PyQt5.QtGui.QFont('Comic Sans', 10, PyQt5.QtGui.QFont.Bold))

        # done
        create_btn = QPushButton('CREATE', self)
        create_btn.move(self.w_width - 100, 260)
        create_btn.clicked.connect(self.create_db)
        create_btn.resize(80, 20)
        create_btn.setFont(PyQt5.QtGui.QFont('Comic Sans', 10, PyQt5.QtGui.QFont.Bold))

        # done
        open_btn = QPushButton('OPEN', self)
        open_btn.move(self.w_width - 100, 290)
        open_btn.clicked.connect(self.open_db)
        open_btn.resize(80, 20)
        open_btn.setFont(PyQt5.QtGui.QFont('Comic Sans', 10, PyQt5.QtGui.QFont.Bold))

        # done
        recover_btn = QPushButton('RECOVER', self)
        recover_btn.move(self.w_width - 100, 320)
        recover_btn.clicked.connect(self.recover_db)
        recover_btn.resize(80, 20)
        recover_btn.setFont(PyQt5.QtGui.QFont("Helvetica", 10, PyQt5.QtGui.QFont.Bold))

        # done
        q_btn = QPushButton('QUIT', self)
        q_btn.clicked.connect(self.quit)
        q_btn.move(self.w_width - 100, 350)
        q_btn.resize(80, 20)
        q_btn.setFont(PyQt5.QtGui.QFont('Times', 10, PyQt5.QtGui.QFont.Bold))

        save_btn = QPushButton('SAVE', self)
        save_btn.clicked.connect(self.save_to_csv)
        save_btn.move(self.w_width - 100, 380)
        save_btn.resize(80, 20)
        save_btn.setFont(PyQt5.QtGui.QFont("Helvetica", 10, PyQt5.QtGui.QFont.Bold))

        # shortcuts

        find_label = QLabel(self)
        find_label.setText('FIND: Ctrl+F')
        find_label.move(self.w_width - 125, 470)
        find_label.setFont(PyQt5.QtGui.QFont('Times', 10, PyQt5.QtGui.QFont.Bold))
        find_shortcut = QShortcut(PyQt5.QtGui.QKeySequence("Ctrl+F"), self)
        find_shortcut.activated.connect(self.find_el)

        open_label = QLabel(self)
        open_label.setText('OPEN: Ctrl+O')
        open_label.move(self.w_width - 125, 500)
        open_label.setFont(PyQt5.QtGui.QFont('Times', 10, PyQt5.QtGui.QFont.Bold))
        open_shortcut = QShortcut(PyQt5.QtGui.QKeySequence("Ctrl+O"), self)
        open_shortcut.activated.connect(self.open_db)

        add_label = QLabel(self)
        add_label.setText('ADD: Ctrl+A')
        add_label.move(self.w_width - 125, 530)
        add_label.setFont(PyQt5.QtGui.QFont('Times', 10, PyQt5.QtGui.QFont.Bold))
        add_shortcut = QShortcut(PyQt5.QtGui.QKeySequence("Ctrl+A"), self)
        add_shortcut.activated.connect(self.add_el)

        create_label = QLabel(self)
        create_label.setText('CREATE: Ctrl+C')
        create_label.move(self.w_width - 125, 560)
        create_label.setFont(PyQt5.QtGui.QFont('Times', 10, PyQt5.QtGui.QFont.Bold))
        create_shortcut = QShortcut(PyQt5.QtGui.QKeySequence("Ctrl+C"), self)
        create_shortcut.activated.connect(self.create_db)

        edit_label = QLabel(self)
        edit_label.setText('EDIT: Ctrl+E')
        edit_label.move(self.w_width - 125, 590)
        edit_label.setFont(PyQt5.QtGui.QFont('Times', 10, PyQt5.QtGui.QFont.Bold))
        edit_shortcut = QShortcut(PyQt5.QtGui.QKeySequence("Ctrl+E"), self)
        edit_shortcut.activated.connect(self.edit_db)

        drop_label = QLabel(self)
        drop_label.setText('DROP: Ctrl+D')
        drop_label.move(self.w_width - 125, 620)
        drop_label.setFont(PyQt5.QtGui.QFont('Times', 10, PyQt5.QtGui.QFont.Bold))
        drop_shortcut = QShortcut(PyQt5.QtGui.QKeySequence("Ctrl+D"), self)
        drop_shortcut.activated.connect(self.drop_el)

        self.show()

    def save_to_csv(self):
        start = time.time()

        if self.file_path != '':
            if not os.path.isdir(self.save_dir):
                os.mkdir(self.save_dir)
            else:
                data = pd.read_csv(self.file_path, sep=',')
                data.to_csv(os.path.join(self.save_dir, self.db_name+'.csv'), index=False)
                QMessageBox.about(self, "SUCCESS", "Database WAS SUCCESSFULLY SAVED TO .CSV.")

        else:
            QMessageBox.about(self, "ERROR", "Database WAS NOT OPENED.")
        end = time.time()
        print(f'SAVE ELAPSED TIME: {round(end-start, 2)} seconds')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_db(self):
        text, ok = QInputDialog.getText(self, 'CREATE', 'ENTER DataBase NAME:')
        if ok and len(text) != 0:
            start = time.time()

            self.db_name = text
            self.file_path = os.path.join(self.main_root, self.db_name + '.txt')
            if os.path.exists(self.file_path):
                QMessageBox.about(self, "ERROR", "FILE IS ALREADY EXISTS.")
            else:
                f = open(self.file_path, 'w')
                f.close()
                dialog = CreateDialog(self)
                if dialog.exec_():
                    columns_names = dialog.get_inputs()
                    with open(self.file_path, 'w') as file:
                        file.write(columns_names)
                self.databases = [f.replace('.txt', '').lower() for f in os.listdir(self.main_root) if f.endswith('.txt')]
            end = time.time()
            print(f'CREATE ELAPSED TIME: {round(end-start, 2)} seconds')
        else:
            QMessageBox.about(self, "ERROR", "EMPTY FIELDS DETECTED.")

    def delete_db(self):
        if self.file_path == '':
            QMessageBox.about(self, "ERROR", "Database WAS NOT OPENED.")
        else:
            reply = QMessageBox.question(self, 'DELETING DataBase',
                                         'DO YOU WANT TO DELETE DataBase?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                if os.path.exists(self.file_path):
                    os.remove(self.file_path)
                else:
                    QMessageBox.about(self, "ERROR", "FILE WAS NOT FOUND.")
                self.quit()

    def open_db(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle('OPEN')
        dialog.setLabelText('Enter DataBase name:'.upper())
        dialog.setTextValue("")
        le = dialog.findChild(QLineEdit)
        completer = QCompleter(self.databases, le)
        le.setCompleter(completer)

        ok, text = (
            dialog.exec_() == QDialog.Accepted,
            dialog.textValue(),
        )
        if ok and len(text) != 0:
            start = time.time()

            self.db_name = text
            self.file_path = os.path.join(self.main_root, self.db_name + '.txt')
            if os.path.exists(self.file_path):
                self.table = QTableWidget(self)
                self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                data = pd.read_csv(self.file_path, sep=',')
                self.edges = get_ends_of_lines(self.file_path)
                if "Unnamed: 0" in data.columns.tolist():
                    data.drop(["Unnamed: 0"], axis='columns', inplace=True)
                    data.to_csv(self.file_path, index=False)
                else:
                    pass
                if 'id' not in [l.lower() for l in data.columns.tolist()]:
                    temp_data = pd.read_csv(self.file_path, sep=',')
                    temp_data.insert(loc=0, column='ID', value=np.arange(0, temp_data.shape[0]))
                    new = [l.upper() for l in temp_data.columns.tolist()]
                    temp_data.columns = new
                    temp_data.to_csv(self.file_path, index=False)
                else:
                    temp_data = pd.read_csv(self.file_path, sep=',')
                    new = [l.upper() for l in temp_data.columns.tolist()]
                    temp_data.columns = new
                    temp_data.to_csv(self.file_path, index=False)

                data = pd.read_csv(self.file_path)
                with open(self.file_path, 'r') as file:
                    self.headers = file.readline().splitlines()[0].split(',')
                    self.primary_key = self.headers[0]
                    self.num_lines = sum(1 for line in file)

                self.create_temporary_files()
                headers = data.columns.values.tolist()
                self.table.setColumnCount(len(headers))
                self.table.setHorizontalHeaderLabels(headers)

                for i, row in data.iterrows():
                    self.table.setRowCount(self.table.rowCount() + 1)

                    for j in range(self.table.columnCount()):
                        self.table.setItem(i, j, QTableWidgetItem(str(row[j])))

                self.table.resize(self.w_width - 150, self.w_height - 150)

                self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                self.table.horizontalHeader().setFont(PyQt5.QtGui.QFont('Times', 15, PyQt5.QtGui.QFont.Bold))
                end = time.time()
                print(f'OPEN ELAPSED TIME: {round(end-start, 2)} seconds')

                if os.path.exists(os.path.join(self.backup_dir, self.db_name+'_backup.txt')) is False:
                    self.backup_db()

                self.table.show()
            else:
                QMessageBox.about(self, "ERROR", "FILE WAS NOT FOUND.")

    def recover_db(self):
        if self.file_path == '':
            QMessageBox.about(self, "ERROR", "Database WAS NOT OPENED.")
        else:
            start = time.time()
            shutil.copyfile(os.path.join(self.backup_dir, self.db_name+'_backup.txt'), self.file_path)
            self.table = QTableWidget(self)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.edges = get_ends_of_lines(self.file_path)
            data = pd.read_csv(self.file_path)

            self.create_temporary_files()
            headers = data.columns.values.tolist()
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)

            for i, row in data.iterrows():
                self.table.setRowCount(self.table.rowCount() + 1)

                for j in range(self.table.columnCount()):
                    self.table.setItem(i, j, QTableWidgetItem(str(row[j])))

            self.table.resize(self.w_width - 150, self.w_height - 150)

            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.table.horizontalHeader().setFont(PyQt5.QtGui.QFont('Times', 15, PyQt5.QtGui.QFont.Bold))

            self.table.show()
            end = time.time()
            print(f'RECOVER ELAPSED TIME: {round(end-start, 2)} seconds')
            QMessageBox.about(self, "RECOVER", "Database WAS SUCCESSFULLY RECOVERED.")

    def edit_db(self):
        if self.file_path == '':
            QMessageBox.about(self, "ERROR", "Database WAS NOT OPENED.")
        else:
            dialog = QInputDialog(self)
            dialog.setWindowTitle('EDIT')
            dialog.setLabelText('ENTER ID VALUE:')
            dialog.setTextValue("")
            dictionary = initialize_dictionary_from_txt(os.path.join(self.temp_dir,
                                                                     self.db_name +
                                                                     f'_{self.primary_key}_HASHED.txt'))
            le = dialog.findChild(QLineEdit)
            completer = QCompleter(dictionary.keys(), le)
            le.setCompleter(completer)

            check, _id = (
                dialog.exec_() == QDialog.Accepted,
                dialog.textValue(),
            )
            if check:
                with open(os.path.join(self.temp_dir, self.db_name + f'_{self.primary_key}_HASHED.txt'), 'r') as file:
                    dictionary = initialize_dictionary_from_txt(os.path.join(self.temp_dir,
                                                                             self.db_name +
                                                                             f'_{self.primary_key}_HASHED.txt'))
                    raw_locations = dictionary.get(_id)
                    self.table.setSelectionMode(QAbstractItemView.MultiSelection)
                    self.table.selectRow(int(raw_locations) - 1)
                    self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
                    previous = get_line(self.file_path, int(raw_locations) - 1).split(',')
                    dg = AddDialog(self, previous_values=previous)
                    if dg.exec_():
                        values = dg.get_inputs()
                        written_line = ','.join(values.values()) + '\n'
                        if self._check_id(values['ID']) or values['ID'] == previous[0]:
                            start = time.time()
                            copy_file = open(os.path.join(self.main_root, self.db_name + '_copy.txt'), 'w')
                            copy_file.close()
                            shutil.copyfile(self.file_path, os.path.join(self.main_root, self.db_name + '_copy.txt'))
                            with open(os.path.join(self.main_root, self.db_name + '_copy.txt'), 'r') as copy_file:
                                with open(self.file_path, 'w') as file:
                                    copy_lines = copy_file.readlines()
                                    file_lines = copy_lines
                                    dictionary = initialize_dictionary_from_txt(os.path.join(self.temp_dir,
                                                                                             self.db_name +
                                                                                             f'_{self.primary_key}'
                                                                                             f'_HASHED.txt'))
                                    raw_location = int(dictionary.get(previous[0]))
                                    file_lines[raw_location] = written_line
                                    file.writelines(file_lines)
                            for column_index, cell_value in enumerate(values.values()):
                                item = QTableWidgetItem(cell_value)
                                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable |
                                              Qt.ItemIsEnabled)
                                self.table.setItem(raw_location-1, column_index, item)
                            os.remove(os.path.join(self.main_root, self.db_name + '_copy.txt'))
                            end = time.time()
                            print(f'EDIT ELAPSED TIME: {round(end-start, 2)} seconds')
                            self.update_files()
            else:
                QMessageBox.about(self, "ERROR", "THERE IS NO ELEMENT WITH GIVEN ID.")

    def drop_el(self):
        if self.file_path == '':
            QMessageBox.about(self, "ERROR", "Database WAS NOT OPENED.")
        else:
            dialog = QInputDialog(self)
            dialog.setWindowTitle('DROP')
            dialog.setLabelText('ENTER ID VALUE:')
            dialog.setTextValue("")
            dictionary = initialize_dictionary_from_txt(os.path.join(self.temp_dir,
                                                                     self.db_name +
                                                                     f'_{self.primary_key}_HASHED.txt'))

            le = dialog.findChild(QLineEdit)
            completer = QCompleter(dictionary.keys(), le)
            le.setCompleter(completer)

            check, _id = (
                dialog.exec_() == QDialog.Accepted,
                dialog.textValue(),
            )
            if check and _id is not None:
                start = time.time()
                with open(os.path.join(self.temp_dir, self.db_name + f'_{self.primary_key}_HASHED.txt'), 'r') as file:
                    dictionary = initialize_dictionary_from_txt(os.path.join(self.temp_dir,
                                                                             self.db_name +
                                                                             f'_{self.primary_key}_HASHED.txt'))
                    raw_locations = int(dictionary.get(_id))
                    previous = get_line(self.file_path, raw_locations - 1).split(',')
                    copy_file = open(os.path.join(self.main_root, self.db_name + '_copy.txt'), 'w')
                    copy_file.close()
                    shutil.copyfile(self.file_path, os.path.join(self.main_root, self.db_name + '_copy.txt'))
                    with open(os.path.join(self.main_root, self.db_name + '_copy.txt'), 'r') as copy_file:
                        with open(self.file_path, 'w') as file:
                            backup_lines = copy_file.readlines()
                            dictionary = initialize_dictionary_from_txt(os.path.join(self.temp_dir,
                                                                                     self.db_name +
                                                                                     f'_{self.primary_key}'
                                                                                     f'_HASHED.txt'))
                            raw_location = int(dictionary.get(previous[0]))
                            file_lines = backup_lines
                            del file_lines[raw_location]
                            file.writelines(file_lines)
                os.remove(os.path.join(self.main_root, self.db_name + '_copy.txt'))
                self.table.removeRow(raw_location-1)
                end = time.time()
                print(f'DROP ELAPSED TIME: {round(end-start, 2)} seconds')
                self.update_files()
            else:
                QMessageBox.about(self, "ERROR", "THERE IS NO ELEMENT WITH GIVEN ID.")


    def backup_db(self):
        start = time.time()
        if not os.path.isdir(self.backup_dir):
            os.mkdir(self.backup_dir)
        else:
            pass
        self.backup_file = os.path.join(self.backup_dir, self.db_name + '_backup' + '.txt')
        if os.path.exists(self.backup_file):
            os.remove(self.backup_file)
        with open(self.backup_file, 'x') as f:
            f.write('Create a new text file!')
        shutil.copyfile(self.file_path, self.backup_file)
        end = time.time()
        print(f'BACKUP ELAPSED TIME: {round(end-start, 2)} seconds')
        QMessageBox.about(self, "BACKUP", "FILE WAS SUCCESSFULLY BACKUPED.")

    def find_el(self):
        if self.file_path == '':
            QMessageBox.about(self, "ERROR", "Database WAS NOT OPENED.")
        else:
            self.table.clearSelection()
            items = [s.strip() for s in self.headers]
            attribute, ok = QInputDialog.getItem(self, "CHOOSE ATTRIBUTE", "ATTRIBUTES:", items, 0, False)
            if ok:
                dialog = QInputDialog(self)
                dialog.setWindowTitle('FIND')
                dialog.setLabelText('ENTER ATTRIBUTE VALUE:')
                dialog.setTextValue("")
                dictionary = initialize_dictionary_from_txt(os.path.join(self.temp_dir,
                                                                         self.db_name +
                                                                         f'_{attribute}_HASHED.txt'))

                le = dialog.findChild(QLineEdit)
                completer = QCompleter(dictionary.keys(), le)
                le.setCompleter(completer)

                check, attribute_value = (
                    dialog.exec_() == QDialog.Accepted,
                    dialog.textValue(),
                )
                if check and attribute_value in dictionary.keys():
                    start = time.time()
                    with open(os.path.join(self.temp_dir, self.db_name + f'_{attribute}_HASHED.txt'), 'r') as file:
                        raw_locations = dictionary.get(attribute_value)
                        if raw_locations is None:
                            QMessageBox.about(self, "ERROR", f"NO ELEMENTS WITH {attribute} = {attribute_value}.")
                            return
                        self.table.setSelectionMode(QAbstractItemView.MultiSelection)
                        if ':' in raw_locations:
                            locations = [int(location) for location in raw_locations.split(':')]
                            for location in locations:
                                self.table.selectRow(location - 1)
                        else:
                            self.table.selectRow(int(raw_locations) - 1)
                        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
                    end = time.time()
                    print(f'FIND ELAPSED TIME: {round(end-start, 2)} seconds')
                else:
                    QMessageBox.about(self, "ERROR", "THERE IS NO ELEMENT WITH GIVEN ATTRIBUTE VALUE.")

    def update_files(self):
        self.create_temporary_files()

    def closeEvent(self, event):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        event.accept()  # let the window close

    def quit(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        QApplication.quit()

    def add_el(self):
        if self.file_path == '':
            QMessageBox.about(self, "ERROR", "Database WAS NOT OPENED.")
        else:
            dg = AddDialog(self)
            if dg.exec_():
                start = time.time()
                added_values = dg.get_inputs()
                written_line = ','.join(added_values.values())
                if self._check_id(added_values['ID']):
                    with open(self.file_path, 'a') as file:
                        file.write(written_line + '\n')
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)
                    for column_index, value in enumerate(added_values.values()):
                        self.table.setItem(row_position, column_index, QTableWidgetItem(value))
                    QMessageBox.about(self, "SUCCESS", "ELEMENT WAS ADDED TO DataBase.")
                    self.update_files()
                    end = time.time()
                    print(f'ADD ELAPSED TIME: {round(end-start, 2)} seconds')

    def create_temporary_files(self):
        if os.path.exists(self.temp_dir):
            pass
        else:
            os.mkdir(self.temp_dir)
        for index, header in enumerate(self.headers):
            file = open(os.path.join(self.temp_dir, self.db_name + f'_{header}_HASHED.txt'), 'w')
            file.close()
            with open(os.path.join(self.temp_dir, self.db_name + f'_{header}_HASHED.txt'), 'a') as \
                    temporary_file:
                temporary_file.write(f'LOCATIONS,{header}_VALUE\n')
                dict_locations = hash_helper(self.file_path, header)
                for key, value in dict_locations.items():
                    temporary_file.write(f"{value},{key}\n")

    def _check_id(self, new_id) -> int:
        if not new_id.isdigit():
            QMessageBox.about(self, "ERROR", "ID MUST BE DECIMAL.")
        else:
            with open(os.path.join(self.temp_dir, self.db_name + f'_{self.primary_key}_HASHED.txt'), 'r') as file:
                dictionary = initialize_dictionary_from_txt(os.path.join(self.temp_dir,
                                                                         self.db_name +
                                                                         f'_{self.primary_key}'
                                                                         f'_HASHED.txt'))
                if dictionary.get(new_id) is None:
                    return True
                else:
                    QMessageBox.about(self, "ERROR", "ELEMENT WITH GIVEN ID IS ALREADY EXISTS.")
                    return False


GUI = MainWindow()
sys.exit(DMBS.exec_())
