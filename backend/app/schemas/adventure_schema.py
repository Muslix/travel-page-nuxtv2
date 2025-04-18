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
    status: str  # Neu: Adventure status
    featured_image_url: Optional[str] = None
    distance_km: Optional[float] = None  # Neu: Distanz in Kilometern
    elevation_m: Optional[int] = None     # Neu: Höhenmeter
    duration_days: Optional[int] = None
    location: Optional[str] = None
    
class AdventureCreate(AdventureBase):
    """Schema for creating a new adventure"""
    tags: Optional[List[Union[int, str]]] = Field(
        default_factory=list,
        example=["Bikepacking", "Schwäbische Alb"]
    )

class AdventureUpdate(BaseModel):
    """Schema for updating an existing adventure"""
    title: Optional[str] = Field(None, example="Neue Tour")
    description: Optional[str] = Field(None, example="Kurze Beschreibung der Tour")
    content: Optional[str] = Field(None, example="Detaillierte Beschreibung ...")
    status: Optional[str] = Field(None, example="draft")  # Neu: Adventure status
    featured_image_url: Optional[str] = Field(None, example="/uploads/images/cover.jpg")
    distance_km: Optional[float] = Field(None, example=120.5)  # Neu: Distanz in Kilometern
    elevation_m: Optional[int] = Field(None, example=1800)    # Neu: Höhenmeter
    duration_days: Optional[int] = Field(None, example=3)
    location: Optional[str] = Field(None, example="Schwäbische Alb")
    tags: Optional[List[Union[int, str]]] = Field(None, example=["Bikepacking"]) 

class Adventure(AdventureBase):
    """Schema for Adventure response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    tags: List[Tag] = Field(default_factory=list, example=[{"id": 1, "name": "Bikepacking"}])
    # Diese Schema-Erweiterungen stellen sicher, dass Antwort das Feld status und Distanz/Höhenmeter enthält

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Schwäbische Alb Tour",
                "slug": "schwabische-alb-tour",
                "description": "Eine wunderschöne Tour durch die Schwäbische Alb",
                "content": "Detaillierte Beschreibung ...",
                "status": "published",
                "featured_image_url": "/uploads/images/cover.jpg",
                "distance_km": 120.5,
                "elevation_m": 1800,
                "duration_days": 3,
                "location": "Schwäbische Alb",
                "tags": [
                    {"id": 1, "name": "Bikepacking"},
                    {"id": 2, "name": "Schwäbische Alb"}
                ],
                "created_at": "2025-04-18T12:00:00Z",
                "updated_at": "2025-04-18T12:00:00Z"
            }
        }
