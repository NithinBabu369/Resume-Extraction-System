# app/services/extractor.py
import pymupdf as fitz
import docx
import io

def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    text = ""
    filename_lower = filename.lower()
    
    if filename_lower.endswith(".pdf"):
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
                
    elif filename_lower.endswith(".docx"):
        doc = docx.Document(io.BytesIO(file_bytes))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
    else:
        raise ValueError("Unsupported file format. Only PDF and DOCX files are allowed.")
        
    return text.strip()