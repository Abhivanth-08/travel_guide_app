import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

# Simplified seed script
places = [
    {
        "_id": str(uuid.uuid4()),
        "name": "Marudamalai Temple",
        "description": "A famous 12th century hill temple dedicated to Lord Murugan.",
        "category": "Temples",
        "latitude": 11.0456,
        "longitude": 76.8488,
        "rating": 4.8,
        "images": ["https://upload.wikimedia.org/wikipedia/commons/4/46/Marudamalai_Temple_Coimbatore.jpg"],
        "crowd_level": "HIGH",
        "estimated_visit_duration": 120,
        "entry_fee": 0,
        "audio_guide": "Welcome to Marudamalai Temple, a sacred place of worship located on a picturesque hill..."
    },
    {
        "_id": str(uuid.uuid4()),
        "name": "Gass Forest Museum",
        "description": "A government-run natural history museum.",
        "category": "Museums",
        "latitude": 11.0145,
        "longitude": 76.9458,
        "rating": 4.5,
        "images": ["https://upload.wikimedia.org/wikipedia/commons/3/36/Gass_Forest_Museum.jpg"],
        "crowd_level": "LOW",
        "estimated_visit_duration": 90,
        "entry_fee": 20,
        "audio_guide": "The Gass Forest Museum is one of the oldest museums in India, established in 1902..."
    },
    {
        "_id": str(uuid.uuid4()),
        "name": "Ooty Lake",
        "description": "An artificial lake constructed by John Sullivan, in 1824.",
        "category": "Nature",
        "latitude": 11.4011,
        "longitude": 76.6908,
        "rating": 4.3,
        "images": ["https://upload.wikimedia.org/wikipedia/commons/e/eb/Ooty_Lake_View.jpg"],
        "crowd_level": "MEDIUM",
        "estimated_visit_duration": 180,
        "entry_fee": 15,
        "audio_guide": "Ooty lake is a popular destination for boating and enjoying the scenic beauty of the Nilgiris."
    }
]

async def seed_database():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["smart_travel_guide"]
    
    # Drop existing for clean seed
    await db["places"].drop()
    
    await db["places"].insert_many(places)
    print("Database seeded with places!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
