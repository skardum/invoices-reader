import cv2
import numpy as np
import base64
import os
import xlwt


def decode_qr_code(image_path):
    # Load the image and convert it to grayscale
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Create a QR code detector
    qr_detector = cv2.QRCodeDetector()

    # Detect QR code in the image
    data, points, _ = qr_detector.detectAndDecode(gray)
    data = data.encode('utf-8')
    text = base64.b64decode(data).decode("utf-8")

    if text:
        return text
    else:
        return None


# Iterate through all the image files in a folder
folder_path = r'C:\Users\aghna\Desktop\New folder'

# Create a new Excel file
workbook = xlwt.Workbook()
sheet = workbook.add_sheet("QR code data")

# Write the header row
sheet.write(0, 0, "Image File")
sheet.write(0, 1, "QR code data")

# Keep track of the row number
row_num = 1

for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path):
        print("Processing:", file_path)
        data = decode_qr_code(file_path)
        if data:
            print("QR code data:", data)
            # Write the data to the Excel sheet
            sheet.write(row_num, 0, file_path)
            sheet.write(row_num, 1, data)
            row_num += 1

# Save the Excel file
workbook.save("qr_code_data.xls")
