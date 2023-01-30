import cv2
import base64
import os
import xlwt
import pyzbar.pyzbar as pyzbar


def extract_data(text):
    # Define the format of the data to be extracted
    data_format = "☺{}☻{}♥¶{}Z♦♠{}♣♣{}"
    try:
        company, vat, date, invoice, vat_amt = data_format.format(
            *text.split(" "))
    except:
        return None, None, None, None, None
    return company, vat, date, invoice, vat_amt


def decode_qr(image):
    qr_codes = pyzbar.decode(image)
    for qr in qr_codes:
        data = qr.data
        text = base64.b64decode(data).decode("utf-8")
        if text:
            return text
    return None


folder_path = r'New folder'
workbook = xlwt.Workbook()
sheet = workbook.add_sheet("QR code data")
sheet.write(0, 0, "Image File")
sheet.write(0, 1, "Company Name")
sheet.write(0, 2, "VAT Number")
sheet.write(0, 3, "Date")
sheet.write(0, 4, "Invoice Amount")
sheet.write(0, 5, "VAT Amount")
row_num = 1

for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)
    if os.path.isfile(file_path):
        image = cv2.imread(file_path)
        data = decode_qr(image)
        if data:
            company, vat, date, invoice, vat_amt = extract_data(data)
            sheet.write(row_num, 0, file_path)
            sheet.write(row_num, 1, company)
            sheet.write(row_num, 2, vat)
            sheet.write(row_num, 3, date)
            sheet.write(row_num, 4, invoice)
            sheet.write(row_num, 5, vat_amt)
            row_num += 1
        else:
            sheet.write(row_num, 0, file_path)
            row_num += 1

workbook.save("qr_code_data.xls")
