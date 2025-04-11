from typing import Optional, List
from pydantic import BaseModel

class TagBase(BaseModel):
    """Base Tag schema with common fields"""
    name: str

class TagCreate(TagBase):
    """Schema for creating a new tag"""
    pass

class Tag(TagBase):
    """Schema for Tag response"""
    id: int
    
    class Config:
        from_attributes = True
