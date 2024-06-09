import cv2
import os
from PyQt6 import QtCore
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QProgressDialog, QApplication
import pytesseract
import numpy as np
import re


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
                image = cv2.imread(file_path)
                if image is None:
                    raise ValueError(f"File {file_name} is not a valid image.")

                # Get the orientation details using pytesseract
                osd_data = pytesseract.image_to_osd(image)
                angle = int(re.search('(?<=Rotate: )\d+', osd_data).group(0))

                # Rotate the image to the correct orientation
                rotated = self.rotate_image(image, angle)

                # Save the corrected image back to the file
                cv2.imwrite(file_path, rotated)

                # Update progress
                processed_files += 1
                self.progress_updated.emit(processed_files, total_files)
                progress_dialog.setValue(processed_files)

            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

        # Close the progress dialog after processing all images
        progress_dialog.close()

    def rotate_image(self, image, angle):
        """
        Rotate the image to the correct orientation.
        """
        if angle == 0:
            return image
        elif angle == 90:
            return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif angle == 180:
            return cv2.rotate(image, cv2.ROTATE_180)
        elif angle == 270:
            return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        else:
            return image  # Return original image if angle is not recognized


def update_progress_dialog(processed_files, total_files):
    percentage = (processed_files / total_files) * 100
    print(f"Progress: {percentage:.2f}% - Processed Files: {processed_files}/{total_files}")


# Example usage
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    print("Don't use the module directly.")

    sys.exit(app.exec())
