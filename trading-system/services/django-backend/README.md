# 🐍 Django Backend: API & Datenmanagement

## 🎯 Verantwortung
- Bereitstellung einer sicheren, robusten REST-API für alle anderen Services.
- Persistente Speicherung von Prognosen, Signalen, Trades und Konfigurationen in der Datenbank.
- Benutzerauthentifizierung und -autorisierung mittels JSON Web Tokens (JWT).
- Ausführung von zeitgesteuerten, asynchronen Aufgaben (z.B. Starten der Prognose-Engine) mittels Celery.

## 🛠️ Technologie
- **Framework**: Django 4.2+
- **API**: Django REST Framework (DRF)
- **Asynchrone Tasks**: Celery mit Redis als Broker.
- **Datenbank-Anbindung**: `psycopg2-binary` für PostgreSQL/TimescaleDB.

## 🔗 Abhängigkeiten
- **Erfordert**: PostgreSQL mit TimescaleDB-Erweiterung, Redis.

## 📂 Wichtige Modelle (Beispiele)
```python
# in models.py

from django.db import models

class Forecast(models.Model):
    asset = models.CharField(max_length=20, db_index=True)
    horizon = models.CharField(max_length=10)  # z.B. "1h", "4h", "1d"
    prediction = models.FloatField()
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

class StrategyConfig(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=255)

```

## 🔌 API-Endpunkte (Beispiele)
- `GET /api/forecasts/`: Liste aller Prognosen (mit Filterung).
- `POST /api/forecasts/`: Endpunkt für die Forecast-Engine, um neue Prognosen zu speichern.
- `GET /api/strategy/config/`: Aktuelle Strategie-Parameter abrufen.
- `PUT /api/strategy/config/`: Strategie-Parameter aktualisieren (z.B. via UI).

## 🚀 Startanleitung
```bash
# Abhängigkeiten installieren
pip install -r requirements.txt

# Datenbank-Migrationen durchführen
python manage.py migrate

# Celery Worker starten
celery -A trading_system worker -l info

# Django Entwicklungs-Server starten
python manage.py runserver 0.0.0.0:8000
```
