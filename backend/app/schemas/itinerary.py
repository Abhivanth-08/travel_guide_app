from pydantic import BaseModel
from typing import List, Optional

class ItineraryItem(BaseModel):
    place_id: Optional[str] = None
    place_name: str
    time: str
    reason: Optional[str] = None

class Itinerary(BaseModel):
    id: Optional[str] = None
    user_id: str
    title: str
    items: List[ItineraryItem]
    created_at: str

class ItineraryCreate(BaseModel):
    title: str
    items: List[ItineraryItem]
