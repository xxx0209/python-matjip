from openai import OpenAI
from app.config import AI_API_KEY
from app.services.hf_service import generate_hf_comment
import json

client = OpenAI(api_key=AI_API_KEY)

# ----------------------------
# ✅ 전국 지역 사전 (여기에 계속 추가 가능)
# ----------------------------
LOCATIONS = [
    "서울","강남","홍대","성수","잠실","건대","신촌",
    "부산","해운대","광안리",
    "대구","동성로",
    "대전","둔산동",
    "광주","상무지구",
    "제주","서귀포"
]

# ----------------------------
# ✅ 음식 카테고리 사전
# ----------------------------
FOODS = [
    "고기","치킨","파스타","햄버거","초밥","회",
    "국밥","라멘","분식","카페","술집","족발","피자"
]

# ----------------------------
# 🧩 규칙 기반 분석 (항상 동작하는 핵심 엔진)
# ----------------------------
def rule_based_analysis(question: str) -> dict:
    location = next((l for l in LOCATIONS if l in question), None)
    food = next((f for f in FOODS if f in question), None)
    mood = "분위기 좋은" if "분위기" in question else None

    return {"location": location, "food": food, "mood": mood}


# ----------------------------
# 🤖 AI 보조 분석 (부족할 때만 사용)
# ----------------------------
def call_openai_analysis(question: str) -> dict:
    prompt = f"""
    사용자의 질문에서 정보를 JSON으로 추출해라.

    {{
      "location": "",
      "food": "",
      "mood": ""
    }}

    질문: "{question}"
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)


# ----------------------------
# 🔥 최종 질문 분석 함수 (여기가 핵심)
# ----------------------------
def analyze_question(question: str) -> dict:

    # 1️⃣ 무료 규칙 분석 먼저
    analysis = rule_based_analysis(question)

    # 2️⃣ 부족한 값 있을 때만 AI 호출
    if not analysis["location"] or not analysis["food"]:
        try:
            ai_result = call_openai_analysis(question)

            # AI 결과로 비어있는 값만 채움
            for key in analysis:
                if not analysis[key] and ai_result.get(key):
                    analysis[key] = ai_result[key]

        except Exception as e:
            print("AI 분석 실패 → 규칙 기반 유지:", e)

    return analysis


# ----------------------------
# ✍️ 추천 멘트 생성
# ----------------------------
def generate_recommend_comment(question: str, places: list):

    # 1️⃣ OpenAI 시도
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": f"질문:{question}\n맛집:{places}\n자연스럽게 추천해줘"
            }]
        )
        return response.choices[0].message.content

    except:
        pass

    return f"{places[0]['name']} 추천드립니다! 근처에 좋은 맛집들이 많아요."