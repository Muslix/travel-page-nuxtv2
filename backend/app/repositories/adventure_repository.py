from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.adventure_model import Adventure
from app.models.tag_model import Tag
from app.models.image_model import Image

from fastapi import HTTPException, status

class AdventureRepository:
    """Repository für Abenteuer/Touren"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[Adventure]:
        """Alle Abenteuer abrufen mit optionalem Status-Filter"""
        query = db.query(Adventure)
        if status:
            query = query.filter(Adventure.status == status)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, adventure_id: int) -> Optional[Adventure]:
        """Ein Abenteuer anhand seiner ID abrufen"""
        return db.query(Adventure).filter(Adventure.id == adventure_id).first()
    
    @staticmethod
    def get_by_slug(db: Session, slug: str) -> Optional[Adventure]:
        """Ein Abenteuer anhand seines Slugs abrufen"""
        return db.query(Adventure).filter(Adventure.slug == slug).first()
    
    @staticmethod
    def create(db: Session, adventure_data: dict, tags: List[str] = None) -> Adventure:
        """Ein neues Abenteuer erstellen"""
        # Prüfen, ob der Slug bereits existiert
        existing = db.query(Adventure).filter(Adventure.slug == adventure_data["slug"]).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ein Abenteuer mit dem Slug '{adventure_data['slug']}' existiert bereits"
            )
        
        # Abenteuer-Instanz erstellen
        adventure = Adventure(**adventure_data)
        
        # Tags hinzufügen, wenn vorhanden
        if tags:
            for tag_name in tags:
                # Existierendes Tag suchen oder neues erstellen
                tag = db.query(Tag).filter(Tag.name == tag_name).first()
                if not tag:
                    # Slug aus Tag-Namen erstellen
                    tag_slug = tag_name.lower().replace(" ", "-")
                    tag = Tag(name=tag_name, slug=tag_slug)
                    db.add(tag)
                    db.flush()  # ID generieren
                
                adventure.tags.append(tag)
        
        # In Datenbank speichern
        db.add(adventure)
        db.commit()
        db.refresh(adventure)
        return adventure
    
    @staticmethod
    def update(db: Session, adventure_id: int, adventure_data: dict, tags: List[str] = None) -> Optional[Adventure]:
        """Ein bestehendes Abenteuer aktualisieren"""
        adventure = db.query(Adventure).filter(Adventure.id == adventure_id).first()
        if not adventure:
            return None
        
        # Wenn Slug geändert wird, prüfen, ob neuer Slug bereits existiert
        if "slug" in adventure_data and adventure_data["slug"] != adventure.slug:
            existing = db.query(Adventure).filter(Adventure.slug == adventure_data["slug"]).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ein Abenteuer mit dem Slug '{adventure_data['slug']}' existiert bereits"
                )
        
        # Abenteuer-Daten aktualisieren
        for key, value in adventure_data.items():
            setattr(adventure, key, value)
        
        # Tags aktualisieren, wenn vorhanden
        if tags is not None:  # Leere Liste ist erlaubt (keine Tags)
            # Bestehende Tags entfernen
            adventure.tags = []
            
            # Neue Tags hinzufügen
            for tag_name in tags:
                tag = db.query(Tag).filter(Tag.name == tag_name).first()
                if not tag:
                    tag_slug = tag_name.lower().replace(" ", "-")
                    tag = Tag(name=tag_name, slug=tag_slug)
                    db.add(tag)
                    db.flush()
                
                adventure.tags.append(tag)
        
        db.commit()
        db.refresh(adventure)
        return adventure
    
    @staticmethod
    def delete(db: Session, adventure_id: int) -> bool:
        """Ein Abenteuer löschen"""
        adventure = db.query(Adventure).filter(Adventure.id == adventure_id).first()
        if not adventure:
            return False
        
        db.delete(adventure)
        db.commit()
        return True
