import pdfplumber

def extract_text_from_pdf(pdf_file):
    """Extracts text from the uploaded PDF file object."""
    text = ""
    
    # Open the uploaded file using pdfplumber
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"

    return text
