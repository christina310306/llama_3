import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import cv2
import numpy as np
from certificate_verifier import verify_certificate_text

# ---------------- CONFIG ----------------
NOTES_PATH = r"C:\Users\chris\OneDrive\NOTES"

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# ---------------- OCR HELPERS ----------------
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    _, gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return gray


def ocr_image_file(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return ""
    processed = preprocess_image(img)
    return pytesseract.image_to_string(processed, config="--psm 6")


def ocr_pdf_file(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)

    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_np = np.array(img)
        processed = preprocess_image(img_np)
        text += pytesseract.image_to_string(processed, config="--psm 6")

    return text
def looks_like_certificate(text):
    if not text or len(text) < 200:
        return False

    text = text.lower()

    keywords = [
        "certificate",
        "certify",
        "certified",
        "this is to certify",
        "successfully completed",
        "course",
        "award",
        "issued on",
        "date"
    ]

    matches = sum(1 for k in keywords if k in text)

    # Require at least 2 strong signals
    return matches >= 2



# ---------------- MAIN LOGIC ----------------
def extract_certificates_from_notes(notes_path):
    certificates = []

    for root, _, files in os.walk(notes_path):
        for file in files:
            path = os.path.join(root, file)

            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                ocr_text = ocr_image_file(path)

            elif file.lower().endswith(".pdf"):
                ocr_text = ocr_pdf_file(path)

            else:
                continue

            if not looks_like_certificate(ocr_text):
                continue

            result = verify_certificate_text(ocr_text)
            certificates.append({
                "file": file,
                "text": ocr_text,
                "verification": result
            })

    return certificates


        
        