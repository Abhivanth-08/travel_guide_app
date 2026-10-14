from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas.user import UserCreate, UserLogin, UserOut, Token, TokenData
from app.services.auth_service import get_password_hash, verify_password, create_access_token
from app.database import get_database
from app.config import settings
from jose import JWTError, jwt
from datetime import timedelta, datetime
import uuid

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
        
    db = get_database()
    user = await db["users"].find_one({"email": token_data.email})
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    db = get_database()
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    user_dict = user.model_dump()
    user_dict["password_hash"] = get_password_hash(user_dict.pop("password"))
    user_dict["_id"] = str(uuid.uuid4())
    user_dict["created_at"] = datetime.utcnow().isoformat()
    if not user_dict.get("preferences"):
        user_dict["preferences"] = {"interests": [], "budget": "medium", "travel_pace": "moderate", "language": "en"}
    
    await db["users"].insert_one(user_dict)
    
    # Format for response
    user_dict["id"] = user_dict.pop("_id")
    return user_dict

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    db = get_database()
    user = await db["users"].find_one({"email": user_credentials.email})
    
    if not user or not verify_password(user_credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def get_users_me(current_user: dict = Depends(get_current_user)):
    current_user["id"] = current_user.pop("_id")
    return current_user
