import sys
import os
from contextlib import asynccontextmanager # Import asynccontextmanager

# Add the parent directory ('backend') to sys.path to allow imports like 'from app...'
# when running main.py directly from within the 'app' directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Existing imports ---
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.routes import adventure_routes, image_routes, auth_routes
from app.db.database import engine, Base # Import engine and Base
from alembic.config import Config as AlembicConfig # Import Alembic Config
from alembic import command as alembic_command # Import Alembic commands

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
            # raise e # Optionally re-raise to stop startup

    print("Startup tasks finished.")

    yield # Application runs here

    # --- Shutdown Logic ---
    print("Running application shutdown tasks...")
    # Add any cleanup logic here if needed (e.g., closing connections)
    print("Shutdown tasks finished.")


# --- FastAPI App Initialization ---
# Pass the lifespan manager to the FastAPI app
app = FastAPI(
    title="Schwob aufm Sattl API",
    description="API für den Bikepacking & Reise-Blog 'Schwob aufm Sattl'",
    version="0.1.0",
    openapi_url="/openapi.json", # Changed from /api/openapi.json
    docs_url="/docs",           # Changed from /api/docs
    redoc_url="/redoc",         # Changed from /api/redoc
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    contact={
        "name": "Schwob aufm Sattl",
        "url": "https://schwobaufmsattl.de",
        "email": "info@schwobaufmsattl.de",
    },
    license_info={
        "name": "Private Use",
        "url": "https://schwobaufmsattl.de",
    },
    lifespan=lifespan # Add the lifespan manager here
)

# CORS-Konfiguration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Media-Ordner erstellen, falls er nicht existiert
os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

# Media-Ordner statisch bereitstellen
app.mount("/media", StaticFiles(directory=settings.MEDIA_ROOT), name="media")

@app.get("/")
async def root():
    return {"message": "Willkommen bei der Schwob aufm Sattl API"}

# Router einbinden
app.include_router(adventure_routes.router)
app.include_router(image_routes.router)
app.include_router(auth_routes.router)
