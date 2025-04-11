from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Table, Float, Date
from sqlalchemy.orm import relationship
from app.db.database import Base

adventure_tag = Table(
    'adventure_tag',
    Base.metadata,
    Column('adventure_id', Integer, ForeignKey('adventures.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    
    # Relationships
    adventures = relationship("Adventure", secondary=adventure_tag, back_populates="tags")
    
    def __repr__(self):
        return f"<Tag {self.name}>"
