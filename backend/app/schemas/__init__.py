"""
Zentrale Importdatei für alle Pydantic-Schemas.
Diese Datei macht es einfacher, alle Schemas an einem zentralen Ort zu importieren.
"""

# Common Schemas
from app.schemas.response_schema import GenericResponse
from app.schemas.token_schema import Token, TokenData

# User Schemas
from app.schemas.user_schema import User, UserBase, UserCreate, UserUpdate

# Adventure Schemas
from app.schemas.adventure_schema import Adventure, AdventureBase, AdventureCreate, AdventureUpdate

# Tag Schemas
from app.schemas.tag_schema import Tag, TagBase, TagCreate

# Image Schemas
from app.schemas.image_schema import Image, ImageBase, ImageCreate

# Equipment Schemas
from app.schemas.equipment_schema import Equipment, EquipmentBase, EquipmentCreate, EquipmentUpdate

# Profile Schemas
from app.schemas.profile_schema import Profile, ProfileBase, ProfileCreate, ProfileUpdate

# Alle Schemas für einfachen Import exportieren
__all__ = [
    # Common
    "GenericResponse", "Token", "TokenData",
    
    # User
    "User", "UserBase", "UserCreate", "UserUpdate",
    
    # Adventure
    "Adventure", "AdventureBase", "AdventureCreate", "AdventureUpdate",
    
    # Tag
    "Tag", "TagBase", "TagCreate",
    
    # Image
    "Image", "ImageBase", "ImageCreate",
    
    # Equipment
    "Equipment", "EquipmentBase", "EquipmentCreate", "EquipmentUpdate",
    
    # Profile
    "Profile", "ProfileBase", "ProfileCreate", "ProfileUpdate"
]
