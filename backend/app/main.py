import sys
import os
from contextlib import asynccontextmanager
from app.db.database import Base, engine, get_db
from app.api.routes import (
    adventure_routes, auth_routes, image_routes, profile_routes, equipment_routes
)
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from alembic.config import Config as AlembicConfig
from alembic import command as alembic_command

# Add the parent directory ('backend') to sys.path to allow imports like 'from app...'
# when running main.py directly from within the 'app' directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Lifespan Event Handler ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    """
    print("Running application startup tasks...")

    # --- Startup Logic ---
    # 1. Create tables based on SQLAlchemy models
    print("Ensuring database tables exist...")
    try:
        # Run table creation in a separate thread to avoid blocking asyncio event loop
        # Note: For simple cases or development, sync might be okay, but async is preferred
        # If using async database driver (like asyncpg), use its async methods here.
        # For standard sync drivers, execute in threadpool:
        # await asyncio.to_thread(Base.metadata.create_all, bind=engine)
        # For simplicity here, using sync version (might block briefly):
        Base.metadata.create_all(bind=engine)
        print("Tables checked/created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
        # Handle error appropriately, maybe raise to stop startup

    # 2. Apply Alembic migrations
    print("Attempting to apply Alembic migrations...")
    alembic_cfg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
    alembic_script_location = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "alembic"))

    print(f"Using Alembic config: {alembic_cfg_path}")
    print(f"Using Alembic script location: {alembic_script_location}")

    if not os.path.exists(alembic_cfg_path):
        print(f"Warning: Alembic config file not found at {alembic_cfg_path}. Skipping migrations.")
    elif not os.path.exists(alembic_script_location):
         print(f"Warning: Alembic script location not found at {alembic_script_location}. Skipping migrations.")
    else:
        try:
            alembic_cfg = AlembicConfig(alembic_cfg_path)
            alembic_cfg.set_main_option("script_location", alembic_script_location)
            # Run alembic upgrade in a separate thread if it's potentially blocking
            # await asyncio.to_thread(alembic_command.upgrade, alembic_cfg, "head")
            # For simplicity here, using sync version:
            alembic_command.upgrade(alembic_cfg, "head")
            print("Alembic migrations applied successfully (or database already up-to-date).")
        except Exception as e:
            print(f"Error applying Alembic migrations: {e}")
            print("Please ensure the database is running and migrations are consistent.")
        # Seed data in development environment
        from app.core.config import settings as _settings  # avoid shadowing
        if _settings.ENV == 'development':
            print("Seeding database with sample data...")
            try:
                from app.db.seeds import create_seed_data
                create_seed_data()
                print("Seed data created successfully.")
            except Exception as seed_err:
                print(f"Error seeding database: {seed_err}")
    print("Startup tasks finished.")

    yield

    # --- Shutdown Logic ---
    print("Running application shutdown tasks...")
    # Add any cleanup logic here if needed (e.g., closing connections)
    print("Shutdown tasks finished.")


# --- FastAPI App Initialization ---
app = FastAPI(
    title="Schwob aufm Sattl API",
    description="""
    API für den Bikepacking- und Reiseblog "Schwob aufm Sattl". 
    Bietet Endpunkte für Abenteuer, Ausrüstung, Profile, Galerie und Admin-Management. 
    Authentifizierung via JWT Bearer Token. 
    Siehe Beispiel-Requests und -Responses in der Dokumentation.
    """,
    version="1.0.0",
    contact={
        "name": "Projekt Schwob aufm Sattl",
        "email": "muslixlp@googlemail.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=[
        {"name": "adventures", "description": "Abenteuer/Touren-Management (CRUD)"},
        {"name": "equipment", "description": "Ausrüstungs-Management (CRUD)"},
        {"name": "profiles", "description": "Profil-Management (CRUD)"},
        {"name": "images", "description": "Bild- und Galerie-Management"},
        {"name": "auth", "description": "Authentifizierung & Token"}
    ]
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS or ["*"], # Use CORS_ORIGINS from config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth_routes.router)
app.include_router(adventure_routes.router)
app.include_router(image_routes.router)
app.include_router(profile_routes.router)
app.include_router(equipment_routes.router) # Add equipment routes

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Willkommen bei der {settings.PROJECT_NAME} API"}
