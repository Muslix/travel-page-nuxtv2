# File Name: profile_routes.py
# Relative Path: backend/app/api/routes/profile_routes.py
# Purpose: API-Routen für Profil-Management (CRUD) im Blog-Backend.
# Detailed Overview: Diese Datei definiert die FastAPI-Endpunkte für das Abrufen, Erstellen, Aktualisieren und Löschen von Profilinformationen. Sie implementiert Authentifizierungs- und Autorisierungsprüfungen für Admin-Funktionen, nutzt Dependency Injection für Datenbankzugriffe und Services, und stellt eine klare Trennung zwischen öffentlichen und geschützten Routen sicher. Fehler werden explizit behandelt, und alle Endpunkte sind umfassend dokumentiert.

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

@router.post("/", response_model=Profile, status_code=status.HTTP_201_CREATED, summary="Neues Profil erstellen (Admin)")
async def create_profile(
    profile: ProfileCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Erstellt ein neues Profil. **Authentifizierung und Admin-Rechte erforderlich.**
    Gibt 403 Forbidden zurück, wenn keine Admin-Berechtigung vorliegt.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Keine Berechtigung zum Erstellen von Profilen"
        )
    service = ProfileService(db)
    return service.create_profile(profile)

@router.put("/{profile_id}", response_model=Profile, summary="Profil aktualisieren (Admin)")
async def update_profile(
    profile_id: int,
    profile: ProfileUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Aktualisiert ein bestehendes Profil. **Authentifizierung und Admin-Rechte erforderlich.**
    Gibt 403 Forbidden zurück, wenn keine Admin-Berechtigung vorliegt.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Keine Berechtigung zum Aktualisieren von Profilen"
        )
    service = ProfileService(db)
    return service.update_profile(profile_id, profile)

@router.delete("/{profile_id}", response_model=GenericResponse, summary="Profil löschen (Admin)")
async def delete_profile(
    profile_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Löscht ein Profil. **Authentifizierung und Admin-Rechte erforderlich.**
    Gibt 403 Forbidden zurück, wenn keine Admin-Berechtigung vorliegt.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Keine Berechtigung zum Löschen von Profilen"
        )
    service = ProfileService(db)
    result = service.delete_profile(profile_id)
    return GenericResponse(detail=result["detail"])
