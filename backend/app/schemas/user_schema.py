from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    """Base User schema with common fields"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str

class UserUpdate(BaseModel):
    """Schema for updating an existing user"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    """Schema for user response"""
    id: int
    
    class Config:
        from_attributes = True
