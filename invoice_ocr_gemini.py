# invoice_ocr_gemini_pro.py

import paddleocr
import re
from dotenv import load_dotenv
import os
import google.generativeai as genai
import pathlib
import textwrap
from IPython.display import display
from IPython.display import Markdown

load_dotenv()  # take environment variables from .env.

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def process_text_and_fill_ui(image_data):
    try:
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content(
            ["Extract from this invoice Name of vendor, vendor VAT id, Date, Total Amount, and VAT Amount , and format the extracted information as a dictionary with keys: vendor_name vendor_vat_id date invoice_total and vat_amount and dont give me any instructions or text just the dictionary only also dont give me dum data.", image_data])
        to_markdown(response.text)
        print(response.text)
        pattern = r'{.*?}'
        match = re.search(pattern, response.text, re.DOTALL)
        if match:
            print(match)
            dictionary_text = match.group()
            parsed_data = eval(dictionary_text)
            # print(parsed_data)
            return parsed_data
        else:
            print("No dictionary found in the gemini output.")
            return None
    except Exception as e:
        print(f"Error during gemini processing: {e}")
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
