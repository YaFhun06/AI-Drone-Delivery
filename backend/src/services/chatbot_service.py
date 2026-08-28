from src.infrastructure.ai.gemini_client import GeminiClient


class ChatbotService:
    def __init__(self, gemini_client: GeminiClient = None):
        self.gemini_client = gemini_client or GeminiClient()

    def ask(self, question: str) -> str:
        if not question or not question.strip():
            raise ValueError("Câu hỏi không được để trống")

        prompt = (
            "Bạn là trợ lý ảo hỗ trợ khách hàng cho dịch vụ giao hàng bằng drone. "
            "Hãy trả lời ngắn gọn, thân thiện, dễ hiểu bằng tiếng Việt.\n\n"
            f"Câu hỏi của khách hàng: {question}"
        )

        try:
            return self.gemini_client.generate_text(prompt)
        except Exception:
            return "Xin lỗi, hệ thống chatbot đang gặp sự cố. Vui lòng thử lại sau hoặc liên hệ tổng đài hỗ trợ."