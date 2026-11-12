from skill_gap import pdf_extractor


class FakePage:
    def __init__(self, text):
        self.text = text

    def extract_text(self):
        return self.text


class FakePDF:
    pages = [FakePage("Python"), FakePage(None), FakePage("SQL")]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


def test_extract_joins_pages(monkeypatch):
    monkeypatch.setattr(pdf_extractor.pdfplumber, "open", lambda path: FakePDF())
    assert pdf_extractor.extract_text_from_pdf("fake.pdf") == "Python\nSQL"
