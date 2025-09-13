import os
import google.generativeai as genai
from dotenv import load_dotenv

# Ładowanie klucza API
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("Brakuje GOOGLE_API_KEY w środowisku!")

# Konfiguracja klienta Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.0-flash")

def send_to_gemini(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Błąd Gemini: {e}")
