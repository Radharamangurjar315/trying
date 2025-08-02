import requests
import pdfplumber
from io import BytesIO
from docx import Document
import email
from typing import Optional

def download_file(url: str) -> bytes:
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    text = ""
    doc = Document(BytesIO(file_bytes))
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_email(file_bytes: bytes) -> str:
    msg = email.message_from_bytes(file_bytes)
    text = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                text += part.get_payload(decode=True).decode(errors="ignore") + "\n"
    else:
        text = msg.get_payload(decode=True).decode(errors="ignore")
    return text

def extract_text(file_bytes: bytes, file_type: Optional[str] = None) -> str:
    if not file_type:
        # Simple heuristic based on bytes signature
        if file_bytes.startswith(b"%PDF"):
            file_type = "pdf"
        elif file_bytes[0:2] == b'PK':  # docx files are zip archives starting with PK
            file_type = "docx"
        else:
            file_type = "email"

    if file_type == "pdf":
        return extract_text_from_pdf(file_bytes)
    elif file_type == "docx":
        return extract_text_from_docx(file_bytes)
    elif file_type == "email":
        return extract_text_from_email(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
