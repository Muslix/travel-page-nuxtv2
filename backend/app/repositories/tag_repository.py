from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.tag_model import Tag
from fastapi import HTTPException, status

class TagRepository:
    """Repository für Tags/Kategorien"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Tag]:
        """Alle Tags abrufen"""
        return db.query(Tag).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, tag_id: int) -> Optional[Tag]:
        """Ein Tag anhand seiner ID abrufen"""
        return db.query(Tag).filter(Tag.id == tag_id).first()
    
    @staticmethod
    def get_by_slug(db: Session, slug: str) -> Optional[Tag]:
        """Ein Tag anhand seines Slugs abrufen"""
        return db.query(Tag).filter(Tag.slug == slug).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Tag]:
        """Ein Tag anhand seines Namens abrufen"""
        return db.query(Tag).filter(Tag.name == name).first()
    
    @staticmethod
    def create(db: Session, name: str, slug: str = None) -> Tag:
        """Ein neues Tag erstellen"""
        # Wenn kein Slug angegeben ist, aus dem Namen generieren
        if not slug:
            slug = name.lower().replace(" ", "-")
        
        # Prüfen, ob das Tag bereits existiert
        existing = db.query(Tag).filter(Tag.slug == slug).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ein Tag mit dem Slug '{slug}' existiert bereits"
            )
        
        tag = Tag(name=name, slug=slug)
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return tag
    
    @staticmethod
    def update(db: Session, tag_id: int, name: str = None, slug: str = None) -> Optional[Tag]:
        """Ein bestehendes Tag aktualisieren"""
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if not tag:
            return None
        
        # Wenn Slug geändert wird, prüfen, ob neuer Slug bereits existiert
        if slug and slug != tag.slug:
            existing = db.query(Tag).filter(Tag.slug == slug).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ein Tag mit dem Slug '{slug}' existiert bereits"
                )
        
        # Daten aktualisieren
        if name:
            tag.name = name
        if slug:
            tag.slug = slug
        
        db.commit()
        db.refresh(tag)
        return tag
    
    @staticmethod
    def delete(db: Session, tag_id: int) -> bool:
        """Ein Tag löschen"""
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if not tag:
            return False
        
        db.delete(tag)
        db.commit()
        return True
