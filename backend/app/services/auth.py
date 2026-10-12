import uuid
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import bcrypt
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.app.config import settings
from backend.app.database import db_manager, memory_store
from backend.app.models.user import UserResponse, TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # bcrypt check
        return bcrypt.checkpw(plain_password.encode("utf-8")[:72], hashed_password.encode("utf-8"))
    except Exception:
        # fallback secure constant time compare
        return False

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8")[:72], salt)
    return hashed.decode("utf-8")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_user_by_email_or_username(identifier: str) -> Optional[Dict[str, Any]]:
    identifier_lower = identifier.lower()
    if db_manager.is_connected_to_mongo and db_manager.db is not None:
        user = await db_manager.db["users"].find_one({
            "$or": [
                {"email": identifier_lower},
                {"username": identifier}
            ]
        })
        if user:
            user["id"] = str(user.get("_id", uuid.uuid4().hex))
            return user
    
    # Check in-memory store
    user = memory_store.get_user_by_email(identifier_lower)
    if not user:
        user = memory_store.get_user_by_username(identifier)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or session expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(sub=email, role=payload.get("role"))
    except JWTError:
        raise credentials_exception

    user = await get_user_by_email_or_username(token_data.sub)
    if user is None:
        raise credentials_exception
    
    return UserResponse(
        id=user.get("id", "user_1"),
        email=user["email"],
        username=user["username"],
        full_name=user.get("full_name"),
        role=user.get("role", "analyst"),
        is_active=user.get("is_active", True),
        created_at=user.get("created_at", datetime.utcnow())
    )
