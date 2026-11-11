import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts plain text from all pages of a PDF resume.
    Returns a single consolidated string.
    """
    extracted_text = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)
                
    return "\n".join(extracted_text)