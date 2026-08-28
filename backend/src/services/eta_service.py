import math
from src.infrastructure.ai.gemini_client import GeminiClient
from src.domain.constants import DEFAULT_DRONE_SPEED_KMH


class ETAService:
    def __init__(self, gemini_client: GeminiClient = None):
        self.gemini_client = gemini_client or GeminiClient()

    def _haversine_distance_km(self, lat1, lng1, lat2, lng2):
        R = 6371  # bán kính Trái Đất (km)
        d_lat = math.radians(lat2 - lat1)
        d_lng = math.radians(lng2 - lng1)
        a = (math.sin(d_lat / 2) ** 2
             + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
             * math.sin(d_lng / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def estimate(self, origin_lat, origin_lng, dest_lat, dest_lng, speed_kmh=None):
        speed = speed_kmh or DEFAULT_DRONE_SPEED_KMH
        distance_km = self._haversine_distance_km(origin_lat, origin_lng, dest_lat, dest_lng)
        eta_hours = distance_km / speed
        eta_minutes = round(eta_hours * 60, 1)

        result = {
            "distance_km": round(distance_km, 2),
            "speed_kmh": speed,
            "eta_minutes": eta_minutes,
            "ai_explanation": None,
        }

        try:
            prompt = (
                f"Một drone giao hàng bay quãng đường {result['distance_km']} km "
                f"với tốc độ {speed} km/h, thời gian ước tính là {eta_minutes} phút. "
                f"Hãy viết 1 câu ngắn gọn, thân thiện thông báo cho khách hàng về thời gian giao hàng này."
            )
            result["ai_explanation"] = self.gemini_client.generate_text(prompt)
        except Exception:
            result["ai_explanation"] = f"Dự kiến giao hàng trong khoảng {eta_minutes} phút."

        return result