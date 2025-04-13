"""
Seed-Skript zum Erstellen von Testdaten für die Entwicklung.
Dieses Skript füllt die Datenbank mit Beispieldaten für Abenteuer, Ausrüstung, Bilder, etc.

Ausführung: python -m app.db.seeds
"""

import sys
import os
import random
from datetime import datetime, timedelta

# Pfade für Import korrekt setzen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy.orm import Session
from app.db.database import get_db, engine, Base
from app.models.user_model import User
from app.models.adventure_model import Adventure
from app.models.tag_model import Tag
from app.models.equipment_model import Equipment, EquipmentCategory
from app.models.profile_model import Profile, SocialLink
from app.models.image_model import Image
from app.core.security.jwt import get_password_hash

def create_seed_data():
    """Hauptfunktion zum Erstellen der Seed-Daten"""
    
    print("*** SEED SCRIPT STARTING ***")
    
    # Session aus dem Datenbankkontext holen
    try:
        print("Verbindung zur Datenbank wird hergestellt...")
        db = next(get_db())
        print("Datenbankverbindung erfolgreich hergestellt!")
    except Exception as e:
        print(f"FEHLER bei der Datenbankverbindung: {str(e)}")
        return
    
    try:
        print("Erstelle Seed-Daten...")
        
        # Bestehende Daten prüfen
        if db.query(User).count() > 0:
            print("Es sind bereits Daten in der Datenbank vorhanden.")
            print("Bestehende Daten werden überschrieben...")
        
        # Daten erzeugen
        create_users(db)
        create_tags(db)
        create_equipment_categories(db)
        create_equipment(db)
        create_profiles(db)
        create_adventures(db)
        
        print("Seed-Daten erfolgreich erstellt!")
    
    except Exception as e:
        print(f"Fehler beim Erstellen der Seed-Daten: {str(e)}")
        db.rollback()
    finally:
        db.close()

def create_users(db: Session):
    """Admin-Benutzer anlegen"""
    
    print("Erstelle Benutzer...")
    
    # Bestehende User löschen
    db.query(User).delete()
    db.commit()
    
    # Admin-Benutzer erstellen
    admin = User(
        username="admin",
        email="muslixlp@googlemail.com",
        hashed_password=get_password_hash("adminpassword"),
        is_active=True,
        is_admin=True
    )
    
    # Test-Benutzer erstellen
    test_user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        is_active=True,
        is_admin=False
    )
    
    db.add(admin)
    db.add(test_user)
    db.commit()
    
    print(f"Benutzer erstellt: {admin.username}, {test_user.username}")

def create_tags(db: Session):
    """Tags für Abenteuer erstellen"""
    
    print("Erstelle Tags...")
    
    # Bestehende Tags löschen
    db.query(Tag).delete()
    db.commit()
    
    # Liste von typischen Bikepacking/Reise-Tags
    tags_data = [
        {"name": "Bikepacking", "slug": "bikepacking"},
        {"name": "Schwarzwald", "slug": "schwarzwald"},
        {"name": "Alpen", "slug": "alpen"},
        {"name": "Radreise", "slug": "radreise"},
        {"name": "Gravelbike", "slug": "gravelbike"},
        {"name": "Mountainbike", "slug": "mountainbike"},
        {"name": "Fernradweg", "slug": "fernradweg"},
        {"name": "Mehrtagestour", "slug": "mehrtagestour"},
        {"name": "Baden-Württemberg", "slug": "baden-wuerttemberg"},
        {"name": "Bayern", "slug": "bayern"},
        {"name": "Österreich", "slug": "oesterreich"},
        {"name": "Schweiz", "slug": "schweiz"},
        {"name": "Italien", "slug": "italien"},
        {"name": "Frankreich", "slug": "frankreich"},
        {"name": "Camping", "slug": "camping"},
        {"name": "Ultraleicht", "slug": "ultraleicht"},
        {"name": "Tagesausflug", "slug": "tagesausflug"},
        {"name": "Rennrad", "slug": "rennrad"}
    ]
    
    for tag_data in tags_data:
        tag = Tag(**tag_data)
        db.add(tag)
    
    db.commit()
    print(f"{len(tags_data)} Tags erstellt")

