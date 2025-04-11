from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class ProfileBase(BaseModel):
    """Base Profile schema with common fields"""
    nickname: str
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    avatar_url: Optional[str] = None
    social_links: Optional[dict] = None
    user_id: int

class ProfileCreate(ProfileBase):
    """Schema for creating a new profile"""
    pass

class ProfileUpdate(BaseModel):
    """Schema for updating an existing profile"""
    nickname: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    avatar_url: Optional[str] = None
    social_links: Optional[dict] = None

class Profile(ProfileBase):
    """Schema for Profile response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
