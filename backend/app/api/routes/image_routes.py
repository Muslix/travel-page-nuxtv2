from fastapi import APIRouter, Depends, Query, Path, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.schemas import Image, GenericResponse
from app.services.image_service import ImageService

router = APIRouter(
    prefix="/api/v1/images",
    tags=["images"],
    responses={
        404: {"description": "Nicht gefunden"},
        400: {"description": "Ungültige Anfrage"},
        500: {"description": "Serverfehler"}
    },
)

@router.get("/", response_model=List[Image], summary="Alle Bilder abrufen")
async def get_images(
    skip: int = Query(0, ge=0, description="Anzahl der zu überspringenden Datensätze für Paginierung"),
    limit: int = Query(20, ge=1, le=100, description="Maximale Anzahl der zurückzugebenden Datensätze"),
    db: Session = Depends(get_db)
):
    """
    Alle Bilder abrufen mit Paginierung.
    
    - Unterstützt Paginierung über die Parameter `skip` und `limit`
    - Default: 20 Bilder pro Seite, beginnend bei 0
    
    Beispiel-Response:
    ```json
    [
      {
        "id": 1,
        "file_path": "/uploads/images/adventure_1_cover.jpg",
        "title": "Bergpanorama",
        "description": "Aussicht vom Gipfel",
        "is_cover": true,
        "adventure_id": 1,
        "equipment_id": null
      },
      ...
    ]
    ```
    """
    service = ImageService(db)
    return service.get_all_images(skip=skip, limit=limit)

@router.get("/adventure/{adventure_id}", response_model=List[Image], summary="Bilder eines Abenteuers abrufen")
async def get_adventure_images(
    adventure_id: int = Path(..., description="ID des Abenteuers"),
    db: Session = Depends(get_db)
):
    """
    Alle Bilder eines Abenteuers abrufen.
    
    - Gibt eine Liste aller Bilder zurück, die mit einem bestimmten Abenteuer verknüpft sind
    - Das Coverbild wird durch das Attribut `is_cover=true` gekennzeichnet
    
    Bei ungültiger Adventure-ID wird ein 404 Not Found zurückgegeben.
    """
    service = ImageService(db)
    return service.get_adventure_images(adventure_id)

@router.get("/equipment/{equipment_id}", response_model=List[Image], summary="Bilder eines Ausrüstungsgegenstands abrufen")
async def get_equipment_images(
    equipment_id: int = Path(..., description="ID des Ausrüstungsgegenstands"),
    db: Session = Depends(get_db)
):
    """
    Alle Bilder eines Ausrüstungsgegenstands abrufen.
    
    - Gibt eine Liste aller Bilder zurück, die mit einem bestimmten Ausrüstungsgegenstand verknüpft sind
    
    Bei ungültiger Equipment-ID wird ein 404 Not Found zurückgegeben.
    """
    service = ImageService(db)
    return service.get_equipment_images(equipment_id)

@router.get("/{image_id}", response_model=Image, summary="Einzelnes Bild abrufen")
async def get_image(
    image_id: int = Path(..., description="ID des Bildes"),
    db: Session = Depends(get_db)
):
    """
    Ein Bild anhand seiner ID abrufen.
    
    - Gibt detaillierte Informationen zu einem einzelnen Bild zurück
    
    Bei ungültiger Bild-ID wird ein 404 Not Found zurückgegeben.
    """
    service = ImageService(db)
    return service.get_image_by_id(image_id)

@router.post("/upload", response_model=Image, status_code=status.HTTP_201_CREATED, summary="Bild hochladen", 
         responses={
             201: {"description": "Bild erfolgreich hochgeladen"},
             400: {"description": "Ungültiges Bildformat oder fehlende Daten"},
             413: {"description": "Datei ist zu groß"},
             500: {"description": "Serverfehler bei der Bildverarbeitung"}
         })
async def upload_image(
    file: UploadFile = File(..., description="Die hochzuladende Bilddatei"),
    title: Optional[str] = Form(None, description="Optionaler Titel des Bildes"),
    description: Optional[str] = Form(None, description="Optionale Beschreibung des Bildes"),
    is_cover: bool = Form(False, description="Gibt an, ob das Bild als Cover verwendet werden soll"),
    adventure_id: Optional[int] = Form(None, description="ID des Abenteuers, falls das Bild mit einem Abenteuer verknüpft ist"),
    equipment_id: Optional[int] = Form(None, description="ID des Ausrüstungsgegenstands, falls das Bild mit einem Ausrüstungsgegenstand verknüpft ist"),
    db: Session = Depends(get_db)
):
    """
    Ein neues Bild hochladen und speichern.
    
    - Unterstützt gängige Bildformate (JPEG, PNG, GIF)
    - Bilder können optional mit einem Abenteuer oder Ausrüstungsgegenstand verknüpft werden
    - Das Bild kann als Cover markiert werden (is_cover=true)
    - Maximal erlaubte Dateigröße: 5MB
    
    Wichtig: Wenn is_cover=true gesetzt ist, wird bei dem verknüpften Abenteuer oder Ausrüstungsgegenstand 
    das bisherige Cover automatisch zurückgesetzt.
    
    Beispiel-Response:
    ```json
    {
      "id": 1,
      "file_path": "/uploads/images/adventure_1_cover.jpg",
      "title": "Bergpanorama",
      "description": "Aussicht vom Gipfel",
      "is_cover": true,
      "adventure_id": 1,
      "equipment_id": null
    }
    ```
    """
    service = ImageService(db)
    return await service.upload_image(
        file=file,
        title=title,
        description=description,
        is_cover=is_cover,
        adventure_id=adventure_id,
        equipment_id=equipment_id
    )

@router.put("/{image_id}", response_model=Image)
async def update_image(
    image_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    is_cover: Optional[bool] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Metadaten eines bestehenden Bildes aktualisieren.
    """
    service = ImageService(db)
    return service.update_image(
        image_id=image_id,
        title=title,
        description=description,
        is_cover=is_cover
    )

@router.delete("/{image_id}", response_model=GenericResponse)
async def delete_image(image_id: int, db: Session = Depends(get_db)):
    """
    Ein Bild löschen (Datei und Datenbankeintrag).
    """
    service = ImageService(db)
    return service.delete_image(image_id)
