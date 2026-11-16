import os
from skill_gap.pdf_extractor import extract_text_from_pdf

class ResumeError(Exception):
    """Custom exception for resume validation and loading errors."""
    pass

def load_resume(path: str) -> str:
    """Load and extract text from a resume file with rigorous input checks."""
    if not os.path.exists(path):
        raise ResumeError("File not found.")
    
    if os.path.getsize(path) == 0:
        raise ResumeError("The file is empty.")
    
    ext = os.path.splitext(path)[1].lower()
    
    if ext == ".pdf":
        text = extract_text_from_pdf(path)
    elif ext == ".docx":
        from skill_gap.docx_extractor import extract_text_from_docx
        text = extract_text_from_docx(path)
    else:
        raise ResumeError("Please upload a PDF or DOCX file.")
    
    if not text or not text.strip():
        raise ResumeError("No text found. This may be a scanned PDF.")
    
    return text