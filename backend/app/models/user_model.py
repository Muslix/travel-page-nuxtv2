from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base
import bcrypt

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    def verify_password(self, password: str) -> bool:
        """Überprüft, ob das eingegebene Passwort korrekt ist."""
        return bcrypt.checkpw(
            password.encode('utf-8'), 
            self.hashed_password.encode('utf-8')
        )
    
    @classmethod
    def hash_password(cls, password: str) -> str:
        """Erstellt einen Hash für das Passwort."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def __repr__(self):
        return f"<User {self.username}>"
