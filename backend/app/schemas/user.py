from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class UserPreferences(BaseModel):
    interests: List[str] = []
    budget: str = "medium"
    travel_pace: str = "moderate"
    language: str = "en"

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)
    preferences: Optional[UserPreferences] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    preferences: UserPreferences
    created_at: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
