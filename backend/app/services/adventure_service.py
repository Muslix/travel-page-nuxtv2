from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from app.db.database import get_db
from app.repositories.adventure_repository import AdventureRepository
from app.repositories.tag_repository import TagRepository
from app.schemas.adventure_schema import AdventureCreate, AdventureUpdate, Adventure
from app.utils.slug_generator import generate_slug


class AdventureService:
    """Service für die Geschäftslogik rund um Abenteuer/Touren"""
    
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.adventure_repository = AdventureRepository()
        self.tag_repository = TagRepository()
    
    def get_all_adventures(self, skip: int = 0, limit: int = 100, 
                           status: Optional[str] = None) -> List[Adventure]:
        """Alle Abenteuer abrufen mit optionalem Status-Filter"""
        return self.adventure_repository.get_all(self.db, skip, limit, status)
    
    def get_adventure_by_id(self, adventure_id: int) -> Adventure:
        """Ein Abenteuer anhand seiner ID abrufen"""
        adventure = self.adventure_repository.get_by_id(self.db, adventure_id)
        if not adventure:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Abenteuer mit ID {adventure_id} nicht gefunden"
            )
        return adventure
    
    def get_adventure_by_slug(self, slug: str) -> Adventure:
        """Ein Abenteuer anhand seines Slugs abrufen"""
        adventure = self.adventure_repository.get_by_slug(self.db, slug)
        if not adventure:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Abenteuer mit Slug '{slug}' nicht gefunden"
            )
        return adventure
    
    def create_adventure(self, adventure_data: AdventureCreate) -> Adventure:
        """Ein neues Abenteuer erstellen"""
        # Daten aus dem Pydantic-Modell in ein Dict umwandeln
        adventure_dict = adventure_data.dict(exclude={"tags"})
        
        # Wenn kein Slug angegeben ist, aus dem Titel generieren
        if not adventure_dict.get("slug"):
            adventure_dict["slug"] = generate_slug(adventure_dict["title"])
        
        # Tags aus der Anfrage extrahieren
        tags = adventure_data.tags if adventure_data.tags else []
        
        # Abenteuer erstellen
        try:
            return self.adventure_repository.create(self.db, adventure_dict, tags)
        except HTTPException as e:
            # HTTP-Ausnahmen weiterleiten
            raise e
        except Exception as e:
            # Andere Ausnahmen in HTTP-Ausnahmen umwandeln
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Fehler beim Erstellen des Abenteuers: {str(e)}"
            )
    
    def update_adventure(self, adventure_id: int, adventure_data: AdventureUpdate) -> Adventure:
        """Ein bestehendes Abenteuer aktualisieren"""
        # Prüfen, ob das Abenteuer existiert
        existing_adventure = self.adventure_repository.get_by_id(self.db, adventure_id)
        if not existing_adventure:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Abenteuer mit ID {adventure_id} nicht gefunden"
            )
        
        # Daten aus dem Pydantic-Modell in ein Dict umwandeln
        adventure_dict = {k: v for k, v in adventure_data.dict(exclude={"tags"}).items() if v is not None}
        
        # Wenn der Titel geändert wurde und kein neuer Slug angegeben ist, neuen Slug generieren
        if "title" in adventure_dict and "slug" not in adventure_dict:
            adventure_dict["slug"] = generate_slug(adventure_dict["title"])
        
        # Tags aus der Anfrage extrahieren
        tags = None
        if hasattr(adventure_data, "tags") and adventure_data.tags is not None:
            tags = adventure_data.tags
        
        # Abenteuer aktualisieren
        try:
            updated_adventure = self.adventure_repository.update(self.db, adventure_id, adventure_dict, tags)
            if not updated_adventure:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Fehler beim Aktualisieren des Abenteuers"
                )
            return updated_adventure
        except HTTPException as e:
            # HTTP-Ausnahmen weiterleiten
            raise e
        except Exception as e:
            # Andere Ausnahmen in HTTP-Ausnahmen umwandeln
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Fehler beim Aktualisieren des Abenteuers: {str(e)}"
            )
    
    def delete_adventure(self, adventure_id: int) -> None:
        """Ein Abenteuer löschen"""
        # Prüfen, ob das Abenteuer existiert
        existing_adventure = self.adventure_repository.get_by_id(self.db, adventure_id)
        if not existing_adventure:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Abenteuer mit ID {adventure_id} nicht gefunden"
            )
        
        # Abenteuer löschen
        try:
            success = self.adventure_repository.delete(self.db, adventure_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Fehler beim Löschen des Abenteuers"
                )
        except HTTPException as e:
            # HTTP-Ausnahmen weiterleiten
            raise e
        except Exception as e:
            # Andere Ausnahmen in HTTP-Ausnahmen umwandeln
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Fehler beim Löschen des Abenteuers: {str(e)}"
            )
