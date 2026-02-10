from openai import OpenAI
from app.config import AI_API_KEY

client = OpenAI(api_key=AI_API_KEY)

FOODS = ["고기", "치킨", "파스타", "햄버거", "초밥", "술집", "카페", "피자"]


def analyze_question(question: str) -> dict:
    food = next((f for f in FOODS if f in question), None)

    location = question
    if food:
        location = location.replace(food, "")

    location = (
        location.replace("맛집", "")
        .replace("추천해줘", "")
        .replace("추천", "")
        .strip()
    )

    mood = "분위기 좋은" if "분위기" in question or "감성" in question else None

    return {"location": location, "food": food, "mood": mood}


def generate_rule_based_comment(question: str, places: list):
    if not places:
        return "조건에 맞는 맛집을 찾지 못했어요 😢"

    names = ", ".join([p["name"] for p in places[:2]])

    if "분위기" in question or "감성" in question:
        return f"{names}는 분위기가 좋아서 데이트나 모임에 추천드려요 ✨"

    if any(food in question for food in FOODS):
        return f"{names}가 요청하신 메뉴에 잘 맞는 맛집이에요 🍽️"

    return f"{names}는 평점과 리뷰가 좋아 추천드려요 👍"
