from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.equipment_model import Equipment
from fastapi import HTTPException, status

class EquipmentRepository:
    """Repository für Ausrüstungsgegenstände"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Equipment]:
        """Alle Ausrüstungsgegenstände abrufen"""
        return db.query(Equipment).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, equipment_id: int) -> Optional[Equipment]:
        """Einen Ausrüstungsgegenstand anhand seiner ID abrufen"""
        return db.query(Equipment).filter(Equipment.id == equipment_id).first()
    
    @staticmethod
    def create(db: Session, equipment_data: dict) -> Equipment:
        """Einen neuen Ausrüstungsgegenstand erstellen"""
        # Optional: Prüfen, ob ein Gegenstand mit demselben Namen bereits existiert
        # existing = db.query(Equipment).filter(Equipment.name == equipment_data["name"]).first()
        # if existing:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail=f"Ein Ausrüstungsgegenstand mit dem Namen '{equipment_data['name']}' existiert bereits"
        #     )
            
        equipment = Equipment(**equipment_data)
        db.add(equipment)
        db.commit()
        db.refresh(equipment)
        return equipment
    
    @staticmethod
    def update(db: Session, equipment_id: int, equipment_data: dict) -> Optional[Equipment]:
        """Einen bestehenden Ausrüstungsgegenstand aktualisieren"""
        equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
        if not equipment:
            return None
        
        # Optional: Prüfen auf Namenskonflikte bei Namensänderung
        # if "name" in equipment_data and equipment_data["name"] != equipment.name:
        #     existing = db.query(Equipment).filter(Equipment.name == equipment_data["name"]).first()
        #     if existing:
        #         raise HTTPException(
        #             status_code=status.HTTP_400_BAD_REQUEST,
        #             detail=f"Ein Ausrüstungsgegenstand mit dem Namen '{equipment_data['name']}' existiert bereits"
        #         )

        for key, value in equipment_data.items():
            setattr(equipment, key, value)
        
        db.commit()
        db.refresh(equipment)
        return equipment
    
    @staticmethod
    def delete(db: Session, equipment_id: int) -> bool:
        """Einen Ausrüstungsgegenstand löschen"""
        equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
        if not equipment:
            return False
        
        db.delete(equipment)
        db.commit()
        return True
