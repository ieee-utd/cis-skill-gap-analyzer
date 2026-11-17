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

def test_corrupted_pdf_raises_resume_error(tmp_path, monkeypatch):
    """Test that unexpected extractor crashes turn into a clear ResumeError."""
    fake_pdf = tmp_path / "fake.pdf"
    fake_pdf.write_text("not a real pdf")
    
    def mock_bad_extractor(path):
        raise Exception("PdfminerException: Invalid PDF structure")
        
    monkeypatch.setattr("skill_gap.resume_loader.extract_text_from_pdf", mock_bad_extractor)
    
    with pytest.raises(ResumeError, match="Failed to parse resume file"):
        load_resume(str(fake_pdf))

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
    monkeypatch.setattr("skill_gap.resume_loader.clean_text", lambda t: t) # Mock clean_text if needed
    
    text = load_resume(str(pdf_file))
    assert text == "Python Developer"

def test_real_docx_load(tmp_path, monkeypatch):
    """Test loading a real/mocked docx file integration."""
    docx_file = tmp_path / "resume.docx"
    docx_file.write_text("dummy docx content")
    
    monkeypatch.setattr("skill_gap.docx_extractor.extract_text_from_docx", lambda path: "Software Engineer Java")
    monkeypatch.setattr("skill_gap.resume_loader.clean_text", lambda t: t)
    
    text = load_resume(str(docx_file))
    assert text == "Software Engineer Java"