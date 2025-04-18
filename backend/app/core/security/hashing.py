# File Name: hashing.py
# Relative Path: backend/app/core/security/hashing.py
# Purpose: Stellt Funktionen zum sicheren Hashen und Überprüfen von Passwörtern bereit.
# Detailed Overview: Dieses Modul verwendet passlib, um Passwörter sicher mit bcrypt zu hashen und zu verifizieren. Es wird für User-Registrierung, Authentifizierung und Seed-Daten genutzt. Die Funktionen werden in Services, Seed-Skripten und beim Login verwendet.

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hash ein Passwort sicher mit bcrypt.
    :param password: Das zu hashende Klartext-Passwort.
    :return: Der bcrypt-Hash des Passworts.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Überprüft ein Passwort gegen einen Hash.
    :param plain_password: Das eingegebene Klartext-Passwort.
    :param hashed_password: Der gespeicherte Hash.
    :return: True, wenn das Passwort korrekt ist, sonst False.
    """
    return pwd_context.verify(plain_password, hashed_password)
