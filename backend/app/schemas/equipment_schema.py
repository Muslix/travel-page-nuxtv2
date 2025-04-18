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
    class Config:
        schema_extra = {
            "example": {
                "name": "Ortlieb Lenkertasche",
                "description": "Wasserdichte Lenkertasche für Bikepacking-Touren",
                "category": "Taschen",
                "weight_grams": 450,
                "price": 89.95,
                "purchase_link": "https://www.ortlieb.com/lenkertasche",
                "image_url": "/uploads/images/lenkertasche.jpg",
                "rating": 5
            }
        }

class EquipmentUpdate(BaseModel):
    """Schema for updating existing equipment"""
    name: Optional[str] = Field(None, example="Ortlieb Lenkertasche")
    description: Optional[str] = Field(None, example="Wasserdichte Lenkertasche für Bikepacking-Touren")
    category: Optional[str] = Field(None, example="Taschen")
    weight_grams: Optional[int] = Field(None, example=450)
    price: Optional[float] = Field(None, example=89.95)
    purchase_link: Optional[str] = Field(None, example="https://www.ortlieb.com/lenkertasche")
    image_url: Optional[str] = Field(None, example="/uploads/images/lenkertasche.jpg")
    rating: Optional[int] = Field(None, ge=1, le=5, example=5)

class Equipment(EquipmentBase):
    """Schema for Equipment response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Ortlieb Lenkertasche",
                "description": "Wasserdichte Lenkertasche für Bikepacking-Touren",
                "category": "Taschen",
                "weight_grams": 450,
                "price": 89.95,
                "purchase_link": "https://www.ortlieb.com/lenkertasche",
                "image_url": "/uploads/images/lenkertasche.jpg",
                "rating": 5,
                "created_at": "2025-04-18T12:00:00Z",
                "updated_at": "2025-04-18T12:00:00Z"
            }
        }
