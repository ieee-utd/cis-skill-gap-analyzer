import docx


def extract_text_from_docx(docx_path: str) -> str:
    """
    Extracts plain text from a DOCX resume.

    In: the path to a .docx file.
    Out: one string with every non-empty paragraph on its own line, followed by
    the text inside any tables (many resumes put skills or columns in tables).
    """
    document = docx.Document(docx_path)

    lines = [p.text for p in document.paragraphs if p.text.strip()]

    # Resumes often keep skills or a two-column layout inside tables.
    for table in getattr(document, "tables", []):
        for row in table.rows:
            seen = set()
            for cell in row.cells:
                # A merged cell shows up once per column it spans; keep it once.
                if id(cell._tc) in seen:
                    continue
                seen.add(id(cell._tc))
                lines.extend(p.text for p in cell.paragraphs if p.text.strip())

    return "\n".join(lines)
