from fastapi import APIRouter, Depends, HTTPException
from typing import List
import uuid
from datetime import datetime
from app.schemas.itinerary import Itinerary, ItineraryCreate
from app.database import get_database
from app.routers.auth import get_current_user

router = APIRouter(prefix="/itinerary", tags=["itinerary"])

@router.post("/", response_model=Itinerary)
async def create_itinerary(itinerary: ItineraryCreate, current_user: dict = Depends(get_current_user)):
    db = get_database()
    
    itin_dict = itinerary.model_dump()
    itin_dict["_id"] = str(uuid.uuid4())
    itin_dict["user_id"] = current_user["_id"]
    itin_dict["created_at"] = datetime.utcnow().isoformat()
    
    await db["itineraries"].insert_one(itin_dict)
    
    itin_dict["id"] = itin_dict.pop("_id")
    return itin_dict

@router.get("/", response_model=List[Itinerary])
async def get_itineraries(current_user: dict = Depends(get_current_user)):
    db = get_database()
    cursor = db["itineraries"].find({"user_id": current_user["_id"]})
    itineraries = await cursor.to_list(length=50)
    
    for i in itineraries:
        i["id"] = i.pop("_id")
    return itineraries
