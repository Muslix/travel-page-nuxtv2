from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class EquipmentBase(BaseModel):
    """Base Equipment schema with common fields"""
    name: str
    description: str
    category: str
    weight_grams: Optional[int] = None
    price: Optional[float] = None
    purchase_link: Optional[str] = None
    image_url: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)

class EquipmentCreate(EquipmentBase):
    """Schema for creating new equipment"""
    pass

class EquipmentUpdate(BaseModel):
    """Schema for updating existing equipment"""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    weight_grams: Optional[int] = None
    price: Optional[float] = None
    purchase_link: Optional[str] = None
    image_url: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)

class Equipment(EquipmentBase):
    """Schema for Equipment response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
