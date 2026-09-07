# app/config.py
import os

from dotenv import load_dotenv

load_dotenv()


def get_groq_api_key() -> str:
    api_key = os.getenv("GROQ_API_KEY", "")

    if api_key:
        return api_key

    try:
        import streamlit as st

        return st.secrets["GROQ_API_KEY"]
    except (ImportError, FileNotFoundError, KeyError):
        return ""


class Settings:
    GROQ_API_KEY: str = get_groq_api_key()


settings = Settings()