from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/alerts", tags=["alerts"])

class Alert(BaseModel):
    id: str
    message: str
    severity: str
    location_id: str

@router.get("/", response_model=List[Alert])
async def get_alerts():
    # Simulated alerts
    return [
        {
            "id": "1",
            "message": "High crowd expected at Marudamalai Temple today due to a local festival.",
            "severity": "WARNING",
            "location_id": "marudamalai_id"
        },
        {
            "id": "2",
            "message": "Rain expected in Ooty this afternoon. Plan indoor activities.",
            "severity": "INFO",
            "location_id": "ooty_id"
        }
    ]
