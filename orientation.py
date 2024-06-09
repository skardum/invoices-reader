import os
from PyQt6 import QtCore
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QProgressDialog, QApplication
import pytesseract
from PIL import Image, ImageEnhance
import numpy as np
import re
import cv2


class ImageProcessor(QObject):
    progress_updated = pyqtSignal(int, int)

    def correct_image_orientation(self, folder_path):
        total_files = len(os.listdir(folder_path))
        processed_files = 0

        # Create and show the progress dialog
        progress_dialog = QProgressDialog("Fixing Image Orientation...", None, 0, total_files)
        progress_dialog.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        progress_dialog.setAutoClose(False)  # Keep the dialog open until completion

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            try:
                # Load image using PIL
                image = Image.open(file_path)

                # Enhance the image
                enhanced_image = self.enhance_image(image)

                # Get the orientation details using pytesseract
                osd_data = pytesseract.image_to_osd(enhanced_image)
                angle = int(re.search('(?<=Rotate: )\d+', osd_data).group(0))

                # Rotate the image to the correct orientation
                rotated = enhanced_image.rotate(-angle, expand=True)

                # Crop the image to remove unnecessary borders or margins
                cropped = self.automatic_crop(rotated)

                # Save the corrected image back to the file
                cropped.save(file_path)

                # Update progress
                processed_files += 1
                self.progress_updated.emit(processed_files, total_files)
                progress_dialog.setValue(processed_files)

            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

        # Close the progress dialog after processing all images
        progress_dialog.close()

    def enhance_image(self, image):
        """
        Enhance the image by adjusting contrast.
        """
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        enhanced_image = enhancer.enhance(1.5)  # Increase contrast by 50%

        return enhanced_image

    def automatic_crop(self, image):
        """
        Automatically crop the image to remove unnecessary borders or margins.
        """
        # Convert image to grayscale
        gray_image = np.array(image.convert('L'))

        # Apply binary thresholding
        _, thresholded = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # Find contours
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        print("Number of contours found:", len(contours))  # Debug print

        # Initialize variables to store largest contour and its area
        largest_contour = None
        max_area = 0

        # Find the largest contour
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                largest_contour = contour
                max_area = area

        # If a contour is found, proceed with cropping
        if largest_contour is not None:
            # Get bounding box coordinates
            x, y, w, h = cv2.boundingRect(largest_contour)

            print("Bounding box coordinates:", x, y, w, h)  # Debug print

            # Crop the image using the bounding box
            cropped_image = image.crop((x, y, x + w, y + h))

            # Remove excess whitespace
            cropped_array = np.array(cropped_image)
            rows, cols = np.where(cropped_array < 255)

            if rows.size > 0 and cols.size > 0:
                min_row, max_row = min(rows), max(rows) + 1
                min_col, max_col = min(cols), max(cols) + 1

                # Crop to remove excess whitespace
                cropped_image = cropped_image.crop((min_col, min_row, max_col, max_row))
        else:
            # If no contours found, return the original image
            cropped_image = image

        return cropped_image


def update_progress_dialog(processed_files, total_files):
    percentage = (processed_files / total_files) * 100
    print(f"Progress: {percentage:.2f}% - Processed Files: {processed_files}/{total_files}")


# Example usage
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    print("Don't use the module directly.")

    sys.exit(app.exec())
