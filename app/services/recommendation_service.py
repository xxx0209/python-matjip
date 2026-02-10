import random


async def calculate_place_score(
    place: dict,
    analysis: dict,
    preferred_categories: list[str]
) -> float:
    score = 0

    # 1️⃣ 질문 기반 점수
    if analysis.get("food") and analysis["food"] in place.get("category", ""):
        score += 5

    # 2️⃣ 🔥 사용자 선호 카테고리 (상위 3개)
    for idx, category in enumerate(preferred_categories):
        if category in place.get("category", ""):
            score += (3 - idx) * 2
            # 1순위 6점 / 2순위 4점 / 3순위 2점

    # 3️⃣ 랜덤성 (동점 방지)
    score += random.uniform(0, 1)

    return round(score, 2)
