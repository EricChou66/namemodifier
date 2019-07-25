#!/usr/bin/python3

import sys
import re
from PyQt5.QtWidgets import  QApplication,\
    QDesktopWidget, QMessageBox, QMainWindow, QFileDialog, QErrorMessage
from PyQt5.uic import loadUi
from fileio import folder_exist
from fileio import change_files_in_folder
from hintstring import *


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
        self.extStr.textChanged.connect(self.ok_btn_validate)
        self.newfilenameStr.textChanged.connect(self.ok_btn_validate)
        self.originalfnStr.textChanged.connect(self.ok_btn_validate)
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
        self.clearallhint()
        self.okBtn.setEnabled(False)
        self.instruLabel.setText('')
        self.okBtnEnable = False

    def clearallhint(self):
        self.folderhintLabel.setText('')
        self.exthintLabel.setText('')
        self.newnamehintLabel.setText('')
        self.originalhintLabel.setText('')
        self.outputhintLabel.setText('')

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
                self.outputStr.setEnabled(False)
                self.outputhintLabel.setText('')
            else:
                self.outsamefolder = False
                self.outputBtn.setEnabled(True)
                self.outputStr.setEnabled(True)
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

    # Hint label for input folder
    def input_folder_validate(self):
        original_folder = self.folderStr.text()
        if original_folder == "":
            self.folderhintLabel.setText(folder_hint["Null"])
            self.okBtnEnable = self.okBtnEnable and False
        elif not folder_exist(original_folder):
            self.folderhintLabel.setText(folder_hint["Not Found"])
            self.okBtnEnable = self.okBtnEnable and False
        else:
            self.folderhintLabel.setText('')
            self.okBtnEnable = self.okBtnEnable and True

    # Hint label for file extension
    def file_ext_validate(self):
        file_ext = self.extStr.text()
        # Must be none null
        if file_ext == "":
            self.exthintLabel.setText(ext_hint["Null"])
            self.okBtnEnable = self.okBtnEnable and False
        # Use ',' seperate multiple file extension
        elif " " in file_ext:
            self.exthintLabel.setText(ext_hint["Multiple"])
            self.okBtnEnable = self.okBtnEnable and False
        else:
            self.exthintLabel.setText('')
            self.okBtnEnable = self.okBtnEnable and True

    # Hint label for new filename
    def new_filename_validate(self):
        new_filename = self.newfilenameStr.text()
        pattern = re.compile(r'\{.*\}')
        if (new_filename != ""):
            # The number would be append to new filename if there is no '{}'
            if (new_filename.count("{") == 0) \
                and (new_filename.count("}") == 0):
                self.newnamehintLabel.setText('')
                self.okBtnEnable = self.okBtnEnable and True
            # If there is '{}', '{' should before '}' and only has one
            # occurence
            elif (new_filename.count("{") == 1) \
                and (new_filename.count("}") == 1) \
                and (pattern.search(new_filename)):
                self.newnamehintLabel.setText('')
                self.okBtnEnable = self.okBtnEnable and True
            else:
                self.newnamehintLabel.setText(newname_hint["Format"])
                self.okBtnEnable = self.okBtnEnable and False

    # Hint label for original fileanme
    def original_filename_validate(self):
        original_filename = self.originalfnStr.text()
        if original_filename != "":
            # if original filename is not empty, '{}' must input
            if (not original_filename.count("{")) or \
                (not original_filename.count("}")):
                self.originalhintLabel.setText(originalname_hint["Format"])
                self.okBtnEnable = self.okBtnEnable and True
            else:
                pattern = re.compile(r'\{.*\}')
                # At least include one '{.*}'
                if (pattern.search(original_filename)):
                    # If there is only one '{}', and the '{' is before '}'
                    if ((original_filename.count("{") == 1) and \
                        original_filename.count("}") == 1):
                        self.originalhintLabel.setText('')
                        self.okBtnEnable = self.okBtnEnable and True
                    # Multiple '{.*}', but still valid format
                    else:
                        self.originalhintLabel.setText(originalname_hint["Multiple"])
                        self.okBtnEnable = self.okBtnEnable and True
                else:
                    self.originalhintLabel.setText(originalname_hint["Error"])
                    self.okBtnEnable = self.okBtnEnable and False
        # Empty is valid
        else:
            self.originalhintLabel.setText('')
            self.okBtnEnable = self.okBtnEnable and True

    # Hint label for output folder
    def output_folder_validate(self):
        new_folder = self.outputStr.text()
        # If output in samefolder
        if self.outsamefolder:
            self.okBtnEnable = self.okBtnEnable and True
        # output folder must be indicated
        elif new_folder == "":
            self.outputhintLabel.setText(folder_hint["Null"])
            self.okBtnEnable = self.okBtnEnable and False
        # the path of the output folder is not valid
        elif not folder_exist(new_folder):
            self.outputhintLabel.setText(folder_hint["Not Found"])
            self.okBtnEnable = self.okBtnEnable and False
        else:
            self.outputhintLabel.setText('')
            self.okBtnEnable = self.okBtnEnable and True

    # Validate if OK button should be enabled
    def ok_btn_validate(self):
        self.okBtnEnable = True
        self.input_folder_validate()
        self.file_ext_validate()
        self.new_filename_validate()
        self.original_filename_validate()
        self.output_folder_validate()

        if(self.okBtnEnable):
            self.okBtn.setEnabled(True)
        else:
            self.okBtn.setEnabled(False)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    m = Main()
    m.show()
    sys.exit(app.exec_())
