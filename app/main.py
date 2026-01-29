from fastapi import FastAPI
from app.api.recommend import router as recommend_router

app = FastAPI(
    title="AI Restaurant Recommendation API",
    description="카카오 지도 + AI 기반 맛집 추천 서비스",
    version="1.0.0"
)

# 기본 테스트
@app.get("/")
async def root():
    return {"message": "AI Recommendation Server Running"}

# 헬스체크 (AWS 로드밸런서용)
@app.get("/health")
def health():
    return {"status": "UP"}

# 🔥 AI 추천 API 연결
app.include_router(recommend_router)