def create_equipment_categories(db: Session):
    """Ausrüstungskategorien erstellen"""
    
    print("Erstelle Ausrüstungskategorien...")
    
    # Bestehende Kategorien löschen
    db.query(EquipmentCategory).delete()
    db.commit()
    
    # Kategorien definieren
    categories_data = [
        {"name": "Fahrrad", "slug": "fahrrad", "description": "Verschiedene Fahrradtypen und Rahmen"},
        {"name": "Bikepacking-Taschen", "slug": "bikepacking-taschen", "description": "Taschen für Bikepacking-Touren"},
        {"name": "Camping", "slug": "camping", "description": "Camping-Ausrüstung wie Zelte, Schlafsäcke, Kocher etc."},
        {"name": "Bekleidung", "slug": "bekleidung", "description": "Funktionskleidung für Radreisen"},
        {"name": "Navigation", "slug": "navigation", "description": "GPS-Geräte, Smartphone-Halterungen und Apps"},
        {"name": "Werkzeug", "slug": "werkzeug", "description": "Werkzeug und Reparatur-Sets für unterwegs"},
        {"name": "Elektronik", "slug": "elektronik", "description": "Kameras, Powerbanks, Ladegeräte etc."},
        {"name": "Packsäcke", "slug": "packsaecke", "description": "Wasserdichte Packsäcke und Organisationshilfen"}
    ]
    
    for cat_data in categories_data:
        category = EquipmentCategory(**cat_data)
        db.add(category)
    
    db.commit()
    print(f"{len(categories_data)} Ausrüstungskategorien erstellt")

def create_equipment(db: Session):
    """Ausrüstungsitems erstellen"""
    
    print("Erstelle Ausrüstungsitems...")
    
    # Bestehende Ausrüstung löschen
    db.query(Equipment).delete()
    db.commit()
    
    # Kategorien abrufen
    categories = db.query(EquipmentCategory).all()
    cat_by_slug = {cat.slug: cat for cat in categories}
    
    # Ausrüstungsitems definieren
    equipment_data = [
        {
            "name": "Specialized Diverge",
            "slug": "specialized-diverge",
            "description": "Mein Gravelbike für Bikepacking-Touren",
            "details": """# Specialized Diverge
Ein vielseitiges Gravelbike, das sich perfekt für längere Bikepacking-Touren eignet.

## Technische Daten
- Rahmen: Specialized Diverge Carbon
- Schaltung: Shimano GRX 2x11
- Bremsen: Hydraulische Scheibenbremsen
- Laufräder: DT Swiss G1800
- Reifen: WTB Riddler 45c tubeless

## Erfahrungen
Hat mich bisher auf allen Abenteuern zuverlässig begleitet und ist sowohl auf Asphalt als auch auf Schotter eine wahre Freude.
""",
            "rating": 5,
            "price": 2800.00,
            "purchase_date": datetime(2022, 3, 15),
            "weight_grams": 9200,
            "category_id": cat_by_slug["fahrrad"].id
        },
        {
            "name": "Ortlieb Seat-Pack",
            "slug": "ortlieb-seat-pack",
            "description": "Wasserdichte Satteltasche mit 16,5 Liter Volumen",
            "details": """# Ortlieb Seat-Pack
Eine robuste, wasserdichte Satteltasche für Bikepacking-Abenteuer.

## Spezifikationen
- Volumen: 16,5 Liter
- Gewicht: 456g
- Material: PU-beschichtetes Nylon
- Wasserdicht (IP64)

## Vorteile
- Absolut wasserdicht
- Stabil auch bei holprigen Abfahrten
- Einfache Montage
- Gutes Packvolumen

## Nachteile
- Etwas schwerer als manche Alternativen
- Keine externen Taschen für Kleinteile
""",
            "rating": 5,
            "price": 135.00,
            "purchase_date": datetime(2022, 4, 10),
            "weight_grams": 456,
            "category_id": cat_by_slug["bikepacking-taschen"].id
        },
        {
            "name": "MSR Hubba Hubba NX2",
            "slug": "msr-hubba-hubba-nx2",
            "description": "Leichtes 2-Personen-Zelt für Bikepacking und Trekking",
            "details": """# MSR Hubba Hubba NX2
Ein ultraleichtes 2-Personen-Zelt, das sich hervorragend für Bikepacking eignet.

## Technische Daten
- Gewicht: 1,72 kg
- Packmaß: 46 x 15 cm
- Innenfläche: 2,7 m²
- 2 Eingänge und 2 Apsiden

## Erfahrungen
Das Zelt bietet ein ausgezeichnetes Verhältnis von Gewicht zu Komfort. Es ist schnell aufgebaut, bietet guten Wetterschutz und ist dabei kompakt genug, um es problemlos am Fahrrad zu transportieren.
""",
            "rating": 4,
            "price": 430.00,
            "purchase_date": datetime(2022, 5, 3),
            "weight_grams": 1720,
            "category_id": cat_by_slug["camping"].id
        },
        {
            "name": "Topeak Mini 20 Pro",
            "slug": "topeak-mini-20-pro",
            "description": "Kompaktes Multi-Tool mit 20 Funktionen",
            "details": """# Topeak Mini 20 Pro
Ein vielseitiges Multi-Tool für unterwegs.

## Funktionen
- Verschiedene Inbus-Schlüssel (2-8mm)
- Torx T10, T15, T25
- Kreuz- und Schlitzschraubendreher
- Kettennieter
- Reifenheber
- Speichenschlüssel

## Vorteile
- Robust und langlebig
- Kompakte Größe
- Umfassende Werkzeugausstattung
- Praktische Tasche inklusive
""",
            "rating": 5,
            "price": 39.99,
            "purchase_date": datetime(2022, 3, 20),
            "weight_grams": 163,
            "category_id": cat_by_slug["werkzeug"].id
        },
        {
            "name": "Garmin eTrex 32x",
            "slug": "garmin-etrex-32x",
            "description": "Robustes GPS-Gerät für Navigation im Gelände",
            "details": """# Garmin eTrex 32x
Ein zuverlässiger GPS-Begleiter für alle Outdoor-Abenteuer.

## Technische Daten
- 2,2" Farbdisplay
- 8 GB interner Speicher
- Bis zu 25 Stunden Akkulaufzeit (2 AA-Batterien)
- Barometrischer Höhenmesser und 3-Achsen-Kompass
- Wasserdicht nach IPX7

## Erfahrungen
Vor allem in Regionen mit schlechtem Handyempfang ist das eTrex ein unverzichtbarer Begleiter. Die Kartendarstellung ist klar und präzise, die Batterielaufzeit beeindruckend.
""",
            "rating": 4,
            "price": 249.99,
            "purchase_date": datetime(2021, 11, 15),
            "weight_grams": 142,
            "category_id": cat_by_slug["navigation"].id
        }
    ]
    
    for equip_data in equipment_data:
        equipment = Equipment(**equip_data)
        db.add(equipment)
    
    db.commit()
    print(f"{len(equipment_data)} Ausrüstungsitems erstellt")

