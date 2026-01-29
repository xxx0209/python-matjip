from fastapi import APIRouter, HTTPException
from app.models.schemas import RecommendRequest, RecommendResponse
from app.services.ai_service import analyze_question, generate_recommend_comment
from app.services.place_service import search_places

router = APIRouter(prefix="/recommend", tags=["AI Recommendation"])


@router.post("/", response_model=RecommendResponse)
async def recommend(data: RecommendRequest):

    analysis = analyze_question(data.question)

    places = await search_places(
        analysis["location"] or "서울",
        analysis["food"] or "",
        data.lat,
        data.lng
    )

    if not places:
        raise HTTPException(status_code=404, detail="추천할 장소 없음")

    comment = generate_recommend_comment(data.question, places[:5])

    return {
        "analysis": analysis,
        "recommended_places": places[:5],
        "ai_comment": comment
    }
