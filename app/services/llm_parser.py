# app/services/llm_parser.py
import instructor
from groq import Groq
from app.config import settings
from app.schemas.resume import OrderedResume

# Instantiate and patch Groq client using Instructor MD_JSON mode
groq_client = Groq(api_key=settings.GROQ_API_KEY)
client = instructor.from_groq(groq_client, mode=instructor.Mode.MD_JSON)

def parse_resume_text(raw_text: str) -> OrderedResume:
    """Sends raw text to Groq API and validates structure using Pydantic."""
    
    response = client.chat.completions.create(
        model="groq/compound-mini",
        response_model=OrderedResume,
        max_retries=2,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert resume parsing engine. Extract details from the "
                    "provided raw resume text into the exact requested JSON structure. "
                    "Do not invent details not present in the document."
                ),
            },
            {
                "role": "user",
                "content": f"Resume Text:\n{raw_text}",
            },
        ],
    )
    return response