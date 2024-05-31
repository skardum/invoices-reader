import sys
import os
import cv2
import pyzbar.pyzbar as pyzbar
import base64
import re
from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QFileDialog, QLabel, QComboBox
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal, Qt, QObject
from PyQt6.QtGui import QPixmap
from PyQt6.uic import loadUi
import PIL.Image
from database import connect_to_database, save_detection_to_database, DatabaseDialog, insert_extracted_data, ConnectionPool
import google.generativeai as genai
import time
import sqlite3
from ocr import ocr_text, update_ui_with_ocrdata, extract_with_gemini
from ollama_ocr import ocr_for_ollama, process_ollama_and_fill_ui, update_ui_with_ollama_data

# Create a connection pool instance
pool = ConnectionPool(max_connections=5)

# Load environment variables
load_dotenv()

# Configure Google API
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def gemini_process_img_and_fill_ui(image_data):
    try:
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content(['''Extract the following fields from this invoice and format the information as a dictionary:
                                           - Vendor Name
                                           - Vendor VAT ID
                                           - Date
                                           - Total Amount
                                           - VAT Amount
                                           - invoice number

                                           Please provide the extracted information in the format:
                                           {
                                               'vendor_name': '...',
                                               'vat_id': '...',
                                               'date': '...',
                                               'invoice_total': '...',
                                               'vat_total': '...',
                                               'invoice_number': '...'
                                           }''',
                                           image_data
                                           ])

        print(response.text)
        pattern = r'{.*?}'
        match = re.search(pattern, response.text, re.DOTALL)
        if match:
            print(match)
            dictionary_text = match.group()
            parsed_data = eval(dictionary_text)
            return parsed_data
        else:
            print("No dictionary found in the gemini output.")
            return None
    except Exception as e:
        print(f"Error during gemini processing: {e}")
        return None


def update_ui_with_data(ui, data):
    ui.vendor_lineedit.setText(data.get('vendor_name', ''))
    ui.vatid_lineedit.setText(data.get('vat_id', ''))
    ui.date_lineedit.setText(data.get('date', ''))

    # Convert float to string before setting the text
    invoice_total = str(data.get('invoice_total', ''))
    ui.total_lineedit.setText(invoice_total)

    # Convert float to string before setting the text
    vat_total = str(data.get('vat_total', ''))
    ui.vatamount_lineedit.setText(vat_total)
    invoice_number = str(data.get('invoice_number', ''))
    ui.invoicenumber_lineedit.setText(invoice_number)


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


class AiExtractor(QObject):
    progress_changed = pyqtSignal(int, str)  # Signal for progress updates
    started = pyqtSignal()  # Signal for indicating start of processing
    # Signal to emit extracted data and image path
    data_extracted = pyqtSignal(dict, str)

    def __init__(self, image_path, ui, db_connection, parent=None):
        super(AiExtractor, self).__init__(parent)
        self.image_path = image_path  # Set image_path
        self.ui = ui
        self.db_connection = db_connection

    def extract(self):
        self.started.emit()  # Emit signal indicating start of processing

        try:
            # Read the image file
            with open(self.image_path, 'rb') as file:
                image_data = PIL.Image.open(file)
                self.progress_changed.emit(
                    25, "Image loaded")  # Emit progress update
                parsed_data = gemini_process_img_and_fill_ui(image_data)
                if parsed_data:
                    self.progress_changed.emit(
                        50, "Data extracted")  # Emit progress update
                    update_ui_with_data(self.ui, parsed_data)
                    # Save data to database
                    # Emit signal with extracted data and image path
                    self.data_extracted.emit(parsed_data, self.image_path)
                    self.progress_changed.emit(
                        100, "Extraction complete")  # Emit progress update
                else:
                    self.progress_changed.emit(
                        0, "No data extracted")  # Emit progress update
        except FileNotFoundError:
            self.progress_changed.emit(
                0, "File not found")  # Emit progress update
        except Exception as e:
            self.progress_changed.emit(
                0, f"Error: {str(e)}")  # Emit progress update


