from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.image_model import Image
from fastapi import HTTPException, status

class ImageRepository:
    """Repository für Bilder"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Image]:
        """Alle Bilder abrufen"""
        return db.query(Image).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, image_id: int) -> Optional[Image]:
        """Ein Bild anhand seiner ID abrufen"""
        return db.query(Image).filter(Image.id == image_id).first()
    
    @staticmethod
    def get_by_adventure(db: Session, adventure_id: int) -> List[Image]:
        """Alle Bilder eines Abenteuers abrufen"""
        return db.query(Image).filter(Image.adventure_id == adventure_id).all()
    
    @staticmethod
    def get_by_equipment(db: Session, equipment_id: int) -> List[Image]:
        """Alle Bilder eines Ausrüstungsgegenstands abrufen"""
        return db.query(Image).filter(Image.equipment_id == equipment_id).all()
    
    @staticmethod
    def create(db: Session, file_path: str, title: str = None, description: str = None, 
               is_cover: bool = False, adventure_id: int = None, equipment_id: int = None) -> Image:
        """Ein neues Bild erstellen"""
        image = Image(
            file_path=file_path, 
            title=title, 
            description=description, 
            is_cover=is_cover,
            adventure_id=adventure_id,
            equipment_id=equipment_id
        )
        
        # Wenn das Bild als Cover markiert ist und zu einem Abenteuer gehört,
        # setzen wir alle anderen Bilder dieses Abenteuers als Nicht-Cover
        if is_cover and adventure_id:
            existing_covers = db.query(Image).filter(
                Image.adventure_id == adventure_id, 
                Image.is_cover == True
            ).all()
            for cover in existing_covers:
                cover.is_cover = False
        
        # Analog für Ausrüstungsgegenstände
        if is_cover and equipment_id:
            existing_covers = db.query(Image).filter(
                Image.equipment_id == equipment_id, 
                Image.is_cover == True
            ).all()
            for cover in existing_covers:
                cover.is_cover = False
        
        db.add(image)
        db.commit()
        db.refresh(image)
        return image
    
    @staticmethod
    def update(db: Session, image_id: int, file_path: str = None, title: str = None, 
               description: str = None, is_cover: bool = None) -> Optional[Image]:
        """Ein bestehendes Bild aktualisieren"""
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            return None
        
        # Daten aktualisieren
        if file_path:
            image.file_path = file_path
        if title is not None:
            image.title = title
        if description is not None:
            image.description = description
        
        # Cover-Status ändern
        if is_cover is not None and is_cover != image.is_cover:
            image.is_cover = is_cover
            
            # Wenn als Cover gesetzt, andere Cover zurücksetzen
            if is_cover:
                if image.adventure_id:
                    existing_covers = db.query(Image).filter(
                        Image.adventure_id == image.adventure_id, 
                        Image.id != image_id,
                        Image.is_cover == True
                    ).all()
                    for cover in existing_covers:
                        cover.is_cover = False
                
                if image.equipment_id:
                    existing_covers = db.query(Image).filter(
                        Image.equipment_id == image.equipment_id, 
                        Image.id != image_id,
                        Image.is_cover == True
                    ).all()
                    for cover in existing_covers:
                        cover.is_cover = False
        
        db.commit()
        db.refresh(image)
        return image
    
    @staticmethod
    def delete(db: Session, image_id: int) -> bool:
        """Ein Bild löschen"""
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            return False
        
        db.delete(image)
        db.commit()
        return True
