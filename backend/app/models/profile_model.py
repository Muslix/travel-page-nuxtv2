from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    bio = Column(Text, nullable=True)
    avatar = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    # Relationship to SocialLink entries
    social_links = relationship('SocialLink', back_populates='profile', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Profile {self.name}>"

class SocialLink(Base):
    __tablename__ = 'social_links'
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    platform = Column(String(50), nullable=False)
    url = Column(String(255), nullable=False)
    profile = relationship('Profile', back_populates='social_links')
