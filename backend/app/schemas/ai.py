from pydantic import BaseModel
from typing import List, Optional

class AIRecommendationRequest(BaseModel):
    user_id: str
    lat: float
    lng: float
    available_hours: int
    interests: List[str]
    budget: str

class AIItineraryItem(BaseModel):
    time: str
    place_name: str
    reason: str

class AIResponse(BaseModel):
    summary: str
    itinerary: List[AIItineraryItem]
    warnings: List[str]
