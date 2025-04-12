from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.profile_model import Profile
from fastapi import HTTPException, status

class ProfileRepository:
    """Repository für Profile"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Profile]:
        """Alle Profile abrufen"""
        return db.query(Profile).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, profile_id: int) -> Optional[Profile]:
        """Ein Profil anhand seiner ID abrufen"""
        return db.query(Profile).filter(Profile.id == profile_id).first()

    @staticmethod
    def get_by_user_id(db: Session, user_id: int) -> Optional[Profile]:
        """Ein Profil anhand der User-ID abrufen"""
        return db.query(Profile).filter(Profile.user_id == user_id).first()
    
    @staticmethod
    def create(db: Session, profile_data: dict, user_id: int) -> Profile:
        """Ein neues Profil erstellen, verknüpft mit einer user_id"""
        # Check if profile for this user already exists
        existing_profile = ProfileRepository.get_by_user_id(db, user_id)
        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ein Profil für Benutzer-ID {user_id} existiert bereits"
            )
            
        profile = Profile(**profile_data, user_id=user_id) # Add user_id here
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile
    
    @staticmethod
    def update(db: Session, profile_id: int, profile_data: dict) -> Optional[Profile]:
        """Ein bestehendes Profil aktualisieren"""
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            return None
        
        # Optional: Prüfen auf Namens-/E-Mail-Konflikte bei Änderung

        for key, value in profile_data.items():
            setattr(profile, key, value)
        
        db.commit()
        db.refresh(profile)
        return profile
    
    @staticmethod
    def delete(db: Session, profile_id: int) -> bool:
        """Ein Profil löschen"""
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            return False
        
        db.delete(profile)
        db.commit()
        return True
