from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class ImageBase(BaseModel):
    """Base Image schema with common fields"""
    filename: str
    url: str
    description: Optional[str] = None
    alt_text: Optional[str] = None
    adventure_id: Optional[int] = None

class ImageCreate(ImageBase):
    """Schema for creating a new image"""
    pass

class Image(ImageBase):
    """Schema for Image response"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
