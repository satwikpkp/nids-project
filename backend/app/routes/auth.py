import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from backend.app.models.user import UserCreate, UserLogin, UserResponse, Token
from backend.app.services.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_user_by_email_or_username,
    get_current_user
)
from backend.app.database import db_manager, memory_store

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Pre-seed a default administrator if store is empty
DEFAULT_ADMIN_EMAIL = "admin@soc.defense"
if not memory_store.get_user_by_email(DEFAULT_ADMIN_EMAIL):
    memory_store.insert_user({
        "id": "admin_default",
        "email": DEFAULT_ADMIN_EMAIL,
        "username": "admin",
        "full_name": "Chief Security Officer",
        "hashed_password": get_password_hash("Admin@123456"),
        "role": "admin",
        "is_active": True,
        "created_at": datetime.utcnow()
    })

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate):
    # Check if email or username already taken
    existing_user = await get_user_by_email_or_username(user_in.email)
    if not existing_user:
        existing_user = await get_user_by_email_or_username(user_in.username)
        
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )
    
    user_id = str(uuid.uuid4())
    user_dict = {
        "id": user_id,
        "email": user_in.email.lower(),
        "username": user_in.username,
        "full_name": user_in.full_name or user_in.username,
        "hashed_password": get_password_hash(user_in.password),
        "role": user_in.role if user_in.role in ["admin", "analyst", "auditor"] else "analyst",
        "is_active": True,
        "created_at": datetime.utcnow()
    }
    
    if db_manager.is_connected_to_mongo and db_manager.db is not None:
        await db_manager.db["users"].insert_one(user_dict)
    else:
        memory_store.insert_user(user_dict)
        
    access_token = create_access_token(
        data={"sub": user_dict["email"], "role": user_dict["role"]}
    )
    
    user_resp = UserResponse(
        id=user_id,
        email=user_dict["email"],
        username=user_dict["username"],
        full_name=user_dict["full_name"],
        role=user_dict["role"],
        is_active=True,
        created_at=user_dict["created_at"]
    )
    
    return Token(access_token=access_token, user=user_resp)

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    user = await get_user_by_email_or_username(credentials.username_or_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password"
        )
        
    if not verify_password(credentials.password, user.get("hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password"
        )
        
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account. Contact security administrator."
        )
        
    access_token = create_access_token(
        data={"sub": user["email"], "role": user.get("role", "analyst")}
    )
    
    user_resp = UserResponse(
        id=str(user.get("id", user.get("_id", "user_1"))),
        email=user["email"],
        username=user["username"],
        full_name=user.get("full_name"),
        role=user.get("role", "analyst"),
        is_active=user.get("is_active", True),
        created_at=user.get("created_at", datetime.utcnow())
    )
    
    return Token(access_token=access_token, user=user_resp)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user
