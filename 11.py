import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

# Load the image
img = cv2.imread("image.jpg")

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding to the image
thresholded = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 2)

# Decode QR codes in the image
codes = pyzbar.decode(thresholded)

# Print the decoded QR codes
for code in codes:
    (x, y, w, h) = code.rect
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    print("QR Code: ", code.data)

# Show the image with the QR codes detected
cv2.imshow("QR Codes", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
