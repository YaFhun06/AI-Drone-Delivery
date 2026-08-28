from flask import Blueprint, jsonify, request
from src.services.chatbot_service import ChatbotService

chatbot_bp = Blueprint("chatbot", __name__)
chatbot_service = ChatbotService()


@chatbot_bp.route("/api/chatbot/ask", methods=["POST"])
def ask_chatbot():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Trường 'question' là bắt buộc"}), 400

    try:
        answer = chatbot_service.ask(question)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"question": question, "answer": answer}), 200