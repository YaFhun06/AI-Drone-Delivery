import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()


class GeminiClient:
    def __init__(self, model_name='gemini-flash-latest'):
        api_key = os.getenv('GEMINI_API_KEY')

        if not api_key:
            self.model = None
            return

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate_text(self, prompt: str) -> str:
        if not self.model:
            raise RuntimeError(
                "GEMINI_API_KEY chưa được cấu hình trong .env"
            )

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")