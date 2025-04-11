from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas import User, UserCreate, Token
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
    responses={401: {"description": "Nicht autorisiert"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

@router.post("/token", response_model=Token, summary="Login und Token erhalten")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2-kompatible Token-Login, gibt JWT-Token zurück.
    
    - Akzeptiert Standard-OAuth2-Formular mit Benutzername und Passwort
    - Gibt ein JWT-Token zurück, das für die Authentifizierung bei geschützten Endpunkten verwendet werden kann
    
    Beispiel-Response:
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer"
    }
    ```
    
    Bei ungültigen Anmeldeinformationen wird ein 401 Unauthorized zurückgegeben.
    """
    service = AuthService(db)
    return service.create_user_token(form_data.username, form_data.password)

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED, summary="Neuen Benutzer registrieren")
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Registriert einen neuen Benutzer (nur für Admin-Registrierung).
    
    - Der erste registrierte Benutzer wird automatisch zum Admin
    - Weitere Benutzer werden als reguläre Benutzer angelegt
    - In einer Produktionsumgebung sollte dieser Endpunkt zusätzlich geschützt sein
    
    Benötigt folgende Daten im Request-Body:
    - **username**: Eindeutiger Benutzername
    - **email**: Eindeutige E-Mail-Adresse
    - **password**: Sicheres Passwort
    
    Beispiel-Request:
    ```json
    {
      "username": "admin",
      "email": "admin@example.com",
      "password": "sicheres_passwort"
    }
    ```
    
    Bei erfolgreicher Registrierung werden die Benutzerdaten ohne Passwort zurückgegeben.
    """
    service = AuthService(db)
    # Der erste Benutzer wird automatisch zum Admin
    first_user = db.query(User).first() is None
    return service.register_user(user_data, is_admin=first_user)

@router.get("/me", response_model=User, summary="Eigenes Benutzerprofil abrufen")
async def read_users_me(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Gibt Informationen über den aktuell angemeldeten Benutzer zurück.
    
    - Erfordert einen gültigen JWT-Token im Authorization-Header
    - Das Token muss als Bearer-Token übergeben werden
    
    Beispiel für Authorization-Header:
    ```
    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    ```
    
    Bei ungültigem oder abgelaufenem Token wird ein 401 Unauthorized zurückgegeben.
    """
    service = AuthService(db)
    return service.get_current_user(token)

@router.get("/admin", response_model=User, summary="Admin-Benutzerprofil abrufen")
async def read_admin_me(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Gibt Informationen über den aktuell angemeldeten Admin zurück.
    
    - Erfordert einen gültigen JWT-Token eines Benutzers mit Admin-Rechten
    - Dieser Endpunkt ist nur für Administratoren zugänglich
    
    Bei Zugriffsversuchen durch Benutzer ohne Admin-Rechte wird ein 403 Forbidden zurückgegeben.
    Bei ungültigem oder abgelaufenem Token wird ein 401 Unauthorized zurückgegeben.
    """
    service = AuthService(db)
    return service.get_current_admin(token)
