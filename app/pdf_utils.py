import fitz  # PyMuPDF
import re

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    # Remove cid artifacts like (cid:2)
    text = re.sub(r'\(cid:\d+\)', '', text)

    # Replace weird characters with spaces
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', ' ', text)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()
