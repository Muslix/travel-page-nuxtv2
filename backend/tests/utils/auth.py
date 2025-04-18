# File Name: auth.py
# Relative Path: backend/tests/utils/auth.py
# Purpose: Hilfsfunktionen zur Token-Generierung für Test-User (Admin und Nicht-Admin) für automatisierte API-Tests.
# Detailed Overview: Dieses Modul stellt Funktionen bereit, um gültige JWT-Access-Tokens für Test-User zu erzeugen. Es nutzt die bestehende Token-Logik aus dem Projekt, um realistische Authentifizierungs-Header für FastAPI-Tests zu liefern. Die Tokens können in allen Testmodulen für Admin- und Nicht-Admin-User verwendet werden.

from app.core.security.jwt import create_access_token
from app.models.user_model import User
from sqlalchemy.orm import Session
from app.db.database import get_db

# Test-User-Konstanten
ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@example.com"
NON_ADMIN_USERNAME = "testuser"
NON_ADMIN_EMAIL = "testuser@example.com"


def get_or_create_test_user(db: Session, is_admin: bool = False) -> User:
    """Erstellt oder holt einen Test-User (Admin/Nicht-Admin) aus der DB."""
    from app.models.user_model import User
    username = ADMIN_USERNAME if is_admin else NON_ADMIN_USERNAME
    email = ADMIN_EMAIL if is_admin else NON_ADMIN_EMAIL
    user = db.query(User).filter_by(username=username).first()
    if not user:
        user = User(
            username=username,
            email=email,
            hashed_password="$2b$12$testhash",  # Dummy-Hash, Passwort irrelevant für Token
            is_admin=is_admin
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def generate_token_for_user(user: User) -> str:
    """Erzeugt einen gültigen JWT-Token für den angegebenen User."""
    token = create_access_token(subject=str(user.id))
    return token


def get_admin_token(db: Session) -> str:
    """Gibt einen gültigen JWT-Token für den Admin-Testuser zurück."""
    user = get_or_create_test_user(db, is_admin=True)
    return generate_token_for_user(user)


def get_non_admin_token(db: Session) -> str:
    """Gibt einen gültigen JWT-Token für den Nicht-Admin-Testuser zurück."""
    user = get_or_create_test_user(db, is_admin=False)
    return generate_token_for_user(user)
