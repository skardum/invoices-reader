import paddleocr
import google.generativeai as genai
import re


def ocr_text(image):
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


def extract_with_gemini(text):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(['''Extract the following fields from this invoice ocr result and format the information as a dictionary:
                                           - Vendor Name
                                           - Vendor VAT ID
                                           - Date
                                           - Total Amount
                                           - VAT Amount
                                           - invoice number

                                           Please provide the extracted information in the format:
                                           {
                                               'vendor_name': '...',
                                               'vat_id': '...',
                                               'date': '...',
                                               'invoice_total': '...',
                                               'vat_total': '...',
                                               'invoice_number': '...'
                                           }''',
                                           text
                                           ])

        print(response.text)
        pattern = r'{.*?}'
        match = re.search(pattern, response.text, re.DOTALL)
        if match:
            print(match)
            dictionary_text = match.group()
            parsed_data = eval(dictionary_text)
            return parsed_data
        else:
            print("No dictionary found in the gemini output.")
            return {
                'vendor_name': '...',
                'vat_id': '...',
                'date': '...',
                'invoice_total': '...',
                'vat_total': '...',
                'invoice_number': '...'
            }
    except Exception as e:
        print(f"Error during gemini processing: {e}")
        return {
            'vendor_name': '...',
            'vat_id': '...',
            'date': '...',
            'invoice_total': '...',
            'vat_total': '...',
            'invoice_number': '...'
        }


def update_ui_with_ocrdata(ui, data):
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
