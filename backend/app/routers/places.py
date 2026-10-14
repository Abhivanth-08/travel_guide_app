from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas.place import Place
from app.database import get_database
from geopy.distance import geodesic
import math

router = APIRouter(prefix="/places", tags=["places"])

@router.get("/", response_model=List[Place])
async def get_all_places(category: Optional[str] = None):
    db = get_database()
    query = {}
    if category:
        query["category"] = category
    places_cursor = db["places"].find(query)
    places = await places_cursor.to_list(length=100)
    
    # Fix ID
    for p in places:
        p["id"] = p.pop("_id")
    return places

@router.get("/nearby", response_model=List[Place])
async def get_nearby_places(lat: float, lng: float, radius: float = 10.0): # radius in km
    db = get_database()
    places_cursor = db["places"].find({})
    places = await places_cursor.to_list(length=100)
    
    nearby = []
    for p in places:
        p["id"] = p.pop("_id")
        place_coord = (p["latitude"], p["longitude"])
        user_coord = (lat, lng)
        dist = geodesic(user_coord, place_coord).km
        
        if dist <= radius:
            p["distance"] = dist
            nearby.append(p)
            
    # Sort by distance
    nearby.sort(key=lambda x: x["distance"])
    return nearby

@router.get("/search", response_model=List[Place])
async def search_places(q: str):
    db = get_database()
    query = {"name": {"$regex": q, "$options": "i"}}
    places_cursor = db["places"].find(query)
    places = await places_cursor.to_list(length=20)
    for p in places:
        p["id"] = p.pop("_id")
    return places

@router.get("/{place_id}", response_model=Place)
async def get_place(place_id: str):
    db = get_database()
    place = await db["places"].find_one({"_id": place_id})
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    place["id"] = place.pop("_id")
    return place
