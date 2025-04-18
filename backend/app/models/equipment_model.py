from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

# Equipment Category Model
class EquipmentCategory(Base):
    __tablename__ = 'equipment_categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    # Relationship to equipment items
    equipment = relationship("Equipment", back_populates="category")

class Equipment(Base):
    __tablename__ = 'equipment'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    # Foreign key to equipment_categories
    category_id = Column(Integer, ForeignKey('equipment_categories.id'), nullable=True)
    category = relationship("EquipmentCategory", back_populates="equipment")
    weight_g = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)
    purchase_link = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    images = relationship("Image", back_populates="equipment")

    def __repr__(self):
        return f"<Equipment {self.name}>"
