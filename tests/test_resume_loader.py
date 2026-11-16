import pytest
from skill_gap.resume_loader import load_resume, ResumeError

def test_file_not_found():
    with pytest.raises(ResumeError, match="File not found."):
        load_resume("non_existent_file.pdf")

def test_empty_file(tmp_path):
    empty_file = tmp_path / "empty.pdf"
    empty_file.write_text("")
    with pytest.raises(ResumeError, match="The file is empty."):
        load_resume(str(empty_file))

def test_unsupported_file_format(tmp_path):
    txt_file = tmp_path / "resume.txt"
    txt_file.write_text("Some text")
    with pytest.raises(ResumeError, match="Please upload a PDF or DOCX file."):
        load_resume(str(txt_file))

def test_scanned_pdf_empty_text(tmp_path, monkeypatch):
    pdf_file = tmp_path / "scanned.pdf"
    pdf_file.write_text("dummy content")
    
    monkeypatch.setattr("skill_gap.resume_loader.extract_text_from_pdf", lambda path: "")
    
    with pytest.raises(ResumeError, match="No text found. This may be a scanned PDF."):
        load_resume(str(pdf_file))

def test_successful_pdf_load(tmp_path, monkeypatch):
    pdf_file = tmp_path / "resume.pdf"
    pdf_file.write_text("dummy content")
    
    monkeypatch.setattr("skill_gap.resume_loader.extract_text_from_pdf", lambda path: "Python Developer")
    
    text = load_resume(str(pdf_file))
    assert text == "Python Developer"