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

class ProfileCreate(ProfileBase):
    """Schema for creating a new profile. user_id is derived from the logged-in user."""
    class Config:
        schema_extra = {
            "example": {
                "nickname": "Schwob aufm Sattl",
                "bio": "Radabenteuer, Outdoor und Bikepacking aus Schwaben.",
                "location": "Stuttgart",
                "website": "https://schwobaufmsattl.de",
                "avatar_url": "/uploads/images/avatar.jpg",
                "social_links": {"instagram": "@schwobaufmsattl", "youtube": "schwobaufmsattl"}
            }
        }

class ProfileUpdate(BaseModel):
    """Schema for updating an existing profile"""
    nickname: Optional[str] = Field(None, example="Schwob aufm Sattl")
    bio: Optional[str] = Field(None, example="Radabenteuer, Outdoor und Bikepacking aus Schwaben.")
    location: Optional[str] = Field(None, example="Stuttgart")
    website: Optional[str] = Field(None, example="https://schwobaufmsattl.de")
    avatar_url: Optional[str] = Field(None, example="/uploads/images/avatar.jpg")
    social_links: Optional[dict] = Field(None, example={"instagram": "@schwobaufmsattl", "youtube": "schwobaufmsattl"})

class Profile(ProfileBase):
    """Schema for Profile response"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "nickname": "Schwob aufm Sattl",
                "bio": "Radabenteuer, Outdoor und Bikepacking aus Schwaben.",
                "location": "Stuttgart",
                "website": "https://schwobaufmsattl.de",
                "avatar_url": "/uploads/images/avatar.jpg",
                "social_links": {"instagram": "@schwobaufmsattl", "youtube": "schwobaufmsattl"},
                "created_at": "2025-04-18T12:00:00Z",
                "updated_at": "2025-04-18T12:00:00Z"
            }
        }
