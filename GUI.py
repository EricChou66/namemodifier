#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import  QApplication,\
    QDesktopWidget, QMessageBox, QMainWindow, QFileDialog, QErrorMessage
from PyQt5.uic import loadUi
from fileio import folder_exist
from fileio import change_files_in_folder


class Main(QMainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        loadUi('./UI/mainwindow.ui', self)
        self.title = "Name Modifier UI"
        self.initUI()
        error_dialog = QErrorMessage()
        error_dialog.showMessage('Oh no!')

    def initUI(self):
        # Set Window Title
        self.setWindowTitle(self.title)

        # Quit Button
        self.quitBtn.clicked.connect(self.close)

        # Select Folder Button
        self.folderBtn.clicked.connect(self.select_folder)

        # Select Output Folder Button
        self.outputBtn.clicked.connect(self.select_output_folder)

        # Clear Button
        self.clearBtn.clicked.connect(self.clear)

        # Skip Duplicate file CheckBox
        self.skipdupBox.stateChanged.connect(lambda: self.checkbox_state(self.skipdupBox))

        # Output file in the origin path
        self.samefoldBox.stateChanged.connect(lambda: self.checkbox_state(self.samefoldBox))

        # Remove original files CheckBox
        self.removeBox.stateChanged.connect(lambda: self.checkbox_state(self.removeBox))

        # Original filename input check:
        self.originalfnStr.textChanged.connect(self.ok_btn_validate)

        # Reset to default status
        self.clear()

        # Ok Button
        self.okBtn.clicked.connect(self.change_files_name)

        # Text change for Files Folder, New filename, and Output Folder
        self.folderStr.textChanged.connect(self.ok_btn_validate)
        self.newfilenameStr.textChanged.connect(self.ok_btn_validate)
        self.outputStr.textChanged.connect(self.ok_btn_validate)

    def select_folder(self):
        folder_dir = QFileDialog.getExistingDirectory(
            self, "Open a folder", "./")
        self.folderStr.setText(folder_dir)

    def select_output_folder(self):
        output_dir = QFileDialog.getExistingDirectory(
            self, "Open a folder", "./")
        self.outputStr.setText(output_dir)

    def clear(self):
        self.folderStr.setText('')
        self.extStr.setText('')
        self.newfilenameStr.setText('')
        self.outputStr.setText('')
        self.originalfnStr.setText('')
        self.samefoldBox.setChecked(False)
        self.skipdupBox.setChecked(False)
        self.removeBox.setChecked(False)
        self.remove = False
        self.skipdup = False
        self.outsamefolder = False
        self.hintLabel.setText('')
        self.okBtn.setEnabled(False)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def checkbox_state(self, box):
        if box.text() == 'Output in Same Folder':
            if box.isChecked():
                self.outsamefolder = True
                self.outputBtn.setEnabled(False)
            else:
                self.outsamefolder = False
                self.outputBtn.setEnabled(True)
            self.ok_btn_validate()

        elif box.text() == 'Skip Duplicate files':
            if box.isChecked():
                self.skipdup = True
            else:
                self.skipdup = False
        elif box.text() == 'Remove Original files':
            if box.isChecked():
                self.remove = True
            else:
                self.remove = False

    def change_files_name(self):
        original_filename = self.originalfnStr.text()
        new_filename = self.newfilenameStr.text()
        original_folder = self.folderStr.text()
        file_ext = self.extStr.text()
        new_folder = self.outputStr.text()
        change_files_in_folder(original_folder, original_filename,
                               new_folder, new_filename, self.remove,
                               self.outsamefolder, self.skipdup, file_ext)
    def ok_btn_validate(self):
        original_filename = self.originalfnStr.text()
        # new_filename = self.newfilenameStr.text()
        original_folder = self.folderStr.text()
        file_ext = self.extStr.text()
        new_folder = self.outputStr.text()
        hint_str = ""

        if not folder_exist(original_folder):
            hint_str += "Files Folder can't no found"
        # File extension must be not null
        if(file_ext == ""):
            hint_str += "\nFile extension must be specified"
        elif(' ' in file_ext):
            hint_str += "\nFile extension must be seperate with ',' not space"
        # Output in same folder
        if (not self.outsamefolder) and (not folder_exist(new_folder)):
            hint_str += "\nOutput Folder can't no found"
        if (original_filename != "") and (not ("{" in original_filename) or not ("}" in original_filename)):
            hint_str += "\nNew Filename format invalid, must includes '{}' to wrap the number"
        # if new_filename == "":
        #     hint_str += "\nNew Filename is empty"
        if(hint_str == ""):
            self.okBtn.setEnabled(True)
        else:
            self.okBtn.setEnabled(False)
        self.hintLabel.setText(hint_str)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    m = Main()
    m.show()
    sys.exit(app.exec_())
