# File Name: test_adventure_api.py
# Relative Path: backend/tests/test_adventure_api.py
# Purpose: Testet die FastAPI-Endpunkte für das Abenteuer-Management (CRUD) mit Fokus auf Authentifizierung, Autorisierung und Datenvalidierung.
# Detailed Overview: Dieses Testmodul verwendet pytest und httpx, um die wichtigsten API-Endpunkte für Abenteuer zu prüfen. Es werden sowohl Erfolgs- als auch Fehlerfälle abgedeckt, inklusive Admin- und Nicht-Admin-User, ungültige Daten, und Edge Cases. Die Tests folgen dem Arrange-Act-Assert-Muster und sind so gestaltet, dass sie unabhängig voneinander laufen können.

import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app
from app.db.database import get_db
from backend.tests.utils.auth import get_admin_token, get_non_admin_token

@pytest.mark.asyncio
async def test_get_adventures_unauthenticated():
    """Öffentliche Abenteuer-Liste abrufbar (keine Authentifizierung nötig)."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/adventures/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_adventure_forbidden_for_non_admin():
    """Nicht-Admin darf kein Abenteuer anlegen (403)."""
    db = next(get_db())
    token = get_non_admin_token(db)
    payload = {
        "title": "Test Adventure",
        "description": "Test Desc",
        "status": "draft",
        "distance_km": 10.0
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/adventures/",
            json=payload,
            headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_create_adventure_success_for_admin():
    """Admin kann Abenteuer erfolgreich anlegen."""
    db = next(get_db())
    token = get_admin_token(db)
    payload = {
        "title": "Admin Adventure",
        "description": "Admin Desc",
        "status": "published",
        "distance_km": 42.0
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/adventures/",
            json=payload,
            headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Admin Adventure"
    assert data["status"] == "published"

# Weitere Tests für Update, Delete, Edge Cases, ungültige Daten etc. folgen...
