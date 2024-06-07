# invoices reader

This Python application provides a graphical user interface (GUI) built using PyQt5 for processing a folder of invoice images. It enables users to extract essential invoice details including invoice number, date, vendor name, vendor VAT ID, invoice total, and invoice VAT amount. The extracted data is then exported to a specified Excel file.

## Features:
- User-Friendly Interface: Easy-to-navigate GUI for selecting folders and specifying file paths.
- Batch Processing: Processes all invoice images within a selected folder.
- Detailed Extraction: Extracts and organizes key invoice information.
- Excel Export: Saves the extracted invoice details in a structured Excel file.
- Decode QR codes from invoice images.
- Extract information using Gemini AI if QR code decoding fails.

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
$ cd invoices-reader

```

Install the required packages

```
$ pip install -r requirements.txt
```

## Obtain API keys for Gemini AI, and store them in a `.env` file:

https://aistudio.google.com/app/apikey

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
4. If QR code decoding fails for an invoice, press ai extract to extract information using Gemini AI.
5. Once processing is complete, the extracted data will be saved to the specified Excel file.

## Contributions

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Test your changes thoroughly.
5. Commit your changes and push to your fork.
6. Create a pull request.
