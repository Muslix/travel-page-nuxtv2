# File Name: equipment_routes.py
# Relative Path: backend/app/api/routes/equipment_routes.py
# Purpose: API-Routen für Ausrüstungs-Management (CRUD) im Blog-Backend.
# Detailed Overview: Diese Datei definiert die FastAPI-Endpunkte für das Abrufen, Erstellen, Aktualisieren und Löschen von Ausrüstungsgegenständen. Sie implementiert Authentifizierungs- und Autorisierungsprüfungen für Admin-Funktionen, nutzt Dependency Injection für Datenbankzugriffe und Services, und stellt eine klare Trennung zwischen öffentlichen und geschützten Routen sicher. Fehler werden explizit behandelt, und alle Endpunkte sind umfassend dokumentiert.


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas import Equipment, EquipmentCreate, EquipmentUpdate, GenericResponse, User
from app.services.equipment_service import EquipmentService
from app.services.auth_service import get_current_active_user

router = APIRouter(
    prefix="/api/v1/equipment",
    tags=["equipment"],
    responses={404: {"description": "Nicht gefunden"}},
)

@router.get("/", response_model=List[Equipment], summary="Alle Ausrüstungsgegenstände abrufen")
async def get_all_equipment(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Ruft eine Liste aller Ausrüstungsgegenstände ab.
    """
    service = EquipmentService(db)
    return service.get_all_equipment(skip=skip, limit=limit)

@router.get("/{equipment_id}", response_model=Equipment, summary="Ausrüstungsgegenstand per ID abrufen")
async def get_equipment_by_id(equipment_id: int, db: Session = Depends(get_db)):
    """
    Ruft einen spezifischen Ausrüstungsgegenstand anhand seiner ID ab.
    """
    service = EquipmentService(db)
    equipment = service.get_equipment_by_id(equipment_id)
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ausrüstungsgegenstand nicht gefunden")
    return equipment

@router.post("/", response_model=Equipment, status_code=status.HTTP_201_CREATED, summary="Neuen Ausrüstungsgegenstand erstellen (Admin)")
async def create_equipment(
    equipment: EquipmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Erstellt einen neuen Ausrüstungsgegenstand. **Authentifizierung und Admin-Rechte erforderlich.**
    Gibt 403 Forbidden zurück, wenn keine Admin-Berechtigung vorliegt.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Keine Berechtigung zum Erstellen von Ausrüstungsgegenständen"
        )
    service = EquipmentService(db)
    return service.create_equipment(equipment)

@router.put("/{equipment_id}", response_model=Equipment, summary="Ausrüstungsgegenstand aktualisieren (Admin)")
async def update_equipment(
    equipment_id: int,
    equipment: EquipmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Aktualisiert einen bestehenden Ausrüstungsgegenstand. **Authentifizierung und Admin-Rechte erforderlich.**
    Gibt 403 Forbidden zurück, wenn keine Admin-Berechtigung vorliegt.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Keine Berechtigung zum Aktualisieren von Ausrüstungsgegenständen"
        )
    service = EquipmentService(db)
    updated_item = service.update_equipment(equipment_id, equipment)
    if not updated_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ausrüstungsgegenstand nicht gefunden")
    return updated_item

@router.delete("/{equipment_id}", response_model=GenericResponse, summary="Ausrüstungsgegenstand löschen (Admin)")
async def delete_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Löscht einen Ausrüstungsgegenstand. **Authentifizierung und Admin-Rechte erforderlich.**
    Gibt 403 Forbidden zurück, wenn keine Admin-Berechtigung vorliegt.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Keine Berechtigung zum Löschen von Ausrüstungsgegenständen"
        )
    service = EquipmentService(db)
    deleted = service.delete_equipment(equipment_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ausrüstungsgegenstand nicht gefunden")
    return GenericResponse(detail="Ausrüstungsgegenstand erfolgreich gelöscht")

