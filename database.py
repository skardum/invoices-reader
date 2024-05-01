import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QDialog, QTableWidgetItem, QMessageBox, QFileDialog
from PyQt6.uic import loadUi
from datetime import datetime
import xlsxwriter


def connect_to_database():
    connection = sqlite3.connect("detections.db")
    return connection


def save_detection_to_database(connection, num_invoices, extracted_data):
    cursor = connection.cursor()
    try:
        # Insert data into main_records table
        cursor.execute("""
            INSERT INTO main_records (detection_date, num_invoices)
            VALUES (?, ?)
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), num_invoices))
        detection_id = cursor.lastrowid  # Get the last inserted detection ID

        # Insert extracted data into extracted_data table
        for data in extracted_data:
            cursor.execute("""
                INSERT INTO extracted_data (id, image_file, vendor_name, date, vat_id, invoice_total, vat_total, invoice_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (detection_id, *data))

        connection.commit()
        return detection_id
    except Exception as e:
        connection.rollback()  # Rollback changes if an error occurs
        print(f'Failed to save detection to database: {str(e)}')
        return None


def update_extracted_data(connection, detection_id, image_file, vendor_name, date, vat_id, invoice_total, vat_total, invoice_number):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO extracted_data (id, image_file, vendor_name, date, vat_id, invoice_total, vat_total, invoice_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (detection_id, image_file, vendor_name, date, vat_id, invoice_total, vat_total, invoice_number))
        connection.commit()
    except Exception as e:
        print(f'Failed to update extracted data in database: {str(e)}')


class DatabaseDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('db.ui', self)  # Load the UI file
        self.setWindowTitle("Database Viewer")
        self.connection = connect_to_database()  # Use the function directly
        self.cursor = self.connection.cursor()
        self.setup_ui()
        self.create_tables()
        self.load_main_records()

    def setup_ui(self):
        self.pushButton_4.clicked.connect(self.close)  # Exit button
        self.pushButton_3.clicked.connect(
            self.load_main_records)  # Refresh button
        self.pushButton_2.clicked.connect(
            self.export_to_excel)  # Export button
        self.pushButton.clicked.connect(self.delete_detection)  # Delete button

    def create_tables(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS main_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    detection_date TEXT,
                    num_invoices INTEGER
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS extracted_data (
                    id INTEGER,
                    image_file TEXT,
                    vendor_name TEXT,
                    date TEXT,
                    vat_id TEXT,
                    invoice_total REAL,
                    vat_total REAL,
                    invoice_number TEXT,
                    FOREIGN KEY (id) REFERENCES main_records(id)
                )
            """)
            self.connection.commit()
        except Exception as e:
            QMessageBox.critical(
                self, 'Database Error', f'Failed to create tables: {str(e)}')

    def load_main_records(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.cursor.execute("SELECT * FROM main_records")
        main_records = self.cursor.fetchall()
        for index, record in enumerate(main_records):
            self.tableWidget.insertRow(index)
            for col, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(index, col, item)

    def export_to_excel(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            detection_id = int(self.tableWidget.item(selected_row, 0).text())
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export Detected Data to Excel", "", "Excel Files (*.xlsx);;All Files (*)")
            if file_path:
                if not file_path.endswith('.xlsx'):
                    file_path += '.xlsx'
                try:
                    workbook = xlsxwriter.Workbook(file_path)
                    worksheet = workbook.add_worksheet()
                    headers = ['ID', 'Image File', 'Vendor Name', 'Date', 'VAT ID',
                               'Invoice Total', 'VAT Total', 'Invoice Number']
                    for col, header in enumerate(headers):
                        worksheet.write(0, col, header)

                    self.cursor.execute(
                        "SELECT * FROM extracted_data WHERE id=?", (detection_id,))
                    detected_data = self.cursor.fetchall()
                    for row_num, record in enumerate(detected_data, start=1):
                        for col_num, value in enumerate(record):
                            worksheet.write(row_num, col_num, value)

                    workbook.close()
                    QMessageBox.information(
                        self, 'Export Successful', 'Detected data exported to Excel successfully!')
                except Exception as e:
                    QMessageBox.warning(
                        self, 'Export Failed', f'Failed to export detected data to Excel: {str(e)}')
        else:
            QMessageBox.warning(
                self, 'No Selection', 'Please select a detection to export!')

    def delete_detection(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            detection_id = int(self.tableWidget.item(selected_row, 0).text())
            confirm = QMessageBox.question(
                self, 'Confirmation', 'Are you sure you want to delete this detection?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                try:
                    self.cursor.execute(
                        "DELETE FROM main_records WHERE id=?", (detection_id,))
                    self.cursor.execute(
                        "DELETE FROM extracted_data WHERE id=?", (detection_id,))
                    self.connection.commit()
                    self.load_main_records()
                    QMessageBox.information(
                        self, 'Deletion Successful', 'Detection deleted successfully!')
                except Exception as e:
                    QMessageBox.warning(
                        self, 'Deletion Failed', f'Failed to delete detection: {str(e)}')
        else:
            QMessageBox.warning(
                self, 'No Selection', 'Please select a detection to delete!')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = DatabaseDialog()
    dialog.exec()
