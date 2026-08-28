import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY chưa được cấu hình trong .env")

genai.configure(api_key=API_KEY)

class GeminiClient:
    def __init__(self, model_name='gemini-flash-latest'):
        self.model = genai.GenerativeModel(model_name)

    def generate_text(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")