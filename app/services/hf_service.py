# app/services/hf_service.py

from typing import List, Dict, Optional

HF_AVAILABLE = False
generator = None

try:
    from transformers import pipeline

    # 🔥 서버 시작 시 1번만 로드됨
    generator = pipeline(
        "text-generation",
        model="distilgpt2",
        device=-1  # CPU 사용 (GPU 있으면 0)
    )
    HF_AVAILABLE = True
    print("✅ HuggingFace 모델 로드 성공")
except Exception as e:
    print("❌ HuggingFace 로드 실패:", e)
    HF_AVAILABLE = False


def generate_hf_comment(question: str, places: List[Dict]) -> Optional[str]:
    """
    HuggingFace 기반 추천 멘트 생성
    실패하면 None 반환 → 상위에서 fallback 처리
    """

    if not HF_AVAILABLE or not places:
        return None

    try:
        place_names = ", ".join([p["name"] for p in places[:5]])

        prompt = (
            f"사용자 질문: {question}\n"
            f"추천할 장소: {place_names}\n"
            "위 정보를 바탕으로 자연스럽게 한 문장 추천해줘:"
        )

        result = generator(
            prompt,
            max_length=60,
            do_sample=True,
            temperature=0.7,
            num_return_sequences=1
        )

        text = result[0]["generated_text"]

        # 🔥 프롬프트 부분 제거 (distilgpt2 특성 대응)
        if "추천해줘:" in text:
            text = text.split("추천해줘:")[-1].strip()

        return text

    except Exception as e:
        print("HF 생성 실패:", e)
        return None
