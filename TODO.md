# "Schwob aufm Sattl" - Bikepacking & Reise-Blog TODO Liste

## Projektbeschreibung
"Schwob aufm Sattl" ist ein Blog-Projekt, das sich auf Bikepacking, Radreisen und Outdoor-Abenteuer konzentriert. Das Projekt umfasst:
- Eine Nuxt.js-Frontend-Anwendung für Server-Side Rendering (SSR)
- Ein FastAPI-Backend zur Datenverwaltung
- Eine PostgreSQL-Datenbank für die Speicherung von Abenteuern, Routen, Ausrüstung und Medien

Der Blog soll folgende Hauptfunktionen bieten:
- Einen abgesicherten Admin-Bereich zur Verwaltung von Inhalten
- Eine attraktive Homepage mit Hero-Bild und Hervorhebung aktueller/kommender Abenteuer
- Verschiedene Seiten für Touren/Routen, Ausrüstungstipps, Profile und eine Galerie
- Integration von Social Media, insbesondere YouTube-Videos
- Bild-Upload und -Verwaltungsfunktionen

Ziel ist es, ein persönliches Reise- und Radabenteuer-Blog zu schaffen, das sowohl optisch ansprechend als auch funktional ist, mit einfacher Content-Verwaltung für den Blog-Besitzer.

## Setup & Infrastruktur
- [x] Projektstruktur einrichten (Nuxt.js für Frontend, FastAPI für Backend)
- [x] GitHub Repository anlegen
- [x] Development-Umgebung konfigurieren
- [x] Docker-Compose für lokale Entwicklung einrichten (Nuxt, FastAPI, PostgreSQL)
- [ ] CI/CD Pipeline einrichten

## Datenbank
- [ ] Prüfe und erweitere das Datenbankschema, um alle Felder abzubilden, die das Frontend benötigt (z.B. API-Felder für Abenteuer, Tags, Bilder, Profile)

## Backend (FastAPI)
- [x] FastAPI Projekt-Setup
- [x] Datenbank-Modelle und Schemas erstellen
- [x] Authentifizierung und Autorisierung für Admin-Bereich implementieren (alle schreibenden Routen sind jetzt geschützt)
- [x] API-Endpunkte für Abenteuer/Touren CRUD (alle Methoden inkl. Admin-Absicherung vorhanden)
- [x] API-Endpunkte für Bildverwaltung (Upload/Get vorhanden, Verknüpfung/Delete fehlt ggf.)
- [x] Refaktorierung: Schemas in separate Dateien pro Modell aufteilen
- [x] Swagger/OpenAPI Dokumentation konfigurieren und vervollständigen
- [x] Projekt-Dokumentation erstellen und pflegen
- [x] API-Endpunkte für Ausrüstungs-CRUD (siehe equipment_routes.py, Admin-Absicherung umgesetzt)
- [x] API-Endpunkte für Profil-CRUD (siehe profile_routes.py, Admin-Absicherung umgesetzt)
- [x] API-Endpunkte für Galerie-Verwaltung (siehe image_routes.py, Admin-Absicherung umgesetzt)
- [x] Datei-Upload für Bilder implementieren
- [x] Backend-Tests schreiben (siehe backend/tests/, pytest-Setup und Auth-Token-Logik vorhanden)

## Frontend (Nuxt.js)
- [x] Nuxt.js Projekt-Setup mit TypeScript
- [x] Basis-Layout erstellen (Header, Footer, Navigation)
- [x] Design & Styling Setup (Tailwind/SCSS)
- [ ] Responsive Design implementieren
- [ ] Dark Mode implementieren

### Admin-Bereich
- [ ] Login-Seite für Admin-Bereich
- [ ] Dashboard für Admin-Bereich
- [ ] Form für Abenteuer/Touren-Erstellung und -Bearbeitung
- [ ] Bild-Upload und -Verwaltung
- [ ] Ausrüstungs-Verwaltung
- [ ] Profil-Verwaltung
- [ ] Medien-Verwaltung (YouTube-Videos etc.)

### Öffentliche Seiten
- [ ] Homepage mit Hero-Banner und aktuellem Abenteuer
- [ ] Abenteuer-Auswahl in der Navigation
- [ ] Detailseite für Abenteuer/Touren
- [ ] Routen/Tour-Übersichtsseite
- [ ] Ausrüstungs-Seite
- [ ] Profil-Seite
- [ ] Galerie-Seite
- [ ] Social Media / YouTube-Integration

## Deployment
- [ ] Produktions-Umgebung aufsetzen
- [ ] SSL-Zertifikat einrichten
- [ ] Deployment-Prozess automatisieren
- [ ] Backup-Strategie implementieren

## Marketing & SEO
- [ ] SEO-Optimierung
- [ ] Sitemap erstellen
- [ ] Analytics einrichten
- [ ] Social Media Sharing-Funktionalität

## Wartung & Updates
- [ ] Regelmäßige Updates für Abhängigkeiten planen
- [ ] Monitoring einrichten
- [ ] Performance-Optimierung

## Zusätzliche Features (optional)
- [ ] Kommentar-Funktion für Besucher
- [ ] Newsletter-Integration
- [ ] Mehrsprachigkeit
- [ ] PWA-Funktionalität
- [ ] Offline-Zugriff auf Routen
- [ ] GPS-Track Integration und Visualisierung (z.B. mit Leaflet oder Mapbox)
- [ ] Anbindung an Strava oder komoot für Routenimport
- [ ] Wetter-API Integration für aktuelle Bedingungen auf Routen
- [ ] Packlisten-Generator basierend auf Tour-Typ und Jahreszeit
- [ ] Reisekosten-Tracker und Budget-Planer
- [ ] Integration von Höhenprofilen für Routen
- [ ] Benutzerkonten für Community-Aufbau
- [ ] Schwierigkeitsgrad-Rating für Routen
- [ ] Print-to-PDF Funktion für Routen/Touren

## Abschluss
- [ ] Finale Tests
- [ ] Dokumentation
- [ ] Launch!