def remove_non_printable(text):
    """
    تنظف النص المعطى بإزالة الأحرف غير القابلة للطباعة وبعض الأحرف الخاصة،
    وتستبدلها بفواصل، ثم تزيل الفواصل المكررة وتقسم النص إلى قائمة بناءً على الفواصل.

    Args:
    text (str): النص الذي يحتاج إلى تنظيف.

    Returns:
    dict: قاموس يحتوي على المعلومات المطلوبة.
    """
    # استبدال الأحرف الخاصة بفواصل
    chars_to_remove = "?,☺,☻,♥,♦,♠,♣,§,¶,+,="
    for char in chars_to_remove:
        text = text.replace(char, ",")

    # إزالة الفاصلة من بداية النص إذا كانت موجودة
    if len(text) > 0 and text[0] == ",":
        text = text[1:]

    # إزالة الفواصل المكررة
    text = ','.join(text.split(","))
    cleaned_string = text.replace("\x01", ",").replace("\x02", ",").replace(
        "\x03", ",").replace("\x04", ",").replace("\x05", ",").replace("\x0e", ",").replace("\x1e", ",").replace("\x13", ",").replace("\x1f", ",").replace("\x1a", ",").replace("\x11", ",").replace("\x10", ",").replace("\x1c", ",")
    cleaned_string = cleaned_string.replace("\x0f", ",").replace(
        "\x14", ",").replace("\x15", ",").replace("\x06", ",").replace("\x07", ",").replace("\x19", ",").replace("\x08", ",").replace("\t", ",").replace(".00", "").replace("\x16", ",").replace("\x0b", ",").replace("\x0c", ",").replace("\x1b", ",")

    # تقسيم النص المنظف إلى قائمة بناءً على الفواصل
    result = cleaned_string.split(",")
    result2 = list(filter(None, result))
    # إنشاء قاموس من القائمة بفرض ترتيب ثابت
    print(result2)
    date_pattern = r'^\d{4}-\d{2}-\d{2}'
    match = re.search(date_pattern, result2[2] if len(result2) > 1 else '')
    print(match)
    date = match.group() if match else result2[2] if len(result2) > 1 else ''
    return {
        'vendor_name': result2[0] if len(result2) > 0 else '',
        'date': date,
        'vat_id': result2[1] if len(result2) > 2 else '',
        'invoice_total': result2[3] if len(result2) > 3 else '',
        'vat_total': result2[4] if len(result2) > 4 else ''
    }


