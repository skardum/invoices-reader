# invoice_ocr_ai.py

import paddleocr
import ollama
import re


def ocr_for_ollama(image):
    try:
        # Initialize OCR for English language with Robust-scene-rec_mv3_db model
        ocr_english = paddleocr.PaddleOCR(use_angle_cls=False, lang='en', det_model_dir='Robust-scene-rec_mv3_db')
        # Initialize OCR for Arabic language with ch_ppocr_server_v2.0_rec_mv3_crnn_enhance model
        ocr_arabic = paddleocr.PaddleOCR(use_angle_cls=False, lang='ar', rec_model_dir='ch_ppocr_server_v2.0_rec_mv3_crnn_enhance')

        results_english = ocr_english.ocr(image)
        results_arabic = ocr_arabic.ocr(image)

        extracted_text = ""

        # Merge English results
        for result in results_english:
            for line in result:
                extracted_text += line[1][0] + " "
            extracted_text += "\n"

        # Merge Arabic results
        for result in results_arabic:
            for line in result:
                extracted_text += line[1][0] + " "
            extracted_text += "\n"

        print(extracted_text)

        return extracted_text
    except Exception as e:
        print(f"Error during OCR processing: {e}")
        return None


def process_ollama_and_fill_ui(extracted_text):
    try:
        response = ollama.chat(model='stablelm-zephyr', messages=[
            {
                'role': 'user',
                'content': f'{extracted_text}\nExtract the following fields from this invoice OCR result and format the information as a dictionary:\n'
                           '- Vendor Name\n'
                           '- Vendor VAT ID\n'
                           '- Date\n'
                           '- Total Amount\n'
                           '- VAT Amount\n'
                           '- Invoice Number\n'
                           '\n'
                           'Please provide the extracted information in the format:\n'
                           '{\n'
                           "    'vendor_name': '...',\n"
                           "    'vat_id': '...',\n"
                           "    'date': '...',\n"
                           "    'invoice_total': '...',\n"
                           "    'vat_total': '...',\n"
                           "    'invoice_number': '...'\n"
                           '}'
            },
        ])

        print(response['message']['content'])

        response_content = response['message']['content']
        dictionary_text = re.search(r'\{.*\}', response_content, re.DOTALL).group()

        parsed_data = eval(dictionary_text)

        print(parsed_data)
        return parsed_data

    except Exception as e:
        print(f"Error during Ollama processing: {e}")
        # Return default dictionary in case of an error
        return {
            'vendor_name': '...',
            'vat_id': '...',
            'date': '...',
            'invoice_total': '...',
            'vat_total': '...',
            'invoice_number': '...'
        }


def update_ui_with_ollama_data(ui, data):
    print("Vendor Line Edit Text:", ui.vendor_lineedit.text())
    if ui.vendor_lineedit.text() == "qr not detected":
        print("Updating Vendor Name:", data.get('vendor_name', ''))
        ui.vendor_lineedit.setText(data.get('vendor_name', ''))

    print("VAT ID Line Edit Text:", ui.vatid_lineedit.text())
    if ui.vatid_lineedit.text() == "0":
        print("Updating VAT ID:", data.get('vat_id', ''))
        ui.vatid_lineedit.setText(data.get('vat_id', ''))

    print("Date Line Edit Text:", ui.date_lineedit.text())
    if ui.date_lineedit.text() == "0":
        print("Updating Date:", data.get('date', ''))
        ui.date_lineedit.setText(data.get('date', ''))

    # Convert float to string before setting the text
    invoice_total = str(data.get('invoice_total', ''))
    print("Total Line Edit Text:", ui.total_lineedit.text())
    if ui.total_lineedit.text() == "0.0":
        print("Updating Invoice Total:", invoice_total)
        ui.total_lineedit.setText(invoice_total)

    # Convert float to string before setting the text
    vat_total = str(data.get('vat_total', ''))
    print("VAT Amount Line Edit Text:", ui.vatamount_lineedit.text())
    if ui.vatamount_lineedit.text() == "0.0":
        print("Updating VAT Amount:", vat_total)
        ui.vatamount_lineedit.setText(vat_total)

    invoice_number = str(data.get('invoice_number', ''))
    print("Invoice Number Line Edit Text:", ui.invoicenumber_lineedit.text())
    if ui.invoicenumber_lineedit.text() == "0":
        print("Updating Invoice Number:", invoice_number)
        ui.invoicenumber_lineedit.setText(invoice_number)
