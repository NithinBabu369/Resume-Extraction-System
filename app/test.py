import os
from dotenv import load_dotenv

load_dotenv()
k = os.getenv("GROQ_API_KEY")
print("SET" if k else "MISSING", len(k) if k else 0)

import os
import requests

key = os.getenv("GROQ_API_KEY")

r = requests.get(
    "https://api.groq.com/openai/v1/models",
    headers={"Authorization": f"Bearer {key}"}
)

print(r.status_code, r.text)