\
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import Depends, HTTPException, status

from app.db.database import get_db
from app.repositories.equipment_repository import EquipmentRepository
from app.schemas.equipment_schema import EquipmentCreate, EquipmentUpdate, Equipment

class EquipmentService:
    """Service für die Geschäftslogik rund um Ausrüstung"""

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.equipment_repository = EquipmentRepository()

    def get_all_equipment(self, skip: int = 0, limit: int = 100) -> List[Equipment]:
        """Alle Ausrüstungsgegenstände abrufen"""
        return self.equipment_repository.get_all(self.db, skip, limit)

    def get_equipment_by_id(self, equipment_id: int) -> Optional[Equipment]:
        """Einen Ausrüstungsgegenstand anhand seiner ID abrufen"""
        equipment = self.equipment_repository.get_by_id(self.db, equipment_id)
        if not equipment:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ausrüstungsgegenstand mit ID {equipment_id} nicht gefunden"
            )
        return equipment


    def create_equipment(self, equipment_data: EquipmentCreate) -> Equipment:
        """Einen neuen Ausrüstungsgegenstand erstellen"""
        equipment_dict = equipment_data.dict()
        try:
            return self.equipment_repository.create(self.db, equipment_dict)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Fehler beim Erstellen des Ausrüstungsgegenstands: {str(e)}"
            )

    def update_equipment(self, equipment_id: int, equipment_data: EquipmentUpdate) -> Optional[Equipment]:
        """Einen bestehenden Ausrüstungsgegenstand aktualisieren"""
        existing_equipment = self.equipment_repository.get_by_id(self.db, equipment_id)
        if not existing_equipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ausrüstungsgegenstand mit ID {equipment_id} nicht gefunden"
            )

        equipment_dict = {k: v for k, v in equipment_data.dict().items() if v is not None}

        try:
            updated_equipment = self.equipment_repository.update(self.db, equipment_id, equipment_dict)
            if not updated_equipment:
                 raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Fehler beim Aktualisieren des Ausrüstungsgegenstands"
                )
            return updated_equipment
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Fehler beim Aktualisieren des Ausrüstungsgegenstands: {str(e)}"
            )

    def delete_equipment(self, equipment_id: int) -> bool:
        """Einen Ausrüstungsgegenstand löschen"""
        existing_equipment = self.equipment_repository.get_by_id(self.db, equipment_id)
        if not existing_equipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ausrüstungsgegenstand mit ID {equipment_id} nicht gefunden"
            )

        success = self.equipment_repository.delete(self.db, equipment_id)
        if not success:
             raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Fehler beim Löschen des Ausrüstungsgegenstands"
            )
        return success

