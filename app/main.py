# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from app.schemas.resume import OrderedResume
from app.services.extractor import extract_text_from_file
from app.services.llm_parser import parse_resume_text

app = FastAPI(
    title="Ordered CV Parser API (Groq)",
    description="Upload CVs in PDF/DOCX and receive standardized structured output via Groq Llama 3.3.",
    version="1.0.0"
)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}

@app.post(
    "/api/v1/parse-cv",
    response_model=OrderedResume,
    status_code=status.HTTP_200_OK,
    summary="Upload and parse a CV into ordered sections"
)
async def parse_cv(file: UploadFile = File(...)):
    filename = file.filename or ""
    if not any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Upload a .pdf or .docx file."
        )

    try:
        content = await file.read()
        raw_text = extract_text_from_file(content, filename)
        
        if not raw_text:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Could not extract readable text from document."
            )

        parsed_resume = parse_resume_text(raw_text)
        return parsed_resume

    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing document: {str(e)}"
        )