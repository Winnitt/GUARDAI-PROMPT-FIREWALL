import base64
import re
import io
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Extracts raw text from uploaded files (PDF, HTML, TXT)."""
    if filename.endswith(".pdf"):
        pdf = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
        return text
    elif filename.endswith(".html") or filename.endswith(".htm"):
        soup = BeautifulSoup(file_bytes, "html.parser")
        return soup.get_text()
    else:
        return file_bytes.decode("utf-8", errors="ignore")

def decode_obfuscated_payloads(text: str) -> str:
    """Decodes base64 strings embedded in the input."""
    b64_matches = re.findall(r'[A-Za-z0-9+/]{20,}==?', text)
    augmented_text = text
    for match in b64_matches:
        try:
            decoded = base64.b64decode(match).decode("utf-8", errors="ignore")
            augmented_text += f"\n[Decoded Base64 Content]: {decoded}"
        except Exception:
            pass
    return augmented_text