def decode_qr_code(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Define a list of parameter combinations to try for adaptive thresholding
    adaptive_threshold_params = [
        # Combination 1
        (cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 2),
        # Combination 2
        (cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 2),
        # Combination 3
        (cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 3),
        # Combination 4
        (cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 3),
        # Combination 5
        (cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 35, 4),
        # Combination 6
        (cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, 4),
        # Add more parameter combinations as needed
    ]

    # Define a list of additional preprocessing settings to try
    preprocessing_settings = [
        # Preprocessing 1: No additional preprocessing
        lambda img: img,
        # Preprocessing 2: Gaussian blur
        lambda img: cv2.GaussianBlur(img, (5, 5), 0),
        # Preprocessing 3: Median blur
        lambda img: cv2.medianBlur(img, 5),
        # Preprocessing 4: Bilateral filter
        lambda img: cv2.bilateralFilter(img, 9, 75, 75),
        # Preprocessing 5: Adaptive histogram equalization
        lambda img: cv2.equalizeHist(img),
        # Add more preprocessing settings as needed
    ]

    for preprocess_func in preprocessing_settings:
        try:
            # Apply additional preprocessing
            processed_img = preprocess_func(gray)

            for params in adaptive_threshold_params:
                try:
                    # Apply adaptive thresholding with current parameters
                    threshold = cv2.adaptiveThreshold(
                        processed_img, 255, *params)

                    # Decode QR codes using PyZbar
                    qr_detections = pyzbar.decode(threshold)

                    for detection in qr_detections:
                        data = detection.data
                        try:
                            # Attempt to decode QR code data
                            text = base64.b64decode(data).decode("utf-8")
                            return text, threshold
                        except UnicodeDecodeError:
                            try:
                                # محاولة فك التشفير باستخدام ISO-8859-1
                                text = base64.b64decode(data).decode('iso-8859-1')
                            except UnicodeDecodeError:
                                try:
                                    # محاولة فك التشفير باستخدام windows-1256
                                    text = base64.b64decode(data).decode('windows-1256')

                                except Exception as e:
                                    # Handle decoding errors
                                    print(f"Error decoding QR code data: {e}")
                                    continue
                except Exception as e:
                    # Handle thresholding errors
                    print(f"Error applying adaptive thresholding: {e}")
                    continue
        except Exception as e:
            # Handle preprocessing errors
            print(f"Error applying preprocessing: {e}")
            continue

    # Return None if QR code is not detected
    return None, None


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('qrdetector.ui', self)  # Load the UI file
        self.folder_path = None
        self.location = None
        self.sheet = None
        self.browseButton1.clicked.connect(self.choose_folder)

        self.convertButton.clicked.connect(self.convert)
        self.save.clicked.connect(self.save_invoice)
        self.last.clicked.connect(self.load_last_invoice)
        self.next.clicked.connect(self.load_next_invoice)
        self.previous.clicked.connect(self.load_previous_invoice)
        self.first.clicked.connect(self.load_first_invoice)
        self.previous_extractions.clicked.connect(self.show_database_form)
        self.current_row = 2  # Start from row 2 to skip header
        self.setStyleSheet(dark_theme_stylesheet)
        self.current_detection_id = self.generate_unique_detection_id()

        # Connect the AI extract button to the new model
        self.ai_button.clicked.connect(self.ai_extract)

        # Initialize progress dialog
        self.progress_dialog = None

        # Connect to the database
        self.db_connection = connect_to_database(pool)  # Use the connection pool to manage database connections

        # Set row factory to Row for better dictionary-like access
        self.db_connection.row_factory = sqlite3.Row
        self.cursor = self.db_connection.cursor()
        self.image_path = None
        self.new_batch.clicked.connect(self.create_new_batch)

        # Initialize records list and current record index for navigation
        self.records = []
        self.current_record_index = 0
        self.ocr_btn.clicked.connect(self.ocr)

        # Add comboBox for processing mode selection
        self.comboBox.currentIndexChanged.connect(self.update_processing_mode)
        self.current_processing_mode = "بدون"  # Default mode

    def update_processing_mode(self, index):
        # Update current processing mode based on comboBox selection
        self.current_processing_mode = self.comboBox.itemText(index)
        print(f"Processing mode updated to: {self.current_processing_mode}")

    def ocr(self):
        image = self.label_7.pixmap().toImage().save('ocr.jpg', 'JPG')
        if self.current_processing_mode == "gemini":
            text = ocr_text("ocr.jpg")
            data = extract_with_gemini(text)
            update_ui_with_ocrdata(self, data)
        elif self.current_processing_mode == "ollama":
            text = ocr_for_ollama("ocr.jpg")
            data = process_ollama_and_fill_ui(text)
            update_ui_with_ollama_data(self, data)

    def show_database_form(self):
        database_dialog = DatabaseDialog(self, pool)
        database_dialog.exec()

    def create_new_batch(self):
        # Clear all inputs
        self.vendor_lineedit.clear()
        self.vatid_lineedit.clear()
        self.date_lineedit.clear()
        self.total_lineedit.clear()
        self.vatamount_lineedit.clear()
        self.invoicenumber_lineedit.clear()

        # Create a new unique detection ID
        self.current_detection_id = self.generate_unique_detection_id()

    def generate_unique_detection_id(self):
        # Generate a unique ID (example method, modify as needed)
        detection_id = int(time.time())  # Using current time as a simple unique ID
        print(f"New detection ID: {detection_id}")
        return detection_id

    def ai_extract(self):
        # Get the currently displayed pixmap
        pixmap = QPixmap(self.image_path)

        # Convert pixmap to image
        image = pixmap.toImage()

        # Save the image to a temporary file
        image_path = "temp_image.jpg"
        image.save(image_path)

        # Create an instance of AiExtractor and move it to a separate thread
        self.ai_extractor = AiExtractor(image_path, self, self.db_connection)
        self.ai_thread = QtCore.QThread()
        self.ai_extractor.moveToThread(self.ai_thread)

        # Connect signals
        self.ai_extractor.progress_changed.connect(self.update_progress)
        self.ai_extractor.started.connect(self.show_progress_dialog)
        self.ai_thread.started.connect(self.ai_extractor.extract)

        # Start the thread
        self.ai_thread.start()

    def show_progress_dialog(self):
        # Show progress dialog when processing starts
        self.progress_dialog = ProgressDialog()
        self.progress_dialog.show()

    def update_progress(self, value, message):
        # Update progress dialog and UI with progress information
        self.progress_dialog.progressBar.setValue(value)
        self.progress_dialog.progressLabel.setText(message)

        # Close progress dialog when progress reaches 100
        if value == 100:
            self.progress_dialog.close()

    def load_invoice_data(self, detection_id):
        try:
            self.cursor.execute("SELECT * FROM extracted_data WHERE id=?", (detection_id,))
            records = self.cursor.fetchall()
            if records:
                self.records = records  # Store the records
                self.display_record(records[0])
                self.current_record_index = 0  # Reset the index to the first record
            else:
                QMessageBox.warning(self, 'Error', 'No record found!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load data: {str(e)}')

    def save_invoice(self):
        try:
            current_record = dict(self.records[self.current_record_index])  # Convert sqlite3.Row to dictionary
            self.cursor.execute("""
                UPDATE extracted_data
                SET vendor_name=?, vat_id=?, date=?, invoice_total=?, vat_total=?, invoice_number=?
                WHERE id=? and image_file=?
            """, (
                self.vendor_lineedit.text(),
                self.vatid_lineedit.text(),
                self.date_lineedit.text(),
                float(self.total_lineedit.text()),
                float(self.vatamount_lineedit.text()),
                self.invoicenumber_lineedit.text(),
                current_record['id'],
                current_record['image_file']
            ))
            self.db_connection.commit()
            QMessageBox.information(self, 'Information', 'Invoice updated successfully!')

            # Update the corresponding record in the records list with the new data
            current_record['vendor_name'] = self.vendor_lineedit.text()
            current_record['vat_id'] = self.vatid_lineedit.text()
            current_record['date'] = self.date_lineedit.text()
            current_record['invoice_total'] = float(self.total_lineedit.text())
            current_record['vat_total'] = float(self.vatamount_lineedit.text())
            current_record['invoice_number'] = self.invoicenumber_lineedit.text()

            # Update the UI with the edited data
            self.display_record(current_record)

            # Update the records list with the modified record
            self.records[self.current_record_index] = current_record

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to update invoice: {str(e)}')

    def display_record(self, records):
        # Update UI elements with data from the record
        self.vendor_lineedit.setText(records['vendor_name'])
        self.vatid_lineedit.setText(records['vat_id'])
        self.date_lineedit.setText(records['date'])
        self.total_lineedit.setText(str(records['invoice_total']))
        self.vatamount_lineedit.setText(str(records['vat_total']))
        self.invoicenumber_lineedit.setText(records['invoice_number'])

        # Load image into QLabel
        image_path = records['image_file']
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.label_7.setPixmap(pixmap)
        else:
            QMessageBox.warning(self, 'Error', 'Image file not found at the specified path.')

    def load_next_invoice(self):
        print("Loading next invoice...")
        if self.current_record_index < len(self.records) - 1:
            self.current_record_index += 1
            print("Current record index:", self.current_record_index)
            self.display_record(self.records[self.current_record_index])
            print("Invoice loaded successfully.")
        else:
            print("No more invoices to load.")

    def load_previous_invoice(self):
        print("Loading previous invoice...")
        if self.current_record_index > 0:
            self.current_record_index -= 1
            print("Current record index:", self.current_record_index)
            self.display_record(self.records[self.current_record_index])
            print("Invoice loaded successfully.")
        else:
            print("Already at the first invoice.")

    def load_first_invoice(self):
        print("Loading first invoice...")
        if self.records:
            self.current_record_index = 0
            print("Current record index:", self.current_record_index)
            self.display_record(self.records[self.current_record_index])
            print("First invoice loaded successfully.")
        else:
            print("No invoices available.")

    def load_last_invoice(self):
        print("Loading last invoice...")
        if self.records:
            self.current_record_index = len(self.records) - 1
            print("Current record index:", self.current_record_index)
            self.display_record(self.records[self.current_record_index])
            print("Last invoice loaded successfully.")
        else:
            print("No invoices available.")

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

        if not folder_path:
            QMessageBox.warning(
                self, 'Error', 'You need to select a folder!')
            return

        try:
            num_files = len(os.listdir(folder_path))
            self.progressBar.setMaximum(num_files)

            # إنشاء سجل في جدول main_records واستخدام self.current_detection_id
            save_detection_to_database(
                self.db_connection, self.current_detection_id, num_files)

            if self.current_detection_id is None:
                QMessageBox.warning(
                    self, 'Warning', 'Failed to create a detection record in the database.')
                return
            processed_files = 0
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    image = cv2.imread(file_path)
                    if self.current_processing_mode == "بدون":
                        invoice_data, threshold = decode_qr_code(image)
                        if invoice_data:
                            invoice_data_dict = remove_non_printable(invoice_data)
                            invoice_data_dict['image_path'] = file_path
                            invoice_data_dict['invoice_number'] = "0"  # Update as needed
                            insert_extracted_data(
                                self.db_connection, self.current_detection_id, invoice_data_dict['image_path'], invoice_data_dict['vendor_name'], invoice_data_dict['date'], invoice_data_dict['vat_id'], invoice_data_dict['invoice_total'], invoice_data_dict['vat_total'], invoice_data_dict['invoice_number'])
                        else:
                            insert_extracted_data(
                                self.db_connection, self.current_detection_id, file_path, "qr not detected", 0, 0, 0, 0, 0)
                    elif self.current_processing_mode == "GEMINI":
                        text = ocr_text(file_path)
                        data = extract_with_gemini(text)
                        if data:
                            insert_extracted_data(
                                self.db_connection, self.current_detection_id, file_path, data['vendor_name'], data['date'], data['vat_id'], data['invoice_total'], data['vat_total'], data['invoice_number'])
                        else:
                            insert_extracted_data(
                                self.db_connection, self.current_detection_id, file_path, "data not extracted", 0, 0, 0, 0, 0)
                    elif self.current_processing_mode == "OLLAMA":
                        text = ocr_for_ollama(file_path)
                        data = process_ollama_and_fill_ui(text)
                        if data:
                            insert_extracted_data(
                                self.db_connection, self.current_detection_id, file_path, data['vendor_name'], data['date'], data['vat_id'], data['invoice_total'], data['vat_total'], data['invoice_number'])
                        else:
                            insert_extracted_data(
                                self.db_connection, self.current_detection_id, file_path, "data not extracted", 0, 0, 0, 0, 0)
                processed_files += 1
                progress_percent = int((processed_files / num_files) * 100)
                self.progressBar.setValue(progress_percent)  # Update the progress bar

            QMessageBox.information(
                self, 'Information', 'All invoices processed successfully!')

            # Automatically load the first invoice after saving

            self.load_invoice_data(self.current_detection_id)  # Load data after saving
            print("Data loaded successfully!")
        except Exception as e:
            QMessageBox.critical(
                self, 'Error', f'Invoices read failed: {str(e)}')


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
