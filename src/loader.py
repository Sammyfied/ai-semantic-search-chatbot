from pypdf import PdfReader
import re

def load_pdf(path):
    reader = PdfReader(path)
    pages_text = []
    for page in reader.pages:
        extracted = page.extract_text(extraction_mode="layout")
        if extracted:
            pages_text.append(extracted)
    text = "\n".join(pages_text)
    # Fix words split by newlines (common in PDFs)
    text = re.sub(r'(?<=[a-z,])\n(?=[a-z])', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text

def chunk_text(text, chunk_size=200, overlap=30):
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

    pattern = '(' + '|'.join(re.escape(h) for h in section_headers) + ')'
    parts = re.split(pattern, text)

    chunks = []
    i = 0
    while i < len(parts):
        part = parts[i].strip()
        if part in section_headers:
            content = parts[i + 1].strip() if i + 1 < len(parts) else ""
            combined = part + "\n" + content
            words = combined.split()
            if len(words) <= chunk_size:
                chunks.append(combined)
            else:
                j = 0
                while j < len(words):
                    chunk = part + " (continued): " + " ".join(words[j:j + chunk_size])
                    chunks.append(chunk)
                    j += chunk_size - overlap
            i += 2
        else:
            if part and len(part) > 20:
                chunks.append(part)
            i += 1

    if len(chunks) <= 1:
        words = text.split()
        chunks = []
        i = 0
        while i < len(words):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            i += chunk_size - overlap

    return [c for c in chunks if len(c.strip()) > 20]
