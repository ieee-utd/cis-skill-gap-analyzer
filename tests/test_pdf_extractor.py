import pytest
from skill_gap.pdf_extractor import extract_text_from_pdf

def test_pdf_extraction_import():
    """Simple test to verify module import and function structure."""
    assert callable(extract_text_from_pdf)