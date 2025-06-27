# llm_tools/google_places.py
import os
import requests
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_PALCE_API_KEY")
@tool
def get_places_by_keyword_and_location(keyword: str, location: str) -> str:
    """
    [Instruction]
    지역과 키워드를 기반으로 Google Places에서 실제 존재하는 장소(식당, 카페 등)를 검색합니다.
    실제 존재하는 장소만 보여줘야 할 때 호출하세요.

    [Args]
    - keyword: 예) 맛집, 한식당, 카페, 체험활동
    - location: 예) 경복궁, 서울 종로구, 해운대 등

    [Returns]
    상위 5개 장소의 이름, 주소, 평점 등을 요약해 반환합니다.
    """
    try:
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": f"{location} {keyword}",
            "key": GOOGLE_API_KEY,
            "language": "ko"
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if not data.get("results"):
            return f"❌ '{location}'에서 '{keyword}'에 해당하는 장소를 찾을 수 없습니다."

        results = data["results"][:5]
        lines = []
        for place in results:
            name = place.get("name", "이름없음")
            address = place.get("formatted_address", "주소없음")
            rating = place.get("rating", "N/A")
            lines.append(f"📍 {name} | 평점: {rating}\n  - 주소: {address}")
        return "\n\n".join(lines)

    except Exception as e:
        return f"❌ 장소 검색 중 오류 발생: {str(e)}"
