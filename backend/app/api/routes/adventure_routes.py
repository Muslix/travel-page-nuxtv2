# File Name: adventure_routes.py
# Relative Path: backend/app/api/routes/adventure_routes.py
# Purpose: API-Routen für Abenteuer-Management (CRUD) im Blog-Backend.
# Detailed Overview: Diese Datei definiert die FastAPI-Endpunkte für das Abrufen, Erstellen, Aktualisieren und Löschen von Abenteuern/Touren. Sie implementiert Authentifizierungs- und Autorisierungsprüfungen für Admin-Funktionen, nutzt Dependency Injection für Datenbankzugriffe und Services, und stellt eine klare Trennung zwischen öffentlichen und geschützten Routen sicher. Fehler werden explizit behandelt, und alle Endpunkte sind umfassend dokumentiert.

from fastapi import APIRouter, Depends, Query, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app.db.database import get_db
from app.schemas import Adventure, AdventureCreate, AdventureUpdate, GenericResponse, User
from app.services.adventure_service import AdventureService
from app.services.auth_service import get_current_active_user # Import security dependency

router = APIRouter(
    prefix="/api/v1/adventures",
    tags=["adventures"],
    responses={404: {"description": "Nicht gefunden"}},
)

@router.get("/", response_model=List[Adventure], summary="Alle Abenteuer abrufen")
async def get_adventures(
    skip: int = Query(0, ge=0, description="Wie viele Einträge übersprungen werden sollen"),
    limit: int = Query(10, ge=1, le=100, description="Maximale Anzahl der zurückgegebenen Einträge"),
    status: Optional[str] = Query(None, description="Filter nach Status: 'draft', 'published', 'planned'"),
    db: Session = Depends(get_db)
):
    """
    Ruft eine Liste aller Abenteuer/Touren ab, mit optionaler Paginierung und Statusfilterung.
    
    - **skip**: Anzahl der zu überspringenden Einträge (für Paginierung)
    - **limit**: Maximale Anzahl der zurückzugebenden Einträge
    - **status**: Optional. Filter für den Status des Abenteuers (draft, published, planned)
    
    Beispiel-Response:
    ```json
    [
      {
        "id": 1,
        "title": "Schwäbische Alb Tour",
        "slug": "schwabische-alb-tour",
        "description": "Eine wunderschöne Tour durch die Schwäbische Alb",
        "status": "published",
        "distance_km": 120.5,
        "tags": [
          {"id": 1, "name": "Bikepacking", "slug": "bikepacking"},
          {"id": 2, "name": "Schwäbische Alb", "slug": "schwabische-alb"}
        ]
      }
    ]
    ```
    """
    service = AdventureService(db)
    return service.get_all_adventures(skip=skip, limit=limit, status=status)

@router.get("/{adventure_id}", response_model=Adventure, summary="Abenteuer per ID abrufen")
async def get_adventure_by_id(adventure_id: int, db: Session = Depends(get_db)):
    """
    Ruft ein spezifisches Abenteuer anhand seiner ID ab.
    
    - **adventure_id**: Die eindeutige ID des Abenteuers
    
    Gibt ein 404 Not Found zurück, wenn das Abenteuer nicht existiert.
    """
    service = AdventureService(db)
    return service.get_adventure_by_id(adventure_id)

@router.get("/slug/{slug}", response_model=Adventure, summary="Abenteuer per Slug abrufen")
async def get_adventure_by_slug(slug: str, db: Session = Depends(get_db)):
    """
    Ruft ein spezifisches Abenteuer anhand seines Slugs ab.
    
    - **slug**: Der URL-freundliche Slug des Abenteuers (z.B. "schwarzwald-bikepacking-tour")
    
    Gibt ein 404 Not Found zurück, wenn das Abenteuer nicht existiert.
    """
    service = AdventureService(db)
    return service.get_adventure_by_slug(slug)

@router.post("/", response_model=Adventure, status_code=status.HTTP_201_CREATED, summary="Neues Abenteuer erstellen (Admin)")
async def create_adventure(
    adventure: AdventureCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Erstellt ein neues Abenteuer/Tour. **Authentifizierung und Admin-Rechte erforderlich.**
    
    - Benötigt ein AdventureCreate-Objekt im Request-Body
    - Tags können als Liste von Strings übergeben werden
    - Wenn kein Slug angegeben wird, wird er automatisch aus dem Titel generiert
    
    Gibt 403 Forbidden zurück, wenn keine Admin-Berechtigung vorliegt.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Keine Berechtigung zum Erstellen von Abenteuern"
        )
    service = AdventureService(db)
    return service.create_adventure(adventure)

@router.put("/{adventure_id}", response_model=Adventure, summary="Abenteuer aktualisieren (Admin)")
async def update_adventure(
    adventure_id: int,
    adventure_update: AdventureUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Aktualisiert ein bestehendes Abenteuer/Tour. **Authentifizierung erforderlich.**
    
    - **adventure_id**: Die eindeutige ID des zu aktualisierenden Abenteuers
    - Benötigt ein AdventureUpdate-Objekt im Request-Body
    - Nur die angegebenen Felder werden aktualisiert
    - Tags können hinzugefügt oder entfernt werden
    
    Gibt ein 404 Not Found zurück, wenn das Abenteuer nicht existiert.
    """
    service = AdventureService(db)
    
    # Überprüfen, ob Admin-Rechte vorhanden sind
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Keine Berechtigung zum Aktualisieren von Abenteuern"
        )
    
    return service.update_adventure(adventure_id, adventure_update)

@router.delete("/{adventure_id}", response_model=GenericResponse, summary="Abenteuer löschen (Admin)")
async def delete_adventure(
    adventure_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Löscht ein Abenteuer/Tour. **Authentifizierung erforderlich.**
    
    - **adventure_id**: Die eindeutige ID des zu löschenden Abenteuers
    
    Gibt ein 404 Not Found zurück, wenn das Abenteuer nicht existiert.
    """
    service = AdventureService(db)
    
    # Überprüfen, ob Admin-Rechte vorhanden sind
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Keine Berechtigung zum Löschen von Abenteuern"
        )
    
    service.delete_adventure(adventure_id)
    return {"message": f"Abenteuer mit ID {adventure_id} erfolgreich gelöscht"}
