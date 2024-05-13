import paddleocr
import cv2
import spacy
from spacy.lang.en import English
from spacy.lang.ar import Arabic
from spacy.pipeline import EntityRuler
# from gliner_spacy.pipeline import GlinerSpacy


def ocr_text(image):
    try:
        # Initialize OCR for Arabic language
        ocr_arabic = paddleocr.PaddleOCR(use_angle_cls=False, lang='ar')
        # Initialize OCR for English language
        ocr_english = paddleocr.PaddleOCR(use_angle_cls=False, lang='en')
        results_arabic = ocr_arabic.ocr(image)
        results_english = ocr_english.ocr(image)
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
        print(f"Error during ocr processing: {e}")
        return None


def glinertext(text):
    nlp = spacy.load("en_core_web_lg")
    # nlp.add_pipe("gliner_spacy", config={"labels": ["vendor name", "vat id", "invoice date", "invoice number", "vat amount", "invoice total amount"]})
    doc = nlp(text)
    for ent in doc.ents:
        print(ent.text, ent.label_)
        return ent.text, ent.label_


def update_ui_with_ocrdata(ui, data):
    ui.vendor_lineedit.setText(data.get('vendor_name', ''))
    ui.vatid_lineedit.setText(data.get('vat_id', ''))
    ui.date_lineedit.setText(data.get('date', ''))

    # Convert float to string before setting the text
    invoice_total = str(data.get('invoice_total', ''))
    ui.total_lineedit.setText(invoice_total)

    # Convert float to string before setting the text
    vat_total = str(data.get('vat_total', ''))
    ui.vatamount_lineedit.setText(vat_total)
    invoice_number = str(data.get('invoice_number', ''))
    ui.invoicenumber_lineedit.setText(invoice_number)
