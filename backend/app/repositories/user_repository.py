from sqlalchemy.orm import Session
from typing import Optional
from app.models.user_model import User
from app.core.security.jwt import get_password_hash, verify_password

class UserRepository:
    """Repository für die Benutzerverwaltung"""
    
    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[User]:
        """Benutzer anhand des Benutzernamens abrufen"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Benutzer anhand der E-Mail-Adresse abrufen"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        """Benutzer anhand der ID abrufen"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def create(db: Session, username: str, email: str, password: str, is_admin: bool = False) -> User:
        """Neuen Benutzer erstellen"""
        hashed_password = get_password_hash(password)
        db_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_admin=is_admin
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update(db: Session, user_id: int, user_data: dict) -> Optional[User]:
        """Bestehenden Benutzer aktualisieren"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        # Wenn ein neues Passwort angegeben wurde, dieses hashen
        if "password" in user_data:
            user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
        
        # Aktualisiere die Benutzerdaten
        for key, value in user_data.items():
            setattr(user, key, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def authenticate(db: Session, username: str, password: str) -> Optional[User]:
        """Benutzerauthentifizierung mit Benutzername und Passwort"""
        user = UserRepository.get_by_username(db, username)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
