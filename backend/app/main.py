from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection
from app.routers import auth, places, ai, itinerary, ws, weather, alerts

app = FastAPI(
    title="Smart Travel Guide API",
    description="Backend API for the Smart Travel Guide Mobile Application",
    version="1.0.0",
    on_startup=[connect_to_mongo],
    on_shutdown=[close_mongo_connection]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(places.router)
app.include_router(ai.router)
app.include_router(itinerary.router)
app.include_router(ws.router)
app.include_router(weather.router)
app.include_router(alerts.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
