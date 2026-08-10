import fitz  # PyMuPDF
from docx import Document


def extract_pdf_text(filepath):
    text = ""

    try:
        pdf = fitz.open(filepath)

        for page in pdf:
            text += page.get_text()

        pdf.close()

    except Exception as e:
        print("PDF Error:", e)

    return text


def extract_docx_text(filepath):

    text = ""

    try:
        document = Document(filepath)

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

    except Exception as e:
        print("DOCX Error:", e)

    return text


def extract_resume_text(filepath):

    if filepath.endswith(".pdf"):
        return extract_pdf_text(filepath)

    elif filepath.endswith(".docx"):
        return extract_docx_text(filepath)

    return ""