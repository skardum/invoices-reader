import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QDialog, QTableWidgetItem, QMessageBox, QFileDialog
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from datetime import datetime
import xlsxwriter
import os


class ConnectionPool:
    def __init__(self, max_connections):
        self.max_connections = max_connections
        self.connections = []

    def get_connection(self):
        if not self.connections:
            connection = sqlite3.connect("detections.db")
            self.connections.append(connection)
            return connection
        else:
            return self.connections.pop(0)

    def release_connection(self, connection):
        self.connections.append(connection)


def connect_to_database(pool):
    return pool.get_connection()


def save_detection_to_database(connection, detection_id, num_invoices):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO main_records (id, detection_date, num_invoices)
            VALUES (?, ?, ?)
        """, (detection_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), num_invoices))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f'Failed to save detection to database: {str(e)}')
        return None
    return detection_id


def insert_extracted_data(connection, detection_id, image_path, vendor_name, date, vat_id, invoice_total, vat_total, invoice_number):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO extracted_data (id, image_file, vendor_name, date, vat_id, invoice_total, vat_total, invoice_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (detection_id, image_path, vendor_name, date, vat_id, invoice_total, vat_total, invoice_number))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f'Failed to insert extracted data: {str(e)}')


class DatabaseDialog(QDialog):
    def __init__(self, main_window=None, pool=None):
        super().__init__()
        self.main_window = main_window
        loadUi('db.ui', self)
        self.setWindowTitle("Database Viewer")
        self.pool = pool
        self.connection = connect_to_database(self.pool)
        self.cursor = self.connection.cursor()
        self.setup_ui()
        self.create_tables()
        self.load_main_records()

    def setup_ui(self):
        self.pushButton_4.clicked.connect(self.close)
        self.export_btn.clicked.connect(self.export_to_excel)
        self.delete_btn.clicked.connect(self.delete_detection)
        self.load_in_main_ui.clicked.connect(lambda: self.load_in_main_app(self.main_window))

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
        try:
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)
            self.cursor.execute("SELECT * FROM main_records")
            main_records = self.cursor.fetchall()
            for index, record in enumerate(main_records):
                self.tableWidget.insertRow(index)
                for col, value in enumerate(record):
                    item = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(index, col, item)
        except Exception as e:
            QMessageBox.critical(
                self, 'Database Error', f'Failed to load main records: {str(e)}')

    def export_to_excel(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'No Selection', 'Please select a detection to export!')
            return

        detection_id = self.tableWidget.item(selected_row, 0).text()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Detected Data to Excel", "", "Excel Files (*.xlsx);;All Files (*)")
        if not file_path:
            return

        if not file_path.endswith('.xlsx'):
            file_path += '.xlsx'

        try:
            workbook = xlsxwriter.Workbook(file_path)
            worksheet = workbook.add_worksheet()
            headers = ['ID', 'Image File', 'Vendor Name', 'Date',
                       'VAT ID', 'Invoice Total', 'VAT Total', 'Invoice Number']
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)

            self.cursor.execute("SELECT * FROM extracted_data WHERE id=?", (detection_id,))
            detected_data = self.cursor.fetchall()
            for row_num, record in enumerate(detected_data, start=1):
                for col_num, value in enumerate(record):
                    worksheet.write(row_num, col_num, value)

            workbook.close()
            QMessageBox.information(self, 'Export Successful', 'Detected data exported to Excel successfully!')
        except Exception as e:
            QMessageBox.warning(self, 'Export Failed', f'Failed to export detected data to Excel: {str(e)}')

    def delete_detection(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'No Selection', 'Please select a detection to delete!')
            return

        detection_id = self.tableWidget.item(selected_row, 0).text()
        confirm = QMessageBox.question(
            self, 'Confirmation', 'Are you sure you want to delete this detection?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                self.cursor.execute(
                    "DELETE FROM extracted_data WHERE id=?", (detection_id,))
                self.cursor.execute(
                    "DELETE FROM main_records WHERE id=?", (detection_id,))
                self.connection.commit()
                self.load_main_records()
                QMessageBox.information(
                    self, 'Deletion Successful', 'Detection and related invoices deleted successfully!')
            except Exception as e:
                QMessageBox.warning(
                    self, 'Deletion Failed', f'Failed to delete detection: {str(e)}')

    def load_in_main_app(self, main_window):
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'No Selection', 'Please select a detection to load!')
            return

        detection_id = self.tableWidget.item(selected_row, 0).text()

        try:
            main_window.cursor.execute("SELECT * FROM extracted_data WHERE id=?", (detection_id,))
            main_window.records = main_window.cursor.fetchall()
            if main_window.records:
                main_window.display_record(main_window.records[0])
                main_window.current_record_index = 0
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to fetch records: {str(e)}')

        try:
            self.cursor.execute(
                "SELECT image_file, vendor_name, date, vat_id, invoice_total, vat_total, invoice_number FROM extracted_data WHERE id=?", (detection_id,))
            data = self.cursor.fetchone()
            if data:
                image_path, vendor_name, date, vat_id, invoice_total, vat_total, invoice_number = data

                main_window.vendor_lineedit.setText(vendor_name)
                main_window.vatid_lineedit.setText(vat_id)
                main_window.date_lineedit.setText(date)
                main_window.total_lineedit.setText(str(invoice_total))
                main_window.vatamount_lineedit.setText(str(vat_total))
                main_window.invoicenumber_lineedit.setText(invoice_number)

                if os.path.exists(image_path):
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        main_window.label_7.setPixmap(pixmap)
                        main_window.label_7.setScaledContents(True)  # Maintain aspect ratio
                else:
                    QMessageBox.warning(self, 'Image Load Error', 'Image file does not exist.')
            else:
                QMessageBox.warning(self, 'Data Load Error', 'No data found for the selected detection.')
        except Exception as e:
            QMessageBox.critical(self, 'Loading Error', f'Failed to load data: {str(e)}')

    def closeEvent(self, event):
        self.pool.release_connection(self.connection)
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pool = ConnectionPool(max_connections=5)
    dialog = DatabaseDialog(pool=pool)
    dialog.exec()
