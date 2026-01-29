from pydantic import BaseModel
from typing import List, Optional

class Place(BaseModel):
    name: str
    address: str
    lat: str
    lng: str
    category: str
    distance: str

class Analysis(BaseModel):
    location: Optional[str]
    food: Optional[str]
    mood: Optional[str]

class RecommendRequest(BaseModel):
    question: str
    lat: float
    lng: float

class RecommendResponse(BaseModel):
    analysis: Analysis
    recommended_places: List[Place]
    ai_comment: str