def create_profiles(db: Session):
    """Profile und Social-Links erstellen"""
    
    print("Erstelle Profile...")
    
    # Bestehende Profile löschen
    db.query(SocialLink).delete()
    db.query(Profile).delete()
    db.commit()
    
    # Haupt-Profil erstellen
    main_profile = Profile(
        name="Michael",
        slug="michael",
        biography="""# Schwob aufm Sattl
Hallo, ich bin Michael, ein begeisterter Radfahrer aus dem schönen Schwaben!

## Meine Leidenschaft
Seit einigen Jahren entdecke ich die Welt mit dem Gravelbike und liebe es, Bikepacking-Abenteuer zu erleben. Egal ob kurze Wochenendtrips im Schwarzwald oder längere Touren durch die Alpen – auf dem Sattel fühle ich mich zu Hause.

## Über diesen Blog
Auf "Schwob aufm Sattl" teile ich meine Erfahrungen, Routen, Ausrüstungstipps und Geschichten von unterwegs. Mein Ziel ist es, andere zu inspirieren, selbst das Abenteuer auf zwei Rädern zu suchen.

## Lieblings-Reviere
- Schwarzwald
- Schwäbische Alb
- Alpen
- Fernradwege in Europa

Ich freue mich, wenn du mit mir auf Entdeckungsreise gehst!
""",
        avatar_url="/media/profile/michael_avatar.jpg",
        is_main_profile=True
    )
    
    db.add(main_profile)
    db.flush()  # ID generieren, ohne Commit
    
    # Social-Links für das Hauptprofil erstellen
    social_links = [
        {
            "platform": "youtube",
            "url": "https://youtube.com/@schwobaufmsattl",
            "profile_id": main_profile.id
        },
        {
            "platform": "instagram",
            "url": "https://instagram.com/schwobaufmsattl",
            "profile_id": main_profile.id
        },
        {
            "platform": "strava",
            "url": "https://www.strava.com/athletes/schwobaufmsattl",
            "profile_id": main_profile.id
        }
    ]
    
    for link_data in social_links:
        social_link = SocialLink(**link_data)
        db.add(social_link)
    
    # Zweites Profil für Gastbeiträge
    guest_profile = Profile(
        name="Sarah",
        slug="sarah",
        biography="""# Sarah - Gast-Autor
Hallo, ich bin Sarah und gelegentliche Mitfahrerin und Gastbloggerin bei "Schwob aufm Sattl".

## Über mich
Als begeisterte Mountainbikerin bin ich am liebsten auf Singletrails unterwegs, begleite Michael aber auch gerne auf seinen Bikepacking-Abenteuern.

## Meine Beiträge
In meinen Gastbeiträgen teile ich vor allem meine Erfahrungen zum Thema:
- Mountainbiking für Frauen
- Leichte Ausrüstung
- Fotografie unterwegs
""",
        avatar_url="/media/profile/sarah_avatar.jpg",
        is_main_profile=False
    )
    
    db.add(guest_profile)
    db.commit()
    print(f"2 Profile mit {len(social_links)} Social-Links erstellt")

