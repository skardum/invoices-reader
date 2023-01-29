import cv2
import numpy as np
import base64
import os
import xlwt
import pyzbar.pyzbar as pyzbar


def preprocess_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to improve image quality
    thresholded = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 2)

    return thresholded


def decode_qr_code(image):
    # Preprocess the image
    preprocessed_image = preprocess_image(image)

    # Create a QR code detector
    qr_detections = pyzbar.decode(preprocessed_image)

    # Loop through the QR code detections
    for detection in qr_detections:
        # Get the QR code data
        data = detection.data
        text = base64.b64decode(data).decode("utf-8")
        if text:
            return text

    return None


# Iterate through all the image files in a folder
folder_path = r'New folder'

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

        # Load the image
        image = cv2.imread(file_path)

        # Detect QR code in the image
        data = decode_qr_code(image)

        if data:
            print("QR code data:", data)
            # Write the data to the Excel sheet
            sheet.write(row_num, 0, file_path)
            sheet.write(row_num, 1, data)
            row_num += 1
        else:
            # Rotate the image and try again
            for angle in [90, 180, 270]:
                image_rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
                data = decode_qr_code(image_rotated)
                if data:
                    print("QR code data (rotated {} degrees):".format(angle), data)
                    # Write the data to the Excel sheet
                    sheet.write(row_num, 0, file_path)
                    sheet.write(row_num, 1, data)
                    row_num += 1
                    break
            else:
                # Write the file name to the Excel sheet (no QR code detected)
                sheet.write(row_num, 0, file_path)
                row_num += 1

# Save the Excel file
workbook.save("qr_code_data.xls")
