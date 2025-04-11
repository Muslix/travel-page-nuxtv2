from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from app.db.database import Base

class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    bio = Column(Text, nullable=True)
    avatar = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    social_links = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Profile {self.name}>"
