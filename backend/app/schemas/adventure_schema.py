from typing import Optional, List, Union, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class TagBase(BaseModel):
    """Tag schema for Adventure tags"""
    name: str

class Tag(TagBase):
    """Full Tag schema including DB fields"""
    id: int
    
    class Config:
        from_attributes = True

class AdventureBase(BaseModel):
    """Base Adventure schema with common fields"""
    title: str
    slug: Optional[str] = None
    description: str
    content: str
    featured_image_url: Optional[str] = None
    is_published: bool = False
    distance: Optional[float] = None
    elevation_gain: Optional[float] = None
    duration_days: Optional[int] = None
    location: Optional[str] = None
    
class AdventureCreate(AdventureBase):
    """Schema for creating a new adventure"""
    tags: Optional[List[Union[int, str]]] = []

class AdventureUpdate(BaseModel):
    """Schema for updating an existing adventure"""
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    featured_image_url: Optional[str] = None
    is_published: Optional[bool] = None
    distance: Optional[float] = None
    elevation_gain: Optional[float] = None
    duration_days: Optional[int] = None
    location: Optional[str] = None
    tags: Optional[List[Union[int, str]]] = None

class Adventure(AdventureBase):
    """Schema for Adventure response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    tags: Optional[List[Tag]] = []
    
    class Config:
        from_attributes = True
