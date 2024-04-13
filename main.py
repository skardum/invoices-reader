import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QDialog
from PyQt5.uic import loadUi
import os
import cv2
import pyzbar.pyzbar as pyzbar
import base64
import openpyxl
from ai import process_text_and_fill_ui, update_ui_with_data
from threading import Thread
import PIL.Image

# Define the dark theme stylesheet
dark_theme_stylesheet = """
QWidget {
    background-color: #333;
    color: #fff;
}

QPushButton {
    background-color: #555;
    color: #fff;
    border: 2px solid #444;
    border-radius: 5px;
    padding: 5px 10px;
}

QPushButton:hover {
    background-color: #666;
}

QLineEdit, QTextEdit {
    background-color: #444;
    color: #fff;
    border: 1px solid #222;
    border-radius: 5px;
    padding: 5px;
}

QLabel {
    color: #fff;
}

QProgressBar {
    background-color: #444;
    color: #fff;
    border: 1px solid #222;
    border-radius: 5px;
}

QProgressBar::chunk {
    background-color: #666;
}
"""


class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super(ProgressDialog, self).__init__(parent)
        loadUi('progress_dialog.ui', self)  # Load the UI file
        self.setModal(True)
        self.setWindowTitle("Processing")
        self.progressBar.setRange(0, 0)  # Indeterminate progress bar


class AiExtractThread(Thread):
    def __init__(self, image_path, ui, parent=None):
        super(AiExtractThread, self).__init__(parent)
        self.image_path = image_path
        self.ui = ui
        self.progress_dialog = ProgressDialog()
        self.progress_dialog.show()

    def run(self):
        try:
            # Read the image file
            with open(self.image_path, 'rb') as file:
                image_data = PIL.Image.open(file)
                parsed_data = process_text_and_fill_ui(image_data)
                if parsed_data:
                    update_ui_with_data(self.ui, parsed_data)
        except Exception as e:
            print(f"Error during AI extraction: {e}")


def remove_non_printable(text):
    # Replace "☺,☻,♥,♦,♠,♣,§,¶" with ","
    chars_to_remove = "?,☺,☻,♥,♦,♠,♣,§,¶,+,="
    for char in chars_to_remove:
        text = text.replace(char, ",")

    # Remove "," from the beginning of the string
    if len(text) > 0 and text[0] == ",":
        text = text[1:]
    # Remove duplicate ","
    text = ','.join(text.split(","))
    cleaned_string = text.replace("\x01", ",").replace("\x02", ",").replace(
        "\x03", ",").replace("\x04", ",").replace("\x05", ",").replace("\x0e", ",").replace("\x1e", ",").replace("\x13", ",").replace("\x1f", ",").replace("\x1a", ",")
    cleaned_string = cleaned_string.replace("\x0f", ",").replace(
        "\x14", ",").replace("\x15", ",").replace("\x06", ",").replace("\x07", ",").replace("\x19", ",").replace("\x08", ",").replace("\t", ",").replace(".00", "").replace("\x16", ",")
    # Split the string by "," and store it into a list
    result = cleaned_string.split(",")
    result2 = list(filter(None, result))
    return result2


