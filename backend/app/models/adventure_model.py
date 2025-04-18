from sqlalchemy import Column, Integer, String, Text, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from app.db.database import Base
from app.models.tag_model import adventure_tag

class Adventure(Base):
    __tablename__ = 'adventures'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String(50), nullable=True)
    location = Column(String(255), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    duration_days = Column(Integer, nullable=True)
    distance_km = Column(Float, nullable=True)
    elevation_m = Column(Integer, nullable=True)
    difficulty = Column(String(50), nullable=True)
    surface = Column(String(50), nullable=True)
    gpx_file_path = Column(String(255), nullable=True)
    start_coordinates = Column(String(100), nullable=True)
    equipment = Column(Text, nullable=True)
    tips = Column(Text, nullable=True)
    cover_image = Column(String(255), nullable=True)
    created_at = Column(Date, nullable=True, default=date.today)
    updated_at = Column(Date, nullable=True)
    
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    images = relationship("Image", back_populates="adventure")
    tags = relationship("Tag", secondary=adventure_tag, back_populates="adventures")
    
    def __repr__(self):
        return f"<Adventure {self.title}>"
