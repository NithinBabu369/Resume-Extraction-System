# 📄 Resume Extraction System

An intelligent, schema-enforced resume parsing engine powered by **PyMuPDF**, **python-docx**, **Groq LLM** (`groq/compound-mini`), **Instructor**, and **Pydantic**. 

It extracts text from resume documents (`.pdf` and `.docx`) and transforms unstructured text into a standardized, strictly ordered JSON schema.

---

## ✨ Features

- **Document Extraction**: Robust text extraction for PDF and DOCX files.
- **Structured Schema Validation**: Guaranteed output structure using Pydantic and Instructor (`Header`, `Profile`, `Experience`, `Projects`, `Skills`, `Education`, `Certification`).
- **Interactive Streamlit Web UI**: Upload CVs, inspect raw extracted text, view interactive formatted sections, and download parsed JSON.
- **REST API Endpoint**: FastAPI backend for integration into external services.

---

## 📁 Project Structure

```
cvUploader/
├── app/
│   ├── config.py           # Environment and settings configuration
│   ├── main.py             # FastAPI backend server
│   ├── schemas/
│   │   └── resume.py       # Pydantic data models for structured CV schema
│   └── services/
│       ├── extractor.py    # PyMuPDF & python-docx text extraction logic
│       └── llm_parser.py   # Groq & Instructor LLM parsing service
├── streamlit_app.py        # Streamlit web application frontend
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables (API Keys)
```

---

## ⚙️ Environment Setup

### 1. Prerequisites & Virtual Environment

Ensure you have Python 3.10+ installed. Activate the project virtual environment:

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Create or update the `.env` file in the root directory:

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```

Get your free Groq API key from [Groq Console](https://console.groq.com/keys).

---

## 🚀 How to Run the Application

### Option 1: Streamlit Web Interface

Launch the interactive web UI:

```powershell
.\venv\Scripts\streamlit run streamlit_app.py
```

Open your browser at `http://localhost:8501`.

### Option 2: FastAPI REST API

Start the backend server:

```powershell
.\venv\Scripts\uvicorn app.main:app --reload
```

- **Interactive API Documentation (Swagger UI)**: `http://127.0.0.1:8000/docs`
- **Parse Endpoint**: `POST /api/v1/parse-cv` (Accepts `multipart/form-data` with `.pdf` or `.docx` file)

---

## 📊 Sample Output Schema

```json
{
  "header": {
    "full_name": "Jane Doe",
    "email": "jane.doe@example.com",
    "phone": "+1 (555) 123-4567",
    "location": "San Francisco, CA",
    "links": ["linkedin.com/in/janedoe", "github.com/janedoe"]
  },
  "profile": "Senior Full Stack Engineer with 6+ years of experience...",
  "experience": [
    {
      "job_title": "Senior Software Engineer",
      "company": "Tech Corp",
      "duration": "Jan 2022 - Present",
      "responsibilities": [
        "Led backend microservices migration using Python and FastAPI",
        "Optimized database performance by 40%"
      ]
    }
  ],
  "projects": [],
  "skills": ["Python", "FastAPI", "React", "Docker", "PostgreSQL"],
  "education": [
    {
      "degree": "B.S. Computer Science",
      "institution": "Stanford University",
      "year": "2020"
    }
  ],
  "certification": []
}
```