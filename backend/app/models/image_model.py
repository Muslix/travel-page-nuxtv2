from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(255), nullable=False)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    is_cover = Column(Boolean, nullable=True, default=False)
    adventure_id = Column(Integer, ForeignKey('adventures.id'), nullable=True)
    equipment_id = Column(Integer, ForeignKey('equipment.id'), nullable=True)
    
    # Relationships
    adventure = relationship("Adventure", back_populates="images")
    equipment = relationship("Equipment", back_populates="images")
    
    def __repr__(self):
        return f"<Image {self.title or self.file_path}>"
