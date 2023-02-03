import cv2
import os
import xlwt
import pyzbar.pyzbar as pyzbar
import base64
import string


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
    # print(result2)
    return result2


def decode_qr_code(image):
    # Preprocess the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    threshold = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 2)
    # Detect QR codes
    qr_detections = pyzbar.decode(threshold)
    for detection in qr_detections:
        # Get the QR code data
        data = detection.data
        try:
            text = base64.b64decode(data).decode("utf-8")
            print(text)
            return text, threshold
        except:
            print("An exception occurred")
            return None, threshold

    return None, threshold
