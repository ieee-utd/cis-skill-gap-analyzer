import os
from skill_gap.pdf_extractor import extract_text_from_pdf
from skill_gap.text_cleaner import clean_text  # Assuming clean_text is available from Nafeesa's AB#6 / main

class ResumeError(Exception):
    """Custom exception for resume validation and loading errors."""
    pass

def load_resume(path: str) -> str:
    """Load, validate, and clean text from a resume file."""
    if not os.path.exists(path):
        raise ResumeError("File not found.")
    
    if os.path.getsize(path) == 0:
        raise ResumeError("The file is empty.")
    
    ext = os.path.splitext(path)[1].lower()
    
    try:
        if ext == ".pdf":
            text = extract_text_from_pdf(path)
        elif ext == ".docx":
            from skill_gap.docx_extractor import extract_text_from_docx
            text = extract_text_from_docx(path)
        else:
            raise ResumeError("Please upload a PDF or DOCX file.")
    except ResumeError:
        raise
    except Exception as e:
        raise ResumeError(f"Failed to parse resume file: {str(e)}")
    
    if not text or not text.strip():
        raise ResumeError("No text found. This may be a scanned PDF.")
    
    # Clean the text before returning
    return clean_text(text)