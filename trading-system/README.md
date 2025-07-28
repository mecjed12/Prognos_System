# Adaptive Trading System

Ein vollautomatisches, prognosegesteuertes Handelssystem mit Microservice-Architektur.

## Architektur

Das System besteht aus folgenden Microservices:

1. **Django Backend** - Zentrale API und Datenmanagement
2. **Forecast Engine** - Machine Learning-basierte Marktprognosen
3. **Risk Engine** - Risikobewertung und Strategieanpassung
4. **Lean Execution Engine** - Trade-Ausführung
5. **Frontend** - Web-basierte Benutzeroberfläche
6. **Message Broker** - Redis für Inter-Service-Kommunikation
7. **Datenbank** - PostgreSQL/TimescaleDB für persistente Speicherung

## 🚀 Startanleitung

1. Kopieren Sie `.env.example` zu `.env` und passen Sie die Werte an:
   ```bash
   cp .env.example .env
   # Bearbeiten Sie .env mit Ihren Werten
   ```

2. Starten Sie alle Services mit Docker Compose:
   ```bash
   docker-compose up -d --build
   ```

3. Initialisieren Sie die Datenbank (beim ersten Start):
   ```bash
   docker-compose exec django-backend python manage.py migrate
   docker-compose exec django-backend python manage.py init_strategy_config
   ```

4. Greifen Sie auf die Services zu:
   - Frontend: http://localhost:3000
   - API: http://localhost:8000/api/
   - Admin: http://localhost:8000/admin/

## 🧪 Statusüberprüfung

Um den Status aller Services zu überprüfen:
```bash
docker-compose ps
```

## 🛑 Services stoppen

Um alle Services zu stoppen:
```bash
docker-compose down
```

Um alle Services inklusive Volumes zu stoppen (löscht Daten):
```bash
docker-compose down -v
```

## Entwicklung

### Frontend-Entwicklung

Für die Frontend-Entwicklung können Sie entweder den Docker-Container verwenden oder lokal entwickeln:

1. **Mit Docker (empfohlen):**
   ```bash
   docker-compose up -d frontend
   ```

2. **Lokal:**
   ```bash
   cd services/frontend
   npm install
   npm run dev
   ```

### Backend-Entwicklung

1. **Mit Docker (empfohlen):**
   ```bash
   docker-compose up -d django-backend
   ```

2. **Lokal:**
   ```bash
   cd services/django-backend
   python -m venv venv
   source venv/bin/activate  # oder venv\Scripts\activate auf Windows
   pip install -r requirements.txt
   python manage.py runserver
   ```

## Wichtige Hinweise

- Alle Services sind über Docker orchestriert
- Die Services kommunizieren über REST APIs und Redis-Nachrichten
- Die Umgebungsvariablen müssen in der `.env`-Datei konfiguriert werden

## Fehlerbehebung

### "Cannot find module 'react'" im Frontend

Dieser Fehler tritt auf, wenn die npm-Abhängigkeiten nicht installiert sind. Führen Sie folgende Schritte aus:

1. Stellen Sie sicher, dass Node.js und npm installiert sind
2. Installieren Sie die Abhängigkeiten:
   ```bash
   cd services/frontend
   npm install
   ```

### Datenbankprobleme

Wenn es Probleme mit der Datenbank gibt:

1. Stellen Sie sicher, dass der PostgreSQL-Container läuft:
   ```bash
   docker-compose up -d postgres
   ```
2. Führen Sie die Migrationen aus:
   ```bash
   docker-compose exec django-backend python manage.py migrate
   ```

## Lizenz

Dieses Projekt ist für interne Verwendung konzipiert.
