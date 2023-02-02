import os
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

# Folder containing the images
folder = r'C:\Users\moham\desktop\New folder (2)'

# Subfolder to save the cropped images
save_folder = os.path.join(folder, "cropped_images")

# Create the subfolder if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Iterate through the images in the folder
for filename in os.listdir(folder):
    # Load image
    img = cv2.imread(os.path.join(folder, filename))

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect QR code
    qr_code = pyzbar.decode(gray)

    # Check if a QR code was detected
    if len(qr_code) > 0:
        # Get the coordinates of the QR code
        x, y, w, h = qr_code[0].rect

        # Crop the image to QR code only
        cropped = gray[y:y+h, x:x+w]

        # Save the cropped image
        cv2.imwrite(os.path.join(save_folder, filename), cropped)
    else:
        # Save the original image
        cv2.imwrite(os.path.join(save_folder, filename), img)
        print("No QR code detected in image:", filename)
