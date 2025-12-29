from docx import Document
import PyPDF2

def read_docx(path):
    try:
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        print(f"⚠️ Skipping DOCX (error): {path}")
        return ""

def read_pdf(path):
    try:
        text = ""
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"⚠️ Skipping PDF (error): {path}")
        return ""

def read_file(path):
    if path.lower().endswith(".docx"):
        return read_docx(path)
    elif path.lower().endswith(".pdf"):
        return read_pdf(path)
    else:
        return ""
