from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    email: str = Field(..., description="User official email address")
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None
    role: str = Field(default="analyst", description="Role: admin, analyst, or auditor")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username_or_email: str
    password: str

class UserResponse(UserBase):
    id: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenData(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
