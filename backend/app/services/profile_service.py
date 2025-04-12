from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from app.db.database import get_db
from app.repositories.profile_repository import ProfileRepository
from app.schemas.profile_schema import ProfileCreate, ProfileUpdate, Profile

class ProfileService:
    """Service für die Geschäftslogik rund um Profile"""
    
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.profile_repository = ProfileRepository()
    
    def get_all_profiles(self, skip: int = 0, limit: int = 100) -> List[Profile]:
        """Alle Profile abrufen"""
        return self.profile_repository.get_all(self.db, skip, limit)
    
    def get_profile_by_id(self, profile_id: int) -> Profile:
        """Ein Profil anhand seiner ID abrufen"""
        profile = self.profile_repository.get_by_id(self.db, profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profil mit ID {profile_id} nicht gefunden"
            )
        return profile
    
    def create_profile(self, profile_data: ProfileCreate) -> Profile:
        """Ein neues Profil erstellen"""
        # TODO: Add logic to associate profile with a user (e.g., check if user_id exists)
        # TODO: Prevent creating multiple profiles for the same user?
        profile_dict = profile_data.dict()
        try:
            return self.profile_repository.create(self.db, profile_dict)
        except HTTPException as e:
            raise e
        except Exception as e:
            # Log the exception for debugging
            print(f"Error creating profile: {e}") 
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Fehler beim Erstellen des Profils: {str(e)}"
            )
    
    def update_profile(self, profile_id: int, profile_data: ProfileUpdate) -> Profile:
        """Ein bestehendes Profil aktualisieren"""
        # Prüfen, ob das Profil existiert
        existing_profile = self.profile_repository.get_by_id(self.db, profile_id)
        if not existing_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profil mit ID {profile_id} nicht gefunden"
            )
        
        # TODO: Add authorization check - only the owner or an admin should update?
        
        profile_dict = {k: v for k, v in profile_data.dict().items() if v is not None}
        
        try:
            updated_profile = self.profile_repository.update(self.db, profile_id, profile_dict)
            if not updated_profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f"Profil mit ID {profile_id} nicht gefunden nach Update-Versuch"
                )
            return updated_profile
        except HTTPException as e:
            raise e
        except Exception as e:
            # Log the exception for debugging
            print(f"Error updating profile: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Fehler beim Aktualisieren des Profils: {str(e)}"
            )

    def delete_profile(self, profile_id: int) -> Dict[str, str]:
        """Ein Profil löschen"""
        # Prüfen, ob das Profil existiert
        existing_profile = self.profile_repository.get_by_id(self.db, profile_id)
        if not existing_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profil mit ID {profile_id} nicht gefunden"
            )
            
        # TODO: Add authorization check - only the owner or an admin should delete?

        success = self.profile_repository.delete(self.db, profile_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Fehler beim Löschen des Profils"
            )
        
        return {"detail": f"Profil mit ID {profile_id} erfolgreich gelöscht"}
