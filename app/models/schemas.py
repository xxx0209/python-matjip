from pydantic import BaseModel
from typing import List, Dict, Optional

class RecommendRequest(BaseModel):
    question: str
    userId: Optional[int] = None
    preferredCategories: Optional[List[str]] = []

class Place(BaseModel):
    name: str
    address: str
    lat: float
    lng: float
    category: str
    score: float

class RecommendResponse(BaseModel):
    analysis: Dict
    recommended_places: List[Dict]
    ai_comment: str