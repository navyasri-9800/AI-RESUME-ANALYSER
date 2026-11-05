try:
    import pymupdf
except ImportError:
    import fitz as pymupdf
from docx import Document


def extract_pdf_text(file_path):
    try:
        document = pymupdf.open(file_path)
        text = ""
        for page in document:
            text += page.get_text()
        document.close()
        return text
    except Exception:
        return ""


def extract_docx_text(file_path):
    try:
        document = Document(file_path)
        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )
        return text
    except Exception:
        return ""


def extract_text(file_path):

    if file_path.lower().endswith('.pdf'):

        return extract_pdf_text(file_path)

    elif file_path.lower().endswith('.docx'):

        return extract_docx_text(file_path)

    return ""