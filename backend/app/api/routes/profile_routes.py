from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.schemas import Profile, ProfileCreate, ProfileUpdate, GenericResponse, User
from app.services.profile_service import ProfileService
from app.services.auth_service import get_current_active_user

router = APIRouter(
    prefix="/api/v1/profiles",
    tags=["profiles"],
    responses={404: {"description": "Nicht gefunden"}},
)

@router.get("/", response_model=List[Profile], summary="Alle Profile abrufen")
async def get_all_profiles(
    skip: int = Query(0, ge=0, description="Wie viele Einträge übersprungen werden sollen"),
    limit: int = Query(10, ge=1, le=100, description="Maximale Anzahl der zurückgegebenen Einträge"),
    db: Session = Depends(get_db)
):
    """Ruft eine Liste aller Profile ab, mit optionaler Paginierung."""
    service = ProfileService(db)
    return service.get_all_profiles(skip=skip, limit=limit)

@router.get("/{profile_id}", response_model=Profile, summary="Profil per ID abrufen")
async def get_profile_by_id(profile_id: int, db: Session = Depends(get_db)):
    """Ruft ein spezifisches Profil anhand seiner ID ab."""
    service = ProfileService(db)
    return service.get_profile_by_id(profile_id)

@router.post("/", response_model=Profile, status_code=status.HTTP_201_CREATED, summary="Neues Profil erstellen (Admin/User)")
async def create_profile(
    profile: ProfileCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user) # Requires authentication
):
    """
    Erstellt ein neues Profil. **Authentifizierung erforderlich.**
    
    - TODO: Verknüpfe das Profil mit `current_user.id`?
    - TODO: Verhindere, dass ein Benutzer mehrere Profile erstellt?
    """
    service = ProfileService(db)
    # Add logic here to ensure profile.user_id matches current_user.id or handle admin creation
    # if profile.user_id != current_user.id and not current_user.is_superuser: # Example check
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to create profile for another user")
    return service.create_profile(profile)

@router.put("/{profile_id}", response_model=Profile, summary="Profil aktualisieren (Admin/Owner)")
async def update_profile(
    profile_id: int,
    profile: ProfileUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user) # Requires authentication
):
    """
    Aktualisiert ein bestehendes Profil. **Authentifizierung erforderlich.**
    
    - TODO: Stelle sicher, dass nur der Profilinhaber oder ein Admin das Profil bearbeiten kann.
    """
    service = ProfileService(db)
    # Add authorization check: Fetch profile, check if existing_profile.user_id == current_user.id or current_user.is_superuser
    return service.update_profile(profile_id, profile)

@router.delete("/{profile_id}", response_model=GenericResponse, summary="Profil löschen (Admin/Owner)")
async def delete_profile(
    profile_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user) # Requires authentication
):
    """
    Löscht ein Profil. **Authentifizierung erforderlich.**
    
    - TODO: Stelle sicher, dass nur der Profilinhaber oder ein Admin das Profil löschen kann.
    """
    service = ProfileService(db)
    # Add authorization check: Fetch profile, check if existing_profile.user_id == current_user.id or current_user.is_superuser
    result = service.delete_profile(profile_id)
    return GenericResponse(detail=result["detail"])
