import re

REQUIRED_FIELDS = {
    "platform": ["nptel", "swayam"],
    "certificate_phrase": ["successfully completed", "this is to certify"],
    "date": [r"\b(20\d{2})\b"],
}

def verify_certificate_text(ocr_text):
    text = ocr_text.lower()
    found = {}

    for field, patterns in REQUIRED_FIELDS.items():
        found[field] = any(
            re.search(p, text) for p in patterns
        )

    score = sum(found.values())
    return {
        "found_fields": found,
        "score": score,
        "is_valid": score >= 2
    }
