"""Alembic-Konfiguration für Datenbankmigrationen"""

import sys, os
# Add backend/app parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Importiere explizit alle Models, damit Alembic sie für Autogenerate erkennt
from app.models import user_model, adventure_model, equipment_model, image_model, profile_model, tag_model
from app.db.database import Base # Import Base from your database setup
from app.core.config import settings

# Alembic-Konfiguration
config = context.config

# Verbindung mit der DATABASE_URL aus den Einstellungen überschreiben
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Metadaten für die automatische Generierung von Migrationen hinzufügen
target_metadata = Base.metadata # Use the imported Base's metadata

def run_migrations_offline():
    """
    Ausführung von Migrationen im 'offline'-Modus.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Ausführung von Migrationen im 'online'-Modus.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
