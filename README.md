# Schwob aufm Sattl – Bikepacking & Reise-Blog

## Projektüberblick
"Schwob aufm Sattl" ist ein persönlicher Blog für Bikepacking, Radreisen und Outdoor-Abenteuer. Das Projekt bietet eine moderne, responsive Webanwendung mit Nuxt.js (Frontend), FastAPI (Backend) und PostgreSQL (Datenbank). Ziel ist eine einfache, sichere Content-Verwaltung und ein attraktives Nutzererlebnis für Reiseberichte, Ausrüstung, Galerie und mehr.

## Setup & Installation
### Voraussetzungen
- Docker & Docker Compose (empfohlen für lokale Entwicklung)
- Alternativ: Node.js (>=18), Python (>=3.10), PostgreSQL (>=14)

### Schnellstart mit Docker Compose
```sh
git clone <repo-url>
cd nuxt-travel-page
docker-compose up --build
```
Frontend: http://localhost:3000  
Backend (Swagger UI): http://localhost:8000/docs

### Manuelles Setup (Entwicklung)
#### Backend (FastAPI)
```sh
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python app/db/seeds.py  # Seed-Daten einspielen
uvicorn app.main:app --reload
```
#### Frontend (Nuxt.js)
```sh
cd frontend
npm install
npm run dev
```

## Nutzung
- API-Dokumentation: http://localhost:8000/docs
- Admin-Login: /admin/login (Frontend)
- Content-Management: Über das Admin-Dashboard

## Project Map
```
├── backend/
│   ├── app/
│   │   ├── main.py — FastAPI-Entry-Point, OpenAPI-Konfiguration
│   │   ├── api/routes/ — API-Router für Abenteuer, Ausrüstung, Profile, Bilder, Auth
│   │   ├── models/ — SQLAlchemy-Modelle (1 Datei pro Tabelle)
│   │   ├── schemas/ — Pydantic-Schemas mit OpenAPI-Beispielen
│   │   ├── repositories/ — Datenbankoperationen pro Modell
│   │   ├── services/ — Business-Logik pro Domäne
│   │   ├── db/ — DB-Session, Seeds, Migrationen
│   │   └── core/ — Konfiguration, Security, JWT
│   ├── tests/ — Pytest-Tests, Auth-Token-Utils
│   └── alembic/ — Migrationen
├── frontend/
│   ├── app.vue — Nuxt-Root-Komponente
│   ├── pages/ — Seiten für Abenteuer, Galerie, Admin, etc.
│   ├── components/ — Wiederverwendbare UI-Komponenten
│   ├── layouts/ — Layouts für Admin & Public
│   ├── services/ — API-Client für Backend
│   ├── types/ — TypeScript-Interfaces
│   └── assets/ — CSS (responsive, dark mode)
├── docker-compose.yml — Dev-Setup für alle Services
├── TODO.md — Aufgaben- und Fortschrittsübersicht
└── README.md — Diese Dokumentation
```

## Entwicklung & Tests
- Siehe TODO.md für aktuelle Aufgaben
- Backend-Tests: `cd backend && pytest`
- Frontend: Hot-Reload mit `npm run dev`

## Deployment
- Siehe docker-compose.yml für Produktions-Setup
- SSL, Backups und Monitoring empfohlen

## Lizenz
MIT License

---
Für Fragen oder Beiträge: muslixlp@googlemail.com
