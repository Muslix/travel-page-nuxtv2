# File Name: seeds.py
# Relative Path: backend/app/db/seeds.py
# Purpose: Erstellt und befüllt die Datenbank mit Seed-Daten für Entwicklung und Tests.
# Detailed Overview: Dieses Skript legt initiale Entwicklungsdaten für Abenteuer, Ausrüstung, Profile, Tags und Benutzer in der PostgreSQL-Datenbank an. Es nutzt SQLAlchemy-Modelle und -Sessions, um realistische Beispielinhalte für das Frontend bereitzustellen. Das Skript kann mehrfach ausgeführt werden, ohne Duplikate zu erzeugen, und ist für lokale Entwicklungs- und Testumgebungen gedacht.

from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.adventure_model import Adventure
from app.models.equipment_model import Equipment
from app.models.profile_model import Profile
from app.models.tag_model import Tag
from app.models.user_model import User
from app.models.image_model import Image
from app.core.security.hashing import get_password_hash

# TODO: Passe die Seed-Daten ggf. an die aktuellen Models/Schemas an.

def seed_data(db: Session):
    """Fügt Seed-Daten für Abenteuer, Ausrüstung, Profile, Tags, User und Bilder ein."""
    # Benutzer (Admin)
    if not db.query(User).filter_by(username="admin").first():
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin1234"),
            is_admin=True
        )
        db.add(admin)
        db.commit()
    else:
        admin = db.query(User).filter_by(username="admin").first()

    # Tags
    tag_names = ["Bikepacking", "Schwäbische Alb", "Schwarzwald", "Mehrtägig"]
    tags = []
    for name in tag_names:
        tag = db.query(Tag).filter_by(name=name).first()
        if not tag:
            tag = Tag(name=name, slug=name.lower().replace(" ", "-"))
            db.add(tag)
            db.commit()
        tags.append(tag)

    # Abenteuer
    if not db.query(Adventure).filter_by(title="Schwäbische Alb Tour").first():
        adventure = Adventure(
            title="Schwäbische Alb Tour",
            slug="schwabische-alb-tour",
            description="Eine wunderschöne Tour durch die Schwäbische Alb",
            content="Ausführlicher Bericht zur Schwäbischen Alb Tour.",  # Pflichtfeld gesetzt
            status="published",
            distance_km=120.5,
            user_id=admin.id
        )
        db.add(adventure)
        db.commit()
    else:
        adventure = db.query(Adventure).filter_by(title="Schwäbische Alb Tour").first()

    # Ausrüstung
    if not db.query(Equipment).filter_by(name="Ortlieb Lenkertasche").first():
        equipment = Equipment(
            name="Ortlieb Lenkertasche",
            description="Wasserdichte Lenkertasche für Bikepacking-Touren",
            weight_g=450  # Feldname korrigiert
        )
        db.add(equipment)
        db.commit()
    else:
        equipment = db.query(Equipment).filter_by(name="Ortlieb Lenkertasche").first()

    # Profil
    if not db.query(Profile).filter_by(name="Schwob aufm Sattl").first():
        profile = Profile(
            name="Schwob aufm Sattl",
            bio="Radabenteuer, Outdoor und Bikepacking aus Schwaben."
            # user_id entfernt, da im Model nicht vorhanden
        )
        db.add(profile)
        db.commit()
    else:
        profile = db.query(Profile).filter_by(name="Schwob aufm Sattl").first()

    # Beispielbild
    if not db.query(Image).filter_by(title="Bergpanorama").first():
        image = Image(
            file_path="/uploads/images/adventure_1_cover.jpg",
            title="Bergpanorama",
            description="Aussicht vom Gipfel",
            is_cover=True,
            adventure_id=adventure.id
        )
        db.add(image)
        db.commit()

if __name__ == "__main__":
    db = next(get_db())
    seed_data(db)
    print("Seed-Daten erfolgreich eingefügt.")
