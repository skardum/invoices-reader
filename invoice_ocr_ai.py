# invoice_ocr_ai.py

import paddleocr
import ollama
import re


def ocr_and_ai_extraction(image_path):
    try:
        # Initialize OCR for Arabic language
        ocr_arabic = paddleocr.PaddleOCR(use_angle_cls=False, lang='ar')
        # Initialize OCR for English language
        ocr_english = paddleocr.PaddleOCR(use_angle_cls=False, lang='en')

        results_arabic = ocr_arabic.ocr(image_path)
        results_english = ocr_english.ocr(image_path)

        extracted_text = ""

        # Merge Arabic and English results
        for results in [results_arabic, results_english]:
            for result in results:
                for line in result:
                    # Extract text content from the tuple
                    extracted_text += line[1][0] + " "
                extracted_text += "\n"  # Add newline after each detected text

        print(extracted_text)
        return extracted_text
    except Exception as e:
        print(f"Error during OCR and AI extraction: {e}")
        return None


def process_text_and_fill_ui(extracted_text):
    try:
        response = ollama.chat(model='stablelm-zephyr', messages=[
            {
                'role': 'user',
                f'content': '{extracted_text}\nExtract from this ocr extracted text Name of vendor, vendor VAT id, Date, Total Amount, and VAT Amount from this invoice, and format the extracted information as a dictionary with keys: "vendor_name" "vendor_vat_id" "date" "invoice_total" and "vat_amount" and dont give me any instructions or text just the dictionary only also dont give me dum data.',
            },
        ])

        print(response['message']['content'])
        pattern = r'{.*?}'
        match = re.search(pattern, response['message']['content'], re.DOTALL)
        if match:
            print(match)
            dictionary_text = match.group()
            # Parse the dictionary text into a Python dictionary
            parsed_data = eval(dictionary_text)
            print(parsed_data)
            return parsed_data
        else:
            print("No dictionary found in the ollama output.")
            return None

    except Exception as e:
        print(f"Error during Ollama processing: {e}")
        return None


def update_ui_with_data(ui, data):
    ui.vendor_lineedit.setText(data.get('vendor_name', ''))
    ui.vatid_lineedit.setText(data.get('vendor_vat_id', ''))
    ui.date_lineedit.setText(data.get('date', ''))

    # Convert float to string before setting the text
    invoice_total = str(data.get('invoice_total', ''))
    ui.total_lineedit.setText(invoice_total)

    # Convert float to string before setting the text
    vat_amount = str(data.get('vat_amount', ''))
    ui.vatamount_lineedit.setText(vat_amount)
