"""User Pydantic schemas"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: Optional[str] = ""


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")


class UserUpdate(BaseModel):
    """User update schema"""
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)


class UserResponse(UserBase):
    """User response schema"""
    id: int
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    user: UserResponse
