import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QDialog, QTableWidgetItem, QMessageBox, QFileDialog
from PyQt6.uic import loadUi
from datetime import datetime
import xlsxwriter
import logging

# Set up logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)


class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, db_file):
        try:
            self.connection = sqlite3.connect(db_file)
            self.cursor = self.connection.cursor()
            logging.info("Connected to database successfully.")
        except sqlite3.Error as e:
            logging.error("Error connecting to database: %s" % e)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            logging.info("Disconnected from database.")

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logging.error("Error executing query: %s" % e)
            return False

    def fetch_all(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error("Error fetching data: %s" % e)
            return None

    def fetch_one(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logging.error("Error fetching data: %s" % e)
            return None


class DatabaseDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('db.ui', self)  # Load the UI file
        self.setWindowTitle("Database Viewer")
        self.db_manager = DatabaseManager()
        self.db_manager.connect("detections.db")  # Use the function directly
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
            self.db_manager.execute_query("""
                CREATE TABLE IF NOT EXISTS main_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    detection_date TEXT,
                    num_invoices INTEGER
                )
            """)
            self.db_manager.execute_query("""
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
        except sqlite3.Error as e:
            QMessageBox.critical(
                self, 'Database Error', f'Failed to create tables: {str(e)}')

    def load_main_records(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        main_records = self.db_manager.fetch_all("SELECT * FROM main_records")
        if main_records:
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

                    detected_data = self.db_manager.fetch_all(
                        "SELECT * FROM extracted_data WHERE id=?", (detection_id,))
                    if detected_data:
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
                    self.db_manager.execute_query(
                        "DELETE FROM main_records WHERE id=?", (detection_id,))
                    self.db_manager.execute_query(
                        "DELETE FROM extracted_data WHERE id=?", (detection_id,))
                    self.load_main_records()
                    QMessageBox.information(
                        self, 'Deletion Successful', 'Detection deleted successfully!')
                except sqlite3.Error as e:
                    QMessageBox.warning(
                        self, 'Deletion Failed', f'Failed to delete detection: {str(e)}')
        else:
            QMessageBox.warning(
                self, 'No Selection', 'Please select a detection to delete!')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = DatabaseDialog()
    dialog.exec()
