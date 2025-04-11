from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from fastapi import Depends, HTTPException, status, UploadFile, File
import os
import shutil
from uuid import uuid4
from datetime import datetime

from app.db.database import get_db
from app.repositories.image_repository import ImageRepository
from app.schemas.image_schema import Image, ImageCreate
from app.core.config import settings


class ImageService:
    """Service für die Geschäftslogik rund um Bilder und Medien"""
    
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.image_repository = ImageRepository()
        # Stelle sicher, dass das Medien-Verzeichnis existiert
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    
    def get_all_images(self, skip: int = 0, limit: int = 100) -> List[Image]:
        """Alle Bilder abrufen"""
        return self.image_repository.get_all(self.db, skip, limit)
    
    def get_adventure_images(self, adventure_id: int) -> List[Image]:
        """Bilder eines Abenteuers abrufen"""
        return self.image_repository.get_by_adventure(self.db, adventure_id)
    
    def get_equipment_images(self, equipment_id: int) -> List[Image]:
        """Bilder eines Ausrüstungsgegenstands abrufen"""
        return self.image_repository.get_by_equipment(self.db, equipment_id)
    
    def get_image_by_id(self, image_id: int) -> Image:
        """Ein Bild anhand seiner ID abrufen"""
        image = self.image_repository.get_by_id(self.db, image_id)
        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bild mit ID {image_id} nicht gefunden"
            )
        return image
    
    async def upload_image(self, file: UploadFile, title: str = None, description: str = None,
                    is_cover: bool = False, adventure_id: int = None, equipment_id: int = None) -> Image:
        """Ein neues Bild hochladen und speichern"""
        # Dateityp prüfen
        if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dateityp nicht erlaubt. Erlaubte Typen: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
            )
        
        # Eindeutigen Dateinamen generieren
        original_filename = file.filename
        filename, file_extension = os.path.splitext(original_filename)
        unique_filename = f"{uuid4().hex}{file_extension}"
        
        # Unterordner nach Jahr/Monat erstellen
        today = datetime.now()
        upload_dir = os.path.join(settings.MEDIA_ROOT, str(today.year), f"{today.month:02d}")
        os.makedirs(upload_dir, exist_ok=True)
        
        # Vollständiger Dateipfad
        file_path = os.path.join(upload_dir, unique_filename)
        relative_path = os.path.join(str(today.year), f"{today.month:02d}", unique_filename)
        
        # Datei speichern
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Fehler beim Speichern der Datei: {str(e)}"
            )
        finally:
            file.file.close()
        
        # Bild in der Datenbank speichern
        try:
            image = self.image_repository.create(
                db=self.db,
                file_path=relative_path,
                title=title or original_filename,
                description=description,
                is_cover=is_cover,
                adventure_id=adventure_id,
                equipment_id=equipment_id
            )
            return image
        except Exception as e:
            # Bei Fehler die hochgeladene Datei wieder löschen
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Fehler beim Speichern des Bildes in der Datenbank: {str(e)}"
            )
    
    def update_image(self, image_id: int, title: str = None, description: str = None,
                    is_cover: bool = None) -> Image:
        """Ein bestehendes Bild aktualisieren (Metadaten)"""
        updated_image = self.image_repository.update(
            self.db, image_id, title=title, description=description, is_cover=is_cover
        )
        
        if not updated_image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bild mit ID {image_id} nicht gefunden"
            )
            
        return updated_image
    
    def delete_image(self, image_id: int) -> Dict[str, str]:
        """Ein Bild löschen (Datei und Datenbankeintrag)"""
        # Bild aus der Datenbank abrufen
        image = self.image_repository.get_by_id(self.db, image_id)
        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bild mit ID {image_id} nicht gefunden"
            )
        
        # Vollständigen Dateipfad bestimmen
        file_path = os.path.join(settings.MEDIA_ROOT, image.file_path)
        
        # Datei löschen, falls sie existiert
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                # Wenn das Löschen der Datei fehlschlägt, trotzdem mit dem Löschen aus der DB fortfahren
                print(f"Warnung: Datei {file_path} konnte nicht gelöscht werden: {str(e)}")
        
        # Bild aus der Datenbank löschen
        success = self.image_repository.delete(self.db, image_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Fehler beim Löschen des Bildes aus der Datenbank"
            )
        
        return {"detail": f"Bild mit ID {image_id} erfolgreich gelöscht"}
