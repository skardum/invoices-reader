# QR Code Detector

a Python application for detecting QR codes in an image of invoices that made according to zatca. It provides a graphical user interface (GUI) built using PyQt5, allowing users to select a folder containing images with QR codes and specify an Excel file location to save the decoded data.

## Features:

- **QR Code Detection** : Utilizes OpenCV and pyzbar to detect QR codes from images.
- **Graphical User Interface** : Built with PyQt5 for easy interaction.
- **Excel Export** : Saves decoded QR code data to an Excel file for further analysis.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

- Python 3.x
- OpenCV
- Numpy
- Pyzbar

## Installing

Clone the repository

```
$ git clone https://github.com/mohammednabarawy/qr-detector.git
```

Navigate to the project directory

```
$ cd qr-detector

```

Install the required packages

```
$ pip install -r requirements.txt
```

## Running the Application

To run the application, simply run the following command:

```
$ python main.py
```

## Built With

- OpenCV - A computer vision and machine learning software library.
- Numpy - A library for the Python programming language, adding support for large, multi-dimensional arrays and matrices.
- Pyzbar - A library for reading barcodes and QR codes.

## Contributions

Contributions are welcome! If you have any suggestions or improvements, feel free to submit a pull request.
