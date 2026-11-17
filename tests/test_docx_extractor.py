from skill_gap import docx_extractor


class FakeParagraph:
    def __init__(self, text):
        self.text = text


class FakeDocument:
    paragraphs = [FakeParagraph("Python"), FakeParagraph(""), FakeParagraph("SQL")]


def test_extract_skips_empty_paragraphs(monkeypatch):
    monkeypatch.setattr(docx_extractor.docx, "Document", lambda path: FakeDocument())
    assert docx_extractor.extract_text_from_docx("fake.docx") == "Python\nSQL"


class FakeTc:
    pass


class FakeCell:
    def __init__(self, tc, texts):
        self._tc = tc
        self.paragraphs = [FakeParagraph(t) for t in texts]


class FakeRow:
    def __init__(self, cells):
        self.cells = cells


class FakeTable:
    def __init__(self, rows):
        self.rows = rows


class FakeDocumentWithTable:
    paragraphs = [FakeParagraph("Skills")]
    merged = FakeTc()
    tables = [
        FakeTable(
            [
                FakeRow([FakeCell(FakeTc(), ["Git"]), FakeCell(FakeTc(), ["Docker", ""])]),
                # One merged cell spanning two columns appears twice in row.cells.
                FakeRow([FakeCell(merged, ["Linux"]), FakeCell(merged, ["Linux"])]),
            ]
        )
    ]


def test_extract_includes_table_text_once(monkeypatch):
    monkeypatch.setattr(
        docx_extractor.docx, "Document", lambda path: FakeDocumentWithTable()
    )
    result = docx_extractor.extract_text_from_docx("fake.docx")
    assert result == "Skills\nGit\nDocker\nLinux"


def test_extract_real_docx_file(tmp_path):
    path = tmp_path / "resume.docx"
    document = docx_extractor.docx.Document()
    document.add_paragraph("Python")
    document.add_paragraph("")
    document.add_paragraph("SQL")
    document.save(path)
    assert docx_extractor.extract_text_from_docx(str(path)) == "Python\nSQL"
