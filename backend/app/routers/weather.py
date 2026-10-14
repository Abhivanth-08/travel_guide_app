from fastapi import APIRouter
from pydantic import BaseModel
import random

router = APIRouter(prefix="/weather", tags=["weather"])

class WeatherResponse(BaseModel):
    temperature: float
    condition: str
    humidity: int
    wind: float
    rain_probability: int

@router.get("/", response_model=WeatherResponse)
async def get_weather(lat: float, lng: float):
    # Simulated weather response for demo purposes
    conditions = ["Sunny", "Cloudy", "Rainy", "Clear"]
    return {
        "temperature": round(random.uniform(20.0, 35.0), 1),
        "condition": random.choice(conditions),
        "humidity": random.randint(40, 90),
        "wind": round(random.uniform(2.0, 15.0), 1),
        "rain_probability": random.randint(0, 100) if random.random() > 0.5 else 0
    }