def create_adventures(db: Session):
    """Abenteuer/Touren mit Tags erstellen"""
    
    print("Erstelle Abenteuer...")
    
    # Bestehende Abenteuer löschen
    db.query(Adventure).delete()
    db.commit()
    
    # Alle Tags abrufen
    all_tags = db.query(Tag).all()
    tags_by_name = {tag.name: tag for tag in all_tags}
    
    # Profile abrufen
    main_profile = db.query(Profile).filter(Profile.is_main_profile == True).first()
    guest_profile = db.query(Profile).filter(Profile.is_main_profile == False).first()
    
    # Abenteuer-Daten
    adventures_data = [
        {
            "title": "Schwarzwald Traverse",
            "slug": "schwarzwald-traverse",
            "description": "Eine dreitägige Bikepacking-Tour durch den nördlichen Schwarzwald",
            "content": """# Schwarzwald Traverse - Drei Tage durch den Nordschwarzwald

Eine epische Bikepacking-Route durch einen der schönsten Mittelgebirge Deutschlands.

## Die Route

Die Tour beginnt in Baden-Baden und führt über Forbach, Freudenstadt und Alpirsbach nach Schramberg. Sie umfasst etwa 180 Kilometer mit 4.500 Höhenmetern und führt über spektakuläre Aussichtspunkte, durch dichte Wälder und entlang malerischer Flusstäler.

## Tag 1: Baden-Baden nach Forbach (55 km, 1.500 hm)

Der erste Tag beginnt mit einem anspruchsvollen Anstieg auf die Hornisgrinde, dem höchsten Berg im Nordschwarzwald. Von hier aus genießt man einen atemberaubenden Blick auf die Rheinebene. Nach einer rasanten Abfahrt erreicht man das idyllische Murgtal und folgt dem Fluss bis nach Forbach.

## Tag 2: Forbach nach Alpirsbach (70 km, 1.800 hm)

Am zweiten Tag geht es zunächst über den Hohlohturm nach Freudenstadt. Nach einer Mittagspause führt die Route weiter durch das wildromantische Kinzigtal nach Alpirsbach, wo die berühmte Klosterbrauerei zu einer Besichtigung einlädt.

## Tag 3: Alpirsbach nach Schramberg (55 km, 1.200 hm)

Der letzte Tag führt durch einige der einsamsten Gebiete des Schwarzwalds. Über schmale Waldwege und versteckte Pfade erreicht man schließlich Schramberg, den Endpunkt der Tour.

## Übernachtungen

- Nacht 1: Campingplatz am Murgtal in Forbach
- Nacht 2: Jugendherberge Alpirsbach

## Beste Reisezeit

Mai bis Oktober, wobei der Herbst mit seiner Farbenpracht besonders empfehlenswert ist.

## Ausrüstung

- Gravelbike oder Hardtail-MTB
- Bikepacking-Taschen (Rahmen-, Lenker- und Satteltasche)
- Leichtes Camping-Equipment
- Regenbekleidung (auch im Sommer!)
- Ausreichend Wasservorrat für lange Abschnitte ohne Versorgungsmöglichkeiten

## Hinweise

Die Tour ist technisch nicht sehr anspruchsvoll, erfordert aber eine gute Kondition aufgrund der vielen Höhenmeter. GPS-Navigation wird empfohlen, da einige Abschnitte auf kleinen, wenig befahrenen Wegen verlaufen.
""",
            "status": "published",
            "location": "Schwarzwald, Baden-Württemberg",
            "distance_km": 180.0,
            "elevation_m": 4500,
            "duration_days": 3,
            "difficulty": "mittel",
            "featured_image_path": "/media/adventures/schwarzwald_traverse_main.jpg",
            "created_at": datetime.now() - timedelta(days=60),
            "updated_at": datetime.now() - timedelta(days=58),
            "published_at": datetime.now() - timedelta(days=58),
            "profile_id": main_profile.id,
            "tags": [tags_by_name["Bikepacking"], tags_by_name["Schwarzwald"], tags_by_name["Mehrtagestour"], tags_by_name["Baden-Württemberg"], tags_by_name["Gravelbike"]]
        },
        {
            "title": "Alpenüberquerung: Von Garmisch nach Riva",
            "slug": "alpenueberquerung-garmisch-riva",
            "description": "Die klassische MTB-Transalp von Deutschland nach Italien",
            "content": """# Alpenüberquerung: Von Garmisch nach Riva del Garda

Die Königsdisziplin des Bikepacking - eine Überquerung der Alpen von Nord nach Süd.

## Die Route

Diese 7-tägige Tour führt von Garmisch-Partenkirchen in Deutschland über Österreich bis nach Riva del Garda in Italien. Mit etwa 380 Kilometern und 11.000 Höhenmetern ist sie eine echte Herausforderung für ambitionierte Mountainbiker.

## Tag 1: Garmisch-Partenkirchen nach Ehrwald (45 km, 1.200 hm)

Der erste Tag beginnt in Garmisch und führt zunächst zum Fuß der Zugspitze. Über die Ehrwalder Alm geht es weiter nach Ehrwald, wo wir die erste Nacht verbringen.

## Tag 2: Ehrwald nach Ischgl (65 km, 1.900 hm)

Von Ehrwald aus durchqueren wir das Lechtal und nehmen den herausfordernden Anstieg zur Heilbronner Hütte. Nach einer anspruchsvollen Abfahrt erreichen wir Ischgl.

## Tag 3-7: [weitere Etappenbeschreibungen folgen]

## Übernachtungen

Wir übernachten in einer Mischung aus Berghütten und kleinen Pensionen:

- Nacht 1: Gasthof in Ehrwald
- Nacht 2: Sporthotel in Ischgl
- Nacht 3: Berghütte am Fimberpass
- Nacht 4: Hotel in Santa Maria
- Nacht 5: Rifugio am Passo Montozzo
- Nacht 6: Pension in Dimaro
- Nacht 7: Ziel in Riva del Garda

## Beste Reisezeit

Juli bis September, wenn die hohen Pässe schneefrei sind.

## Ausrüstung

- Mountainbike mit mindestens 120mm Federweg
- Bikepacking-Taschen oder leichter Rucksack
- Wechselkleidung und Regenbekleidung
- Erste-Hilfe-Set und Notfallausrüstung
- Karten und GPS-Navigation

## Hinweise

Diese Tour erfordert sowohl technisches Fahrkönnen als auch sehr gute Kondition. Einige Abschnitte (insbesondere am Fimberpass und Passo Montozzo) können Schiebepassagen enthalten.
""",
            "status": "published",
            "location": "Alpen (Deutschland, Österreich, Italien)",
            "distance_km": 380.0,
            "elevation_m": 11000,
            "duration_days": 7,
            "difficulty": "schwer",
            "featured_image_path": "/media/adventures/transalp_main.jpg",
            "created_at": datetime.now() - timedelta(days=120),
            "updated_at": datetime.now() - timedelta(days=118),
            "published_at": datetime.now() - timedelta(days=118),
            "profile_id": main_profile.id,
            "tags": [tags_by_name["Bikepacking"], tags_by_name["Alpen"], tags_by_name["Mehrtagestour"], tags_by_name["Mountainbike"], tags_by_name["Italien"], tags_by_name["Österreich"], tags_by_name["Bayern"]]
        },
        {
            "title": "Schönbuch Gravel Runde",
            "slug": "schonbuch-gravel-runde",
            "description": "Tagestrip durch den Naturpark Schönbuch",
            "content": """# Schönbuch Gravel Runde

Eine perfekte Tagestour durch den Naturpark Schönbuch bei Stuttgart - ideal für Gravelbikes.

## Die Route

Diese 85 Kilometer lange Rundtour mit etwa 950 Höhenmetern führt durch einen der größten zusammenhängenden Waldgebiete Süddeutschlands. Start- und Zielpunkt ist Tübingen.

## Routenbeschreibung

Die Route beginnt in Tübingen und führt zunächst am Neckar entlang bis Lustnau. Von dort geht es hinauf in den Schönbuch, wo uns ein Netz aus gut ausgebauten Forstwegen erwartet. Über Bebenhausen und das idyllische Goldersbachtal erreichen wir Herrenberg an der Westseite des Naturparks.

Nach einer Kaffeepause in Herrenberg führt die Route wieder zurück in den Wald, vorbei am Naturfreundehaus Herrenberg und durch den südlichen Teil des Schönbuchs. Über Ammerbuch-Entringen und Unterjesingen kehren wir schließlich nach Tübingen zurück.

## Highlights

- Das mittelalterliche Kloster Bebenhausen
- Das wildromantische Goldersbachtal
- Der historische Marktplatz von Herrenberg
- Zahlreiche Aussichtspunkte mit Blick auf die Schwäbische Alb

## Beste Reisezeit

Die Tour ist von April bis November gut fahrbar. Im Herbst bietet der Laubwald eine besonders schöne Kulisse.

## Verpflegung

- Einkehrmöglichkeiten in Bebenhausen (Waldhorn)
- Cafés und Restaurants in Herrenberg
- Biergarten in Entringen
- Zahlreiche Brunnen im Schönbuch für Wasserversorgung

## Schwierigkeit

Die Tour ist technisch einfach und auch für Einsteiger geeignet. Die Steigungen sind meist moderat, nur wenige kurze Anstiege erfordern etwas mehr Kraft.

## Fahrradempfehlung

Ideales Terrain für Gravelbikes. Mit einem Rennrad sind einige Abschnitte zu rau, mit einem MTB ist man fast "überequipt".
""",
            "status": "published",
            "location": "Schönbuch, Baden-Württemberg",
            "distance_km": 85.0,
            "elevation_m": 950,
            "duration_days": 1,
            "difficulty": "leicht",
            "featured_image_path": "/media/adventures/schonbuch_main.jpg",
            "created_at": datetime.now() - timedelta(days=30),
            "updated_at": datetime.now() - timedelta(days=28),
            "published_at": datetime.now() - timedelta(days=28),
            "profile_id": main_profile.id,
            "tags": [tags_by_name["Gravelbike"], tags_by_name["Tagesausflug"], tags_by_name["Baden-Württemberg"]]
        },
        {
            "title": "Die besten Singletrails im Schwarzwald",
            "slug": "beste-singletrails-schwarzwald",
            "description": "Ein Guide zu den aufregendsten MTB-Trails im Schwarzwald",
            "content": """# Die besten Singletrails im Schwarzwald

*Ein Gastbeitrag von Sarah*

Als Mountainbikerin bin ich ständig auf der Suche nach spannenden Trails. Der Schwarzwald hat einige der besten Singletrails in Deutschland zu bieten, und ich möchte meine Top 5 mit euch teilen.

## 1. Brandenkopf Trail

**Schwierigkeit:** S2
**Länge:** 3,5 km
**Höhenunterschied:** 450 m

Der Brandenkopf-Trail beginnt am gleichnamigen Berg und schlängelt sich durch dichten Nadelwald hinunter ins Tal. Mit einer guten Mischung aus flowigen Passagen und technischen Abschnitten ist er der perfekte Trail für fortgeschrittene Biker.

## 2. Canadian Trail Bad Wildbad

**Schwierigkeit:** S1-S2
**Länge:** 4,2 km
**Höhenunterschied:** 380 m

Dieser künstlich angelegte Trail im Bikepark Bad Wildbad bietet zahlreiche Sprünge, North-Shore-Elemente und schnelle Kurven. Ideal für alle, die Airtime lieben.

## 3. Feldberg Gipfeltrail

**Schwierigkeit:** S2-S3
**Länge:** 5 km
**Höhenunterschied:** 620 m

Vom höchsten Berg des Schwarzwalds führt dieser anspruchsvolle Trail über Wurzeln, Steine und schmale Passagen hinab nach Todtnau. Technisch herausfordernd, aber mit atemberaubenden Ausblicken belohnt.

## 4. Belchen Trail

**Schwierigkeit:** S1-S2
**Länge:** 2,8 km
**Höhenunterschied:** 320 m

Ein natürlicher Trail mit tollen Ausblicken auf die Alpen bei gutem Wetter. Nicht übermäßig technisch, aber mit hohem Spaßfaktor.

## 5. Genießerpfad Baiersbronner Seensteig

**Schwierigkeit:** S1
**Länge:** 4 km (Trail-Abschnitte)
**Höhenunterschied:** 250 m

Dieser Wanderweg enthält einige legale Trail-Abschnitte für MTBs und führt an malerischen Bergseen vorbei. Perfekt für Einsteiger und Naturliebhaber.

## Hinweise zur legalen Nutzung

Bitte beachtet, dass nicht alle Trails im Schwarzwald legal mit dem Mountainbike befahren werden dürfen. Die 2-Meter-Regel in Baden-Württemberg besagt, dass Wege unter 2 Meter Breite grundsätzlich nicht mit dem Rad befahren werden dürfen.

Die hier vorgestellten Trails sind entweder in Bikeparks, speziell ausgewiesene MTB-Strecken oder Wege, auf denen das Radfahren ausdrücklich erlaubt ist. Respektiert immer die lokalen Regelungen und nehmt Rücksicht auf Wanderer.

## Meine Ausrüstungsempfehlungen

Für diese Trails empfehle ich ein Fully mit mindestens 140mm Federweg. Eine absenkbare Sattelstütze ist besonders auf den technischen Trails ein Muss. Protektoren (mindestens Knie- und Ellbogenschützer) sollten zur Standardausrüstung gehören.
""",
            "status": "published",
            "location": "Schwarzwald, Baden-Württemberg",
            "distance_km": None,
            "elevation_m": None,
            "duration_days": None,
            "difficulty": "unterschiedlich",
            "featured_image_path": "/media/adventures/singletrails_main.jpg",
            "created_at": datetime.now() - timedelta(days=45),
            "updated_at": datetime.now() - timedelta(days=44),
            "published_at": datetime.now() - timedelta(days=44),
            "profile_id": guest_profile.id,
            "tags": [tags_by_name["Mountainbike"], tags_by_name["Schwarzwald"], tags_by_name["Baden-Württemberg"], tags_by_name["Tagesausflug"]]
        },
        {
            "title": "Donauradweg: Von Donaueschingen nach Wien",
            "slug": "donauradweg-donaueschingen-wien",
            "description": "Eine 14-tägige Fernradreise entlang der Donau",
            "content": """# Donauradweg: Von Donaueschingen nach Wien

## Planung für Sommer 2023

*Hinweis: Dies ist ein geplantes Abenteuer, das noch nicht stattgefunden hat. Der Artikel wird nach der Tour mit Erfahrungen und Bildern aktualisiert.*

Im kommenden Sommer plane ich, den Donauradweg von der Quelle in Donaueschingen bis nach Wien zu fahren. Hier teile ich meine Planungen und Vorbereitungen.

## Die Route

Der Donauradweg ist einer der bekanntesten und beliebtesten Fernradwege Europas. Von Donaueschingen bis Wien sind es etwa 1.000 Kilometer, die ich in 14 Tagen zurücklegen möchte. Die Strecke führt durch Deutschland und Österreich, vorbei an historischen Städten, malerischen Dörfern und beeindruckenden Naturlandschaften.

## Etappenplan

1. Donaueschingen - Sigmaringen (85 km)
2. Sigmaringen - Ulm (90 km)
3. Ulm - Donauwörth (80 km)
4. Donauwörth - Ingolstadt (70 km)
5. Ingolstadt - Regensburg (80 km)
6. Regensburg - Straubing (50 km) *[kürzere Etappe für Stadtbesichtigung]*
7. Straubing - Passau (90 km)
8. Passau - Schlögen (40 km)
9. Schlögen - Linz (60 km)
10. Linz - Grein (70 km)
11. Grein - Melk (65 km)
12. Melk - Tulln (80 km)
13. Tulln - Wien (40 km)
14. Reservetag / Wien erkunden

## Vorbereitungen

### Fahrrad
Für diese Tour werde ich mein Specialized Diverge Gravelbike nutzen, da der Donauradweg größtenteils asphaltiert oder gut befestigt ist. Folgende Anpassungen plane ich:
- Gepäckträger hinten mit Ortlieb Back-Roller Classic Taschen
- Lenkertasche für Wertsachen und Kamera
- Rahmentasche für Werkzeug und Snacks
- Zusätzliche Speichen und Ersatzschlauch

### Übernachtung
Ich werde eine Mischung aus Camping und Pensionen/Hotels nutzen:
- Ultraleichtes Zelt (MSR Hubba Hubba NX2)
- Leichter Sommerschlafsack
- Therm-a-Rest NeoAir XLite Isomatte

### Packliste
- 2 Radtrikots
- 2 Radhosen
- 1 lange Radhose
- 1 warme Jacke für kühlere Abende
- Regenjacke und -hose
- Sandalen für nach der Tour
- Notfall-Erste-Hilfe-Set
- Sonnencreme und Insektenschutz
- Kamera und Powerbank
- Fahrradcomputer mit vorbereiteten Tracks

### Verpflegung
Ich plane, in den zahlreichen Ortschaften entlang der Route einzukehren und lokale Spezialitäten zu probieren. Energieriegel und Getränkepulver werde ich als Reserve mitnehmen.

## Besondere Highlights

Auf diese Sehenswürdigkeiten freue ich mich besonders:
- Die junge Donau im Oberen Donautal
- Die historische Altstadt von Regensburg (UNESCO-Welterbe)
- Die Schlögener Schlinge in Österreich
- Die Wachau mit ihren Weinbergen
- Das Stift Melk
- Die Kaiserstadt Wien als krönender Abschluss

## Updates folgen

Nach der Tour werde ich diesen Artikel mit meinen tatsächlichen Erfahrungen, Fotos und Tipps aktualisieren. Bleibt dran!
""",
            "status": "planned",
            "location": "Donau (Deutschland, Österreich)",
            "distance_km": 1000.0,
            "elevation_m": 3500,
            "duration_days": 14,
            "difficulty": "mittel",
            "featured_image_path": "/media/adventures/donauradweg_main.jpg",
            "created_at": datetime.now() - timedelta(days=15),
            "updated_at": datetime.now() - timedelta(days=15),
            "published_at": None,
            "profile_id": main_profile.id,
            "tags": [tags_by_name["Radreise"], tags_by_name["Fernradweg"], tags_by_name["Mehrtagestour"], tags_by_name["Gravelbike"], tags_by_name["Deutschland"], tags_by_name["Österreich"]]
        },
        {
            "title": "Ultraleichtes Packen für Bikepacking",
            "slug": "ultraleichtes-packen-bikepacking",
            "description": "Wie du mit minimalem Gepäck maximal flexibel bleibst",
            "content": """# Ultraleichtes Packen für Bikepacking-Abenteuer

Einer der wichtigsten Aspekte erfolgreicher Bikepacking-Touren ist das richtige Packen. Je leichter das Gepäck, desto mehr Spaß macht das Fahren – besonders auf anspruchsvollen Strecken mit vielen Höhenmetern.

## Warum ultraleicht?

Ein leichtes Rad lässt sich besser handeln, ist schneller und macht einfach mehr Spaß. Jedes zusätzliche Kilo spürst du bei jedem Anstieg. Zudem erlaubt dir leichtes Gepäck, auch technisch anspruchsvollere Trails zu fahren, die mit schwerem Gepäck problematisch wären.

## Meine Ultraleicht-Grundsätze

1. **Multi-Use über Single-Use:** Jeder Gegenstand sollte mehrere Funktionen erfüllen können
2. **Gramm um Gramm:** Analysiere jedes Teil deiner Ausrüstung auf sein Gewicht
3. **Weniger ist mehr:** Verzichte auf "Wäre-schön-zu-haben"-Items
4. **Testen, testen, testen:** Probiere deine Ausrüstung vor längeren Touren aus

## Meine Ultraleicht-Packliste (Sommer, 3 Tage)

### Schlaf-System (1.350g)
- MSR Hubba NX1 Zelt: 1.120g
- Sea to Summit Spark SpI Schlafsack (Limit +4°C): 350g
- Therm-a-Rest NeoAir XLite Small: 230g

### Bekleidung (850g)
- 1× Radtrikot zum Fahren (das zweite trägst du)
- 1× Radhose zum Fahren (die zweite trägst du)
- 1× ultraleichte Daunenjacke: 250g
- 1× Regenjacke: 220g
- 1× lange dünne Merino-Unterhose: 70g
- 1× Merino-T-Shirt für abends: 120g
- 1× dünne Socken: 30g
- 1× Mikrofaser-Handtuch (klein): 50g
- 1× Buff: 30g
- 1× leichte Handschuhe: 40g
- Kleiderbeutel: 40g

### Kochen & Essen (550g)
- Soto Amicus Kocher + Topf: 250g
- Gaskartusche (100g): 210g
- Titanium Spork: 20g
- Faltbare Tasse: 30g
- Feuerzeug: 10g
- Reinigungstuch: 10g
- Kompakte Gewürzdose: 20g

### Elektronik (580g)
- Smartphone (hast du dabei): 0g
- Kleine Powerbank (5.000 mAh): 150g
- Ladekabel: 30g
- Garmin eTrex 32x GPS: 200g
- Ersatzbatterien für GPS: 50g
- Kleine Stirnlampe: 90g
- Micro-USB Ladekabel: 30g
- Kamera (Sony RX100): 300g *[optional, je nach Tour]*

### Werkzeug & Reparatur (400g)
- Multitool mit Kettennieter: 160g
- Reifenheber: 20g
- 2× Ersatzschlauch: 140g
- Flickzeug: 30g
- Mini-Pumpe: 70g
- Kabelbinder: 10g
- Gaffer-Tape (um Pumpe gewickelt): 10g
- Kettenöl (kleine Menge in Tropfflasche): 20g

### Hygiene & Gesundheit (220g)
- Zahnbürste (abgeschnitten): 10g
- Zahnpasta-Tabs: 20g
- Sonnencreme (kleine Tube): 40g
- Lippenbalsam mit LSF: 10g
- Desinfektionsmittel (kleine Flasche): 30g
- Feuchttücher (10 Stück): 40g
- Kompaktes Erste-Hilfe-Set: 90g

### Taschen-Setup (650g)
- Revelate Designs Sattelrolle: 200g
- Apidura Rahmentasche (halbe Größe): 150g
- Ortlieb Handlebar-Pack (klein): 300g

### Gesamtgewicht: ca. 4.600g

Mit diesem Setup bleibe ich unter 5 Kilogramm, was für eine 3-Tages-Tour im Sommer ausreicht. Im Frühjahr oder Herbst kommen eventuell noch eine leichte Regenhose (150g) und etwas wärmere Kleidung hinzu.

## Gewichtsspar-Tipps

1. **Taschen statt Rucksack:** Verteile das Gewicht am Fahrrad, nicht auf deinem Rücken
2. **Dehydrierte Nahrung:** Spart Gewicht, benötigt aber Wasser zum Zubereiten
3. **Digitale statt physische Karten:** GPS oder Smartphone statt Papierkarten
4. **Minimalismus bei Hygiene:** Zahnbürste kürzen, Miniaturgrößen verwenden
5. **Kleidung aus Merinowolle:** Kann mehrere Tage getragen werden, ohne zu riechen

## Fazit

Ultraleichtes Packen ist eine Philosophie, die Freiheit und Flexibilität auf Bikepacking-Touren ermöglicht. Es geht nicht darum, auf Komfort zu verzichten, sondern darum, den wahren Komfort der Mobilität zu entdecken.

*Hinweis: Diese Packliste ist für Sommertouren in Deutschland konzipiert. Für andere Klimazonen oder Jahreszeiten muss sie entsprechend angepasst werden.*
""",
            "status": "draft",
            "location": None,
            "distance_km": None,
            "elevation_m": None,
            "duration_days": None,
            "difficulty": None,
            "featured_image_path": "/media/adventures/ultralight_packing_main.jpg",
            "created_at": datetime.now() - timedelta(days=5),
            "updated_at": datetime.now() - timedelta(days=3),
            "published_at": None,
            "profile_id": main_profile.id,
            "tags": [tags_by_name["Bikepacking"], tags_by_name["Ultraleicht"]]
        }
    ]
    
    for adv_data in adventures_data:
        # Tags extrahieren und aus dem Dict entfernen
        tags = adv_data.pop("tags")
        
        # Abenteuer erstellen
        adventure = Adventure(**adv_data)
        db.add(adventure)
        db.flush()  # ID generieren
        
        # Tags zuweisen
        for tag in tags:
            adventure.tags.append(tag)
    
    db.commit()
    print(f"{len(adventures_data)} Abenteuer erstellt")

if __name__ == "__main__":
    create_seed_data()
