from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.core.config import settings

# Passwort-Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token-Erstellung und Validierung
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Erstellt ein JWT-Token mit den übergebenen Daten und einer Ablaufzeit.
    
    Args:
        data: Daten, die in den Token kodiert werden sollen
        expires_delta: Optionale Gültigkeitsdauer, standardmäßig aus den Einstellungen
        
    Returns:
        JWT-Token als String
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Überprüft, ob das Klartext-Passwort mit dem gehashten Passwort übereinstimmt.
    
    Args:
        plain_password: Klartext-Passwort
        hashed_password: Gehashtes Passwort
        
    Returns:
        True, wenn das Passwort übereinstimmt, sonst False
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Erzeugt einen Hash für das übergebene Klartext-Passwort.
    
    Args:
        password: Klartext-Passwort
        
    Returns:
        Gehashtes Passwort
    """
    return pwd_context.hash(password)

def decode_token(token: str) -> dict:
    """
    Dekodiert ein JWT-Token und gibt die darin enthaltenen Daten zurück.
    
    Args:
        token: JWT-Token
        
    Returns:
        Dekodierte Daten aus dem Token
        
    Raises:
        HTTPException: Wenn das Token ungültig ist
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token konnte nicht validiert werden",
            headers={"WWW-Authenticate": "Bearer"},
        )
