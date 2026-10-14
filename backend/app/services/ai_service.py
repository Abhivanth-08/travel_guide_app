import json
from groq import Groq
from app.config import settings

def get_groq_client():
    if not settings.GROQ_API_KEY:
        return None
    return Groq(api_key=settings.GROQ_API_KEY)

async def generate_itinerary(context: dict):
    client = get_groq_client()
    
    # Fallback for demo mode if no key
    if not client or settings.DEMO_MODE:
        return {
            "summary": "This is a demo itinerary since the Groq API key is not configured.",
            "itinerary": [
                {"time": "09:00", "place_name": "Demo Place 1", "reason": "Close to you"},
                {"time": "12:00", "place_name": "Demo Place 2", "reason": "Good for lunch"}
            ],
            "warnings": ["API Key not found, using demo mode."]
        }

    prompt = f"""
    You are a travel assistant. You only output valid JSON.
    Context:
    User wants to travel for {context.get('available_hours')} hours.
    Interests: {context.get('interests')}.
    Budget: {context.get('budget')}.
    Nearby places provided by system: {context.get('places_summary')}.

    Generate a travel itinerary in the exact JSON structure:
    {{
      "summary": "overall description",
      "itinerary": [
         {{"time": "09:00", "place_name": "Name", "reason": "Why"}}
      ],
      "warnings": ["any alerts like weather or crowd"]
    }}
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": prompt}],
        model="llama3-8b-8192",
        response_format={"type": "json_object"}
    )
    
    result = response.choices[0].message.content
    return json.loads(result)
