from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QProgressBar
import sys
import os
import cv2
import xlwt
import pyzbar.pyzbar as pyzbar
import base64
import string
from main import remove_non_printable, decode_qr_code


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('invoices reader')
        self.setGeometry(100, 100, 500, 300)

        self.browseButton1 = QtWidgets.QPushButton(
            'Choose invoices Folder', self)
        self.browseButton1.setGeometry(150, 50, 200, 30)
        self.browseButton1.clicked.connect(self.choose_folder)

        self.browseButton3 = QtWidgets.QPushButton(
            'Choose Save Location', self)
        self.browseButton3.setGeometry(150, 150, 200, 30)
        self.browseButton3.clicked.connect(self.save_location)

        self.convertButton = QtWidgets.QPushButton('start', self)
        self.convertButton.setGeometry(200, 200, 100, 30)
        self.convertButton.clicked.connect(self.convert)

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(150, 100, 200, 30)
        self.progressBar.setValue(0)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setVisible(False)

    def choose_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.folder_path = str(
            QFileDialog.getExistingDirectory(self, "Select invoices Images Folder"))

    def save_location(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Select excel file Location", "", "Excel Files (*.xls);;All Files (*)")
        self.location = file_path
        if not file_path.endswith('.xls'):
            self.location = file_path + '.xls'

    def convert(self):
        if not hasattr(self, 'folder_path') or not hasattr(self, 'location'):
            QMessageBox.warning(
                self, 'Error', 'You need to select a folder and a save location!')
            return

        folder_path = self.folder_path
        try:
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet("QR code data")
            sheet.write(0, 0, "Image File")
            sheet.write(0, 1, "Name of Seller")
            sheet.write(0, 2, "VAT Number")
            sheet.write(0, 3, "Date and Time")
            sheet.write(0, 4, "Total Amount")
            sheet.write(0, 5, "VAT Amount")

            row_num = 1
            progress_dialog = QtWidgets.QProgressDialog(
                "Reading invoices...", "Cancel", 0, 100, self)
            progress_dialog.setWindowTitle("Reading invoices")
            progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
            progress_dialog.show()
            progress_dialog.setValue(0)

            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    print(f"Processing: {file_path}")
                    image = cv2.imread(file_path)
                    invoice_data, threshold = decode_qr_code(image)
                    if invoice_data:
                        invoice_data = remove_non_printable(invoice_data)
                        print(invoice_data)
                        sheet.write(row_num, 0, file_path)
                        sheet.write(row_num, 1, invoice_data[0])
                        sheet.write(row_num, 2, invoice_data[1])
                        sheet.write(row_num, 3, invoice_data[2])
                        sheet.write(row_num, 4, invoice_data[3])
                        sheet.write(row_num, 5, invoice_data[4])
                        progress_dialog.setValue(row_num)
                    else:
                        print("qr not detected")

                    row_num += 1
            workbook.save(self.location)
            progress_dialog.close()
            QMessageBox.information(
                self, 'Information', 'invoices read successful!')
        except Exception as e:
            QMessageBox.critical(
                self, 'Error', 'invoices read failed: {}'.format(str(e)))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
