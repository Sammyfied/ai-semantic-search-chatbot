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
    # Split on known section headers from the document
    section_headers = [
        "Personal Information",
        "Professional Summary",
        "Work Experience",
        "Education",
        "Technical Skills",
        "Projects",
        "Achievements & Awards",
        "Certifications",
        "Open Source Contributions",
        "Languages",
        "Interests & Hobbies",
        "References"
    ]

    # Build regex pattern from headers
    pattern = '(' + '|'.join(re.escape(h) for h in section_headers) + ')'
    parts = re.split(pattern, text)

    # Pair each header with its content
    chunks = []
    i = 0
    while i < len(parts):
        part = parts[i].strip()
        if part in section_headers:
            # Combine header with its content
            content = parts[i + 1].strip() if i + 1 < len(parts) else ""
            combined = part + "\n" + content
            # If combined is too long, split further
            words = combined.split()
            if len(words) <= chunk_size:
                chunks.append(combined)
            else:
                j = 0
                while j < len(words):
                    chunk = " ".join(words[j:j + chunk_size])
                    chunks.append(chunk)
                    j += chunk_size - overlap
            i += 2
        else:
            if part:
                chunks.append(part)
            i += 1

    # Fallback
    if len(chunks) <= 1:
        words = text.split()
        chunks = []
        i = 0
        while i < len(words):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            i += chunk_size - overlap

    return [c for c in chunks if len(c.strip()) > 20]