def decode_qr_code(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    threshold = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 2)
    qr_detections = pyzbar.decode(threshold)

    for detection in qr_detections:
        data = detection.data
        try:
            text = base64.b64decode(data).decode("utf-8")
            return text, threshold
        except:
            try:
                image_data = PIL.Image.fromarray(
                    cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                parsed_data = process_text_and_fill_ui(image_data)
                if parsed_data:
                    # Construct the text string from the parsed data
                    text = f"{parsed_data['vendor_name']},{parsed_data['vendor_vat_id']},{parsed_data['date']},{parsed_data['invoice_total']},{parsed_data['vat_amount']}"
                    return text, threshold
            except Exception as e:
                print(f"Error during Gemini AI processing: {e}")

            # If both QR detection and Gemini AI fail, return None
            return None, threshold

    return None, threshold


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('qrdetector.ui', self)  # Load the UI file
        self.folder_path = None
        self.location = None
        self.sheet = None
        self.browseButton1.clicked.connect(self.choose_folder)
        self.browseButton3.clicked.connect(self.save_location)
        self.convertButton.clicked.connect(self.convert)
        self.save.clicked.connect(self.save_invoice)
        self.last.clicked.connect(self.load_next_invoice)
        self.next.clicked.connect(self.load_next_invoice)
        self.previous.clicked.connect(self.load_previous_invoice)
        self.first.clicked.connect(self.load_first_invoice)
        self.current_row = 2  # Start from row 2 to skip header
        # Apply dark theme stylesheet
        self.setStyleSheet(dark_theme_stylesheet)
        # Connect the AI extract button to the new model
        self.ai_button.clicked.connect(self.ai_extract)

    def ai_extract(self):
        # Get the currently displayed pixmap from the graphics view
        pixmap = self.graphicsView.scene().items()[0].pixmap()

        # Convert pixmap to image
        image = pixmap.toImage()

        # Save the image to a temporary file (or use it directly if supported by ocr_and_ai_extraction)
        image_path = "temp_image.jpg"  # Temporary image path
        image.save(image_path)

        ai_thread = AiExtractThread(image_path, self)
        ai_thread.start()

    def load_invoice_data(self, row):
        try:
            if self.location is None:
                QMessageBox.warning(
                    self, 'Error', 'Please select an Excel file location first!')
                return

            if not os.path.exists(self.location):
                QMessageBox.warning(
                    self, 'Error', 'The selected Excel file does not exist!')
                return

            workbook = openpyxl.load_workbook(self.location)
            self.sheet = workbook["QR code data"]
            num_rows = self.sheet.max_row

            if row < 2 or row > num_rows + 1:
                QMessageBox.warning(self, 'Error', 'Invalid row number!')
                return

            image_path = self.sheet.cell(row=row, column=1).value
            # Standardize the path format by replacing backslashes with forward slashes
            image_path = image_path.replace("\\", "/")

            print("Attempting to load image from:",
                  image_path)  # Debug statement

            vendor_name = self.sheet.cell(row=row, column=2).value
            vat_id = self.sheet.cell(row=row, column=3).value
            date = self.sheet.cell(row=row, column=4).value
            total_amount = self.sheet.cell(row=row, column=5).value
            vat_amount = self.sheet.cell(row=row, column=6).value

            if os.path.exists(image_path):
                print("Image exists at:", image_path)  # Debug statement
                pixmap = QtGui.QPixmap(image_path)
                if not pixmap.isNull():
                    scene = QtWidgets.QGraphicsScene()
                    pixmap_item = QtWidgets.QGraphicsPixmapItem(pixmap)
                    scene.addItem(pixmap_item)
                    self.graphicsView.setScene(scene)
                else:
                    print("Failed to load image at:",
                          image_path)  # Debug statement
            else:
                print("Image does not exist at:",
                      image_path)  # Debug statement

            self.vendor_lineedit.setText(str(vendor_name))
            self.vatid_lineedit.setText(str(vat_id))
            self.date_lineedit.setText(str(date))
            self.total_lineedit.setText(str(total_amount))
            self.vatamount_lineedit.setText(str(vat_amount))
        except Exception as e:
            QMessageBox.critical(
                self, 'Error', f'Failed to load invoice data: {str(e)}')

    def load_next_invoice(self):
        if self.sheet is not None:
            num_rows = self.sheet.max_row
            if self.current_row < num_rows:
                self.current_row += 1
                self.load_invoice_data(self.current_row)

    def load_previous_invoice(self):
        if self.current_row > 2:
            self.current_row -= 1
            self.load_invoice_data(self.current_row)

    def load_first_invoice(self):
        self.current_row = 2
        self.load_invoice_data(self.current_row)

    def choose_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select invoices Images Folder")
        if folder_path:
            self.folder_path = folder_path
            self.folder_path_label.setText(folder_path)

    def save_location(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Select excel file Location", "", "Excel Files (*.xlsx);;All Files (*)")
        if file_path:
            if not file_path.endswith('.xlsx'):
                file_path += '.xlsx'
            self.location = file_path
            self.location_label.setText(file_path)

    def convert(self):
        folder_path = self.folder_path
        location = self.location

        if not folder_path or not location:
            QMessageBox.warning(
                self, 'Error', 'You need to select a folder and a save location!')
            return

        try:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "QR code data"
            sheet.append(["Image File", "Name of Seller",
                          "VAT Number", "Date and Time", "Total Amount", "VAT Amount"])

            num_files = len(os.listdir(folder_path))
            self.progressBar.setMaximum(num_files)

            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    image = cv2.imread(file_path)
                    invoice_data, threshold = decode_qr_code(image)
                    if invoice_data:
                        # Clean the invoice data using the remove_non_printable function
                        invoice_data = remove_non_printable(invoice_data)
                        # Additional cleaning step before writing to Excel
                        cleaned_invoice_data = ["".join(
                            char for char in item if char.isprintable()) for item in invoice_data]
                        sheet.append([file_path] + cleaned_invoice_data)
                    else:
                        image_data = PIL.Image.open(file_path)
                        parsed_data = process_text_and_fill_ui(image_data)
                        if parsed_data:
                            sheet.append([file_path, parsed_data['vendor_name'], parsed_data['vendor_vat_id'],
                                          parsed_data['date'], parsed_data['invoice_total'], parsed_data['vat_amount']])
                        else:
                            sheet.append(
                                [file_path, "qr not detected", 0, 0, 0, 0])

                    self.progressBar.setValue(sheet.max_row)

            workbook.save(location)
            QMessageBox.information(
                self, 'Information', 'Invoices read successful!')

            # Automatically load the first invoice after saving
            self.current_row = 2
            self.load_invoice_data(self.current_row)  # Load data after saving
            print("Data loaded successfully!")
        except Exception as e:
            QMessageBox.critical(
                self, 'Error', f'Invoices read failed: {str(e)}')

    def save_invoice(self):
        try:
            if self.location is None or not os.path.exists(self.location):
                QMessageBox.warning(
                    self, 'Error', 'Please select a valid Excel file location!')
                return

            workbook = openpyxl.load_workbook(self.location)
            sheet = workbook["QR code data"]

            row = self.current_row

            vendor_name = self.vendor_lineedit.text()
            vat_id = self.vatid_lineedit.text()
            date = self.date_lineedit.text()
            total_amount = self.total_lineedit.text()
            vat_amount = self.vatamount_lineedit.text()

            sheet.cell(row=row, column=2, value=vendor_name)
            sheet.cell(row=row, column=3, value=vat_id)
            sheet.cell(row=row, column=4, value=date)
            sheet.cell(row=row, column=5, value=total_amount)
            sheet.cell(row=row, column=6, value=vat_amount)

            workbook.save(self.location)
            QMessageBox.information(
                self, 'Information', 'Invoice saved successfully!')
        except Exception as e:
            QMessageBox.critical(
                self, 'Error', f'Failed to save invoice: {str(e)}')


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
