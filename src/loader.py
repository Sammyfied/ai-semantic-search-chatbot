from pypdf import PdfReader
import re

def load_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def chunk_text(text, chunk_size=200, overlap=30):
    # First try to split by section headers (lines with dashes underneath)
    section_pattern = r'(?=\n[A-Z][A-Z\s&]+\n[-=]+)'
    sections = re.split(section_pattern, text)
    
    chunks = []
    for section in sections:
        section = section.strip()
        if not section:
            continue
        words = section.split()
        if len(words) <= chunk_size:
            # Small enough — keep as one chunk
            chunks.append(section)
        else:
            # Too big — split with overlap
            i = 0
            while i < len(words):
                chunk = " ".join(words[i:i + chunk_size])
                chunks.append(chunk)
                i += chunk_size - overlap

    # Fallback if no sections found
    if len(chunks) <= 1:
        words = text.split()
        chunks = []
        i = 0
        while i < len(words):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            i += chunk_size - overlap

    return [c for c in chunks if len(c.strip()) > 20]
