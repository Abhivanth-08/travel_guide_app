from pydantic import BaseModel
from typing import List, Optional

class OpeningHours(BaseModel):
    open: str
    close: str

class Place(BaseModel):
    id: str
    name: str
    description: str
    category: str
    latitude: float
    longitude: float
    rating: float
    images: List[str]
    opening_hours: Optional[dict] = None # simplified for now
    crowd_level: str = "LOW"
    estimated_visit_duration: int # minutes
    entry_fee: float = 0
    audio_guide: Optional[str] = None
    
    distance: Optional[float] = None
