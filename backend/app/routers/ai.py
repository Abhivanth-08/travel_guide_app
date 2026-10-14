from fastapi import APIRouter, Depends
from app.schemas.ai import AIRecommendationRequest, AIResponse
from app.services.ai_service import generate_itinerary
from app.database import get_database
from app.routers.auth import get_current_user

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/recommend", response_model=AIResponse)
async def get_recommendation(request: AIRecommendationRequest, current_user: dict = Depends(get_current_user)):
    db = get_database()
    
    # Fetch nearby places context
    places_cursor = db["places"].find({})
    places = await places_cursor.to_list(length=100)
    
    # Generate simple summary of places for AI
    places_summary = ", ".join([f"{p['name']} ({p['category']})" for p in places[:5]])
    
    context = {
        "available_hours": request.available_hours,
        "interests": request.interests,
        "budget": request.budget,
        "places_summary": places_summary
    }
    
    result = await generate_itinerary(context)
    return result
