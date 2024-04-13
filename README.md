# invoices reader

This is a Python application for processing invoices it detec QR codes in an image of invoices that made according to zatca.If QR code decoding fails, the application uses the Gemini AI model to extract information from the image. It provides a graphical user interface (GUI) built using PyQt5, allowing users to select a folder containing images with QR codes and specify an Excel file location to save the decoded data.

## Features:

- Decode QR codes from invoice images.
- Extract information using Gemini AI if QR code decoding fails.
- Save extracted data to an Excel spreadsheet.

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
$ git clone https://github.com/mohammednabarawy/invoices-reader.git
```

Navigate to the project directory

```
$ cd qr-detector

```

Install the required packages

```
$ pip install -r requirements.txt
```

## Obtain API keys for Gemini AI, and store them in a `.env` file:

GOOGLE_API_KEY="your_google_api_key"

## Running the Application

To run the application, simply run the following command:

```
$ python main.py
```

- OpenCV - A computer vision and machine learning software library.

## Usage

1. Select a folder containing invoice images.
2. Choose a location to save the extracted data as an Excel spreadsheet.
3. Click the "Start" button to begin processing invoices.
4. If QR code decoding fails for an invoice, the application will attempt to extract information using Gemini AI.
5. Once processing is complete, the extracted data will be saved to the specified Excel file.

## Contributions

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Test your changes thoroughly.
5. Commit your changes and push to your fork.
6. Create a pull request.
