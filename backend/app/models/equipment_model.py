from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from app.db.database import Base

class Equipment(Base):
    __tablename__ = 'equipment'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    weight_g = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)
    purchase_link = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    images = relationship("Image", back_populates="equipment")
    
    def __repr__(self):
        return f"<Equipment {self.name}>"
