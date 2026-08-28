from src.infrastructure.ai.gemini_client import GeminiClient


class DeliverySummaryService:
    def __init__(self, gemini_client: GeminiClient = None):
        self.gemini_client = gemini_client or GeminiClient()

    def summarize(self, order_id, status_history: list) -> str:
        if not status_history:
            raise ValueError("status_history không được để trống")

        history_text = "\n".join(
            f"- {item.get('timestamp', '')}: {item.get('status', '')}"
            for item in status_history
        )

        prompt = (
            f"Đây là lịch sử trạng thái của đơn hàng #{order_id}:\n{history_text}\n\n"
            "Hãy viết một đoạn tóm tắt ngắn gọn (2-3 câu), thân thiện, dễ hiểu bằng tiếng Việt "
            "cho khách hàng biết đơn hàng hiện đang ở đâu trong quy trình giao hàng."
        )

        try:
            return self.gemini_client.generate_text(prompt)
        except Exception:
            last_status = status_history[-1].get("status", "không rõ")
            return f"Đơn hàng #{order_id} hiện đang ở trạng thái: {last_status}."