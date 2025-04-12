from datetime import timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer # Import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security.jwt import create_access_token, decode_token
from app.core.config import settings
from app.db.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import User, UserCreate
from app.schemas.token_schema import TokenData

# OAuth2 scheme definition
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

class AuthService:
    """Service für Authentifizierung und Autorisierung"""
    
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.user_repository = UserRepository()
    
    def register_user(self, user_data: UserCreate, is_admin: bool = False) -> User:
        """Registriert einen neuen Benutzer"""
        # Prüfen, ob Benutzername bereits existiert
        existing_username = self.user_repository.get_by_username(self.db, user_data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Benutzername bereits vergeben"
            )
        
        # Prüfen, ob E-Mail bereits existiert
        existing_email = self.user_repository.get_by_email(self.db, user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-Mail-Adresse bereits vergeben"
            )
        
        # Benutzer erstellen
        return self.user_repository.create(
            db=self.db,
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            is_admin=is_admin
        )
    
    def authenticate_user(self, username: str, password: str) -> User:
        """Authentifiziert einen Benutzer und gibt den Benutzer zurück, wenn die Anmeldedaten gültig sind"""
        user = self.user_repository.authenticate(self.db, username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Ungültiger Benutzername oder Passwort",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Benutzer ist deaktiviert",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
    
    def create_user_token(self, username: str, password: str) -> dict:
        """Erstellt ein JWT-Token für einen authentifizierten Benutzer"""
        user = self.authenticate_user(username, password)
        
        # Token-Daten erstellen
        token_data = {
            "sub": user.username,
            "email": user.email,
            "is_admin": user.is_admin
        }
        
        # Token erstellen
        access_token = create_access_token(
            data=token_data,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    
    def get_current_user(self, token: str) -> User:
        """Gibt den aktuellen Benutzer anhand des Tokens zurück"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token konnte nicht validiert werden",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = decode_token(token)
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except Exception: # Catch broader exceptions from decode_token if needed
            raise credentials_exception
        
        user = self.user_repository.get_by_username(self.db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

# --- Dependency Function --- 

async def get_current_active_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    FastAPI dependency to get the current active user from a token.
    Injects the user object into the route handler.
    """
    auth_service = AuthService(db=db)
    user = auth_service.get_current_user(token)
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inaktiver Benutzer")
    return user
