from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
import sys
import os
import xlwt
import ollama
import cv2
import base64


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Invoices Reader')
        self.setGeometry(100, 100, 500, 300)

        self.browseButton1 = QtWidgets.QPushButton(
            'Choose Invoices Folder', self)
        self.browseButton1.setGeometry(150, 50, 200, 30)
        self.browseButton1.clicked.connect(self.choose_folder)

        self.browseButton3 = QtWidgets.QPushButton(
            'Choose Save Location', self)
        self.browseButton3.setGeometry(150, 100, 200, 30)
        self.browseButton3.clicked.connect(self.save_location)

        self.convertButton = QtWidgets.QPushButton('Start', self)
        self.convertButton.setGeometry(200, 150, 100, 30)
        self.convertButton.clicked.connect(self.convert)

    def choose_folder(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        self.folder_path = str(
            QtWidgets.QFileDialog.getExistingDirectory(self, "Select Invoices Images Folder"))

    def save_location(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Select Excel File Location", "", "Excel Files (*.xls);;All Files (*)")
        self.location = file_path
        if not file_path.endswith('.xls'):
            self.location = file_path + '.xls'

    def convert(self):
        if not hasattr(self, 'folder_path') or not hasattr(self, 'location'):
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'You need to select a folder and a save location!')
            return

        try:
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet("QR Code Data")
            sheet.write(0, 0, "Image File")
            sheet.write(0, 1, "Name of Seller")
            sheet.write(0, 2, "VAT Number")
            sheet.write(0, 3, "Date and Time")
            sheet.write(0, 4, "Total Amount")
            sheet.write(0, 5, "VAT Amount")

            num_files = len(os.listdir(self.folder_path))
            self.progressBar = QtWidgets.QProgressBar(self)
            self.progressBar.setGeometry(150, 200, 200, 30)
            self.progressBar.setValue(0)
            self.progressBar.setAlignment(Qt.AlignCenter)
            self.progressBar.setVisible(True)
            self.progressBar.setMaximum(num_files)

            row_num = 1
            for file_name in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, file_name)
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as file:
                        response = ollama.chat(
                            model='llava',
                            messages=[
                                {
                                    'role': 'user',
                                    'content': 'Extract Name of vendor,vendor VAT Number,Date,Total Amount,VAT Amount from this invoice and image format it as text with "," between values',
                                    'images': [file.read()],
                                },
                            ],
                        )
                        content = response['message']['content']
                        invoice_data = content.split(',')
                        sheet.write(row_num, 0, file_path)
                        for col, data in enumerate(invoice_data, start=1):
                            sheet.write(row_num, col, data)
                        self.progressBar.setValue(row_num)
                        row_num += 1

            workbook.save(self.location)
            self.progressBar.setVisible(False)
            QtWidgets.QMessageBox.information(
                self, 'Information', 'Invoices read successfully!')
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, 'Error', f'Invoices read failed: {str(e)}')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
