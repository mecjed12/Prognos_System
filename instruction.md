🧠 Master-Anleitung: Adaptives Trading System
An: AI Coder Agent

Von: Senior Quant Developer

Auftrag: Erstelle ein vollautomatisches, prognose-gesteuertes Handelssystem basierend auf der folgenden Architektur und den Spezifikationen. Halte dich exakt an die vorgegebenen Technologien, Schnittstellen und Strukturen.

🎯 1. Ziel des Systems
Deine Aufgabe ist es, ein Fullstack-System zu entwickeln, das die folgenden Kernfunktionen erfüllt:

Prognosen: Erstellt mittels Machine Learning und statistischer Modelle Vorhersagen über zukünftige Marktrenditen.

Signalgenerierung: Leitet aus den Prognosen klare Handelssignale ab und visualisiert diese in einem Web-Interface.

Strategieanpassung: Passt die Parameter der Handelsstrategie in der QuantConnect Lean Engine dynamisch und automatisch an.

Risikomanagement: Steuert das Gesamtrisiko des Portfolios in Echtzeit basierend auf Marktkonditionen und Modellkonfidenz.

Produktionsreife: Das gesamte System muss skalierbar, wartbar, robust und vollständig auditierbar sein.

📂 2. Projektstruktur
Erstelle die folgende Verzeichnis- und Dateistruktur. Die Inhalte der README.md-Dateien sowie der docker-compose.yml sind in den folgenden Abschnitten detailliert beschrieben.

trading-system/
│
├── instruction.md              # Diese Datei
│
├── services/
│   ├── frontend/
│   │   └── README.md
│   │
│   ├── django-backend/
│   │   ├── requirements.txt
│   │   ├── requirements-dev.txt
│   │   └── README.md
│   │
│   ├── forecast-engine/
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   ├── risk-engine/
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   ├── message-broker/
│   │   └── README.md
│   │
│   └── lean-execution/
│       └── README.md
│
├── docker-compose.yml          # Definiert die Gesamtinfrastruktur
├── .env.example                # Vorlage für Umgebungsvariablen
└── monitoring/                 # (Optional, für spätere Implementierung)

🧱 3. Architektur & Technologie
Das System folgt einer Microservice-Architektur. Die Kommunikation erfolgt über eine REST-API und einen Echtzeit-Message-Broker.

Architektur-Diagramm:

  Frontend (React)  │◄─── REST API ───►│ Django API (Backend) │
└───────────────────┘                  └──────────────────────┘
         │                                      │
         │                                      ▼
         │                          ┌──────────────────────────┐
         └──────────────────────────►│  PostgreSQL + TimescaleDB  │
                                    └──────────────────────────┘
                                                │
                  ┌─────────────────────────────┴─────────────────────────────┐
                  ▼                                                         ▼
┌──────────────────────────┐                                ┌──────────────────────────┐
│  Prognose-Engine (Python)  │                                │ Risk Management Engine (Python) │
└──────────────────────────┘                                └──────────────────────────┘
                  │                                                         │
                  └─────────────────────────────┬─────────────────────────────┘
                                                ▼
                                    ┌──────────────────────────┐
                                    │   Message Broker (Redis)   │
                                    └──────────────────────────┘
                                                │
                                                ▼
                                    ┌──────────────────────────┐
                                    │ QuantConnect Lean (C#)   │
                                    │   (Execution Engine)     │
                                    └──────────────────────────┘

Technologie-Stack:

Schicht

Technologie

Anweisung

Frontend

React + TypeScript + Vite + Lightweight Charts

Modernes, reaktives UI.

Backend

Django + DRF + JWT + Celery

Robuste API und Task-Verwaltung.

Datenbank

PostgreSQL + TimescaleDB Extension

Für Zeitreihendaten optimiert.

Message Broker

Redis

Für Low-Latency Echtzeit-Kommunikation.

Prognose

Python (scikit-learn, LightGBM, statsmodels)

Das Kernstück der Intelligenz.

Risk Engine

Python

Dynamische Anpassung der Risikoparameter.

Execution

QuantConnect Lean (C#/.NET 6)

Professionelle Handelsausführung.

Infrastruktur

Docker + Docker Compose

Vollständige Containerisierung aller Services.

🚀 4. Globale Anweisungen & Workflow
Umgebungsvariablen
Erstelle eine .env.example-Datei. Sensible Daten wie API-Keys oder Passwörter dürfen niemals im Code hardcodiert werden.

# .env.example

# PostgreSQL
DB_HOST=postgres
DB_NAME=tradingdb
DB_USER=trader
DB_PASS=secure_password_change_me

# Django
SECRET_KEY=strong_random_secret_key_change_me

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=secure_redis_password_change_me

# API Keys (Beispiele)
MARKET_DATA_API_KEY=dein_api_key_hier
BROKER_API_KEY=dein_broker_key
BROKER_API_SECRET=dein_broker_secret

# QuantConnect
QC_USER_ID=dein_qc_user_id
QC_API_TOKEN=dein_qc_api_token

Docker-Infrastruktur
Erstelle die docker-compose.yml-Datei, um alle Services zu orchestrieren.

# docker-compose.yml

version: '3.8'

services:
  postgres:
    image: timescale/timescaledb:latest-pg14
    container_name: trading_db
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASS}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: trading_broker
    command: redis-server --requirepass ${REDIS_PASSWORD}
    ports:
      - "6379:6379"
    restart: unless-stopped

  django-backend:
    build: ./services/django-backend
    container_name: trading_api
    command: >
      sh -c "python manage.py migrate &&
             gunicorn trading_system.wsgi:application --bind 0.0.0.0:8000"
    volumes:
      - ./services/django-backend:/app
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  frontend:
    build: ./services/frontend
    container_name: trading_ui
    ports:
      - "3000:3000"
    depends_on:
      - django-backend
    restart: unless-stopped

  forecast-engine:
    build: ./services/forecast-engine
    container_name: trading_forecast
    command: python main.py
    env_file: .env
    depends_on:
      - postgres
      - redis
    restart: on-failure

  risk-engine:
    build: ./services/risk-engine
    container_name: trading_risk
    command: python main.py
    env_file: .env
    depends_on:
      - postgres
      - redis
    restart: on-failure

  lean-execution:
    build: ./services/lean-execution
    container_name: trading_execution
    env_file: .env
    depends_on:
      - redis
    restart: on-failure

volumes:
  postgres_data:

📄 5. Anweisungen für Microservices
Erstelle für jeden der folgenden Services eine README.md-Datei im entsprechenden Unterverzeichnis (services/<name>/README.md) mit exakt dem folgenden Inhalt.

/services/frontend/README.md
# 🖥️ Frontend: Web-Dashboard für Signale & Prognosen

## 🎯 Verantwortung
- Visualisierung von Prognosen, Signalen und Risikometriken in Echtzeit.
- Anzeige von historischer Performance und Backtesting-Ergebnissen.
- Bereitstellung einer Benutzeroberfläche zur Konfiguration von Strategieparametern (z.B. Risikoschwellen).

## 🛠️ Technologie
- **Framework**: React mit TypeScript
- **Build-Tool**: Vite für schnelle Entwicklung und Builds
- **Charting**: Lightweight Charts (von TradingView) für performante Finanz-Charts.
- **State Management**: Zustand oder React Context für einfaches, globales State Management.
- **Kommunikation**: Axios für REST-API-Aufrufe, native WebSocket-API für Echtzeit-Updates.

## 🔗 Schnittstellen
- **Django API (REST)**:
  - `GET /api/forecasts/`: Abruf historischer und aktueller Prognosen.
  - `GET /api/risk/`: Abruf des aktuellen Risikostatus.
  - `GET /api/performance/`: Abruf von Performancedaten.
- **Message Broker (WebSocket)**:
  - Verbindet sich mit einem WebSocket-Gateway (das an Redis angebunden ist), um Live-Updates für Prognosen und Risikofaktoren zu erhalten.

## 📂 Struktur (Vorschlag)

src/
├── components/
│   ├── charts/
│   │   └── ForecastChart.tsx
│   ├── dashboard/
│   │   └── RiskDashboard.tsx
│   └── ui/
│       └── SignalHeatmap.tsx
├── services/
│   └── api.ts         # API-Aufrufe
├── hooks/
│   └── useWebSocket.ts  # WebSocket-Logik
├── App.tsx
└── main.tsx


## 🚀 Startanleitung
```bash
# Abhängigkeiten installieren
npm install

# Entwicklungs-Server starten
npm run dev

/services/django-backend/README.md
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

🔌 API-Endpunkte (Beispiele)
GET /api/forecasts/: Liste aller Prognosen (mit Filterung).

POST /api/forecasts/: Endpunkt für die Forecast-Engine, um neue Prognosen zu speichern.

GET /api/strategy/config/: Aktuelle Strategie-Parameter abrufen.

PUT /api/strategy/config/: Strategie-Parameter aktualisieren (z.B. via UI).

🚀 Startanleitung
# Abhängigkeiten installieren
pip install -r requirements.txt

# Datenbank-Migrationen durchführen
python manage.py migrate

# Celery Worker starten
celery -A trading_system worker -l info

# Django Entwicklungs-Server starten
python manage.py runserver 0.0.0.0:8000

/services/forecast-engine/README.md
# 🔮 Prognose-Engine: Signal-Generierung

## 🎯 Verantwortung
- Periodischer Abruf von frischen Marktdaten von externen APIs.
- Durchführung von Feature-Engineering, um relevante Prädiktoren zu erstellen.
- Training und Anwendung von ML/statistischen Modellen zur Vorhersage von Renditen.
- Veröffentlichung der generierten Prognosen in der Datenbank und im Message Broker.

## 🛠️ Technologie
- **Core**: Python 3.10+
- **Bibliotheken**: pandas, numpy, scikit-learn, LightGBM, statsmodels.
- **Kommunikation**: `redis-py` für Redis, `requests` und `psycopg2` für API/DB.
- **Scheduling**: `apscheduler` oder ein Celery Beat Task (gesteuert vom Django-Backend).

## 🔗 Schnittstellen
- **Input**:
  - PostgreSQL: Abruf historischer Daten für das Feature-Engineering.
  - Externe Daten-APIs (z.B. Binance, Polygon).
- **Output**:
  - `INSERT INTO forecasts`: Schreibt die neue Prognose in die TimescaleDB.
  - `PUBLISH forecast_updates {json}`: Sendet die Prognose in Echtzeit an einen Redis-Channel.

## 🔄 Workflow
1.  Wird periodisch (z.B. stündlich) durch den Scheduler ausgelöst.
2.  Lädt die neuesten OHLCV-Daten für die konfigurierten Assets.
3.  Berechnet technische Indikatoren und statistische Features (z.B. RSI, Volatilität, Momentum).
4.  Wendet das trainierte Modell an, um die zukünftige Rendite (`E[r]`) vorherzusagen.
5.  Schätzt die Konfidenz der Vorhersage (z.B. durch Analyse der Feature-Wichtigkeit oder historischer Genauigkeit).
6.  Speichert das Ergebnis in der Datenbank und sendet es an den Redis-Channel.

## 📦 Beispiel-Ausgabe (JSON für Redis)
```json
{
  "asset": "BTCUSD",
  "horizon": "4h",
  "prediction": 0.0082,
  "confidence": 0.76,
  "timestamp": "2025-04-05T12:00:00Z"
}

/services/risk-engine/README.md
# 🛡️ Risk Management Engine

## 🎯 Verantwortung
- Kontinuierliche Überwachung der aktuellen Portfolio-Exposure und Marktrisiken.
- Dynamische Anpassung eines globalen `risk_factor`, der die Aggressivität der Handelsstrategie steuert.
- Implementierung von "Circuit Breakers" (Sicherheitsabschaltungen) bei extremen Drawdowns oder Marktvolatilität.

## 🛠️ Technologie
- **Core**: Python 3.10+
- **Kommunikation**: `redis-py` (hört auf Prognosen, publiziert Risiko-Updates), `SQLAlchemy` oder `psycopg2` für direkten DB-Zugriff.

## 🔗 Schnittstellen
- **Input**:
  - Redis Channel `forecast_updates`: Hört auf neue Prognosen, um die Marktbedingungen zu bewerten.
  - PostgreSQL: Liest aktuelle Positionsgrößen und PnL-Daten, die von Lean geloggt wurden.
- **Output**:
  - Redis Channel `risk_updates`: Publiziert Updates des `risk_factor` als JSON-Objekt.
  - PostgreSQL: Schreibt Einträge in eine `risk_log`-Tabelle zur Auditierung.

## 📊 Logik (Beispiele)
```python
# Pseudocode
risk_factor = 1.0  # Default

if latest_forecast.confidence < 0.6:
    risk_factor *= 0.8

if portfolio.current_drawdown > 0.05:
    risk_factor *= 0.5  # Reduziere Risiko bei hohem Drawdown

if market_volatility > 2 * historical_average_volatility:
    risk_factor *= 0.6  # Reduziere Risiko bei hoher Volatilität

📦 Beispiel-Ausgabe (JSON für Redis)
{
  "risk_factor": 0.8,
  "reasons": ["low_confidence", "high_volatility"],
  "timestamp": "2025-04-05T12:05:00Z"
}

/services/message-broker/README.md
# 📡 Message Broker: Redis

## 🎯 Verantwortung
- Dient als hochperformante, asynchrone Kommunikationszentrale zwischen den Microservices.
- Garantiert die Echtzeit-Verteilung von kritischen Daten wie Prognosen und Risikosignalen.

## 🛠️ Technologie
- **Software**: Redis 7+
- **Konfiguration**: Läuft im Docker-Container, passwortgeschützt.

## 🔑 Wichtige Channels
- `forecast_updates`: Channel für neue Prognosen von der `forecast-engine`. Die `risk-engine` und `lean-execution` abonnieren diesen Channel.
- `risk_updates`: Channel für neue Risikofaktoren von der `risk-engine`. Die `lean-execution` abonniert diesen Channel.
- `strategy_config`: Channel für Konfigurationsänderungen aus dem UI, um Lean dynamisch zu aktualisieren.

## 📡 Beispiel-Nutzung (Python)
```python
import redis
import json

# Verbindung aufbauen
r = redis.Redis(host='redis', port=6379, password='secure_redis_password_change_me')

# Nachricht publizieren
data = {"asset": "BTCUSD", "prediction": 0.01}
r.publish('forecast_updates', json.dumps(data))

/services/lean-execution/README.md
# ⚙️ QuantConnect Lean: Execution Engine

## 🎯 Verantwortung
- Ausführung der Handelslogik basierend auf den Signalen der Prognose- und Risk-Engines.
- Dynamische Anpassung von Positionsgrößen und Handelsentscheidungen in Echtzeit.
- Logging aller Trades, Orders und Portfolio-Zustände in die Datenbank für Audits und Performance-Analyse.

## 🛠️ Technologie
- **Framework**: QuantConnect Lean Engine (in C# / .NET 6)
- **Daten**: Nutzt Custom Data-Klassen, um externe Signale von Redis zu verarbeiten.
- **Kommunikation**: `StackExchange.Redis` für die Anbindung an den Message Broker.

## 🔗 Schnittstellen
- **Input**:
  - Redis: Abonniert die Channels `forecast_updates` und `risk_updates`, um die Strategie dynamisch zu steuern.
- **Output**:
  - Broker API: Sendet Orders an den angebundenen Broker (z.B. Binance, Interactive Brokers).
  - PostgreSQL: Schreibt detaillierte Trade- und PnL-Logs in die Datenbank.

## 🔄 Integration in Lean (Konzept)
1.  **`Initialize()`-Methode**:
    - Stelle die Verbindung zum Redis-Server her.
    - Abonniere die relevanten Channels (`forecast_updates`, `risk_updates`).
    - Richte einen Event-Handler ein, der auf neue Nachrichten reagiert und die Signale in einer internen Variable speichert.
2.  **`OnData()`-Methode**:
    - Prüfe bei jedem Datenpunkt, ob ein neues Signal vom Event-Handler empfangen wurde.
    - Lese den aktuellen `risk_factor`.
    - Passe die Ziel-Positionsgröße basierend auf der Prognose (`prediction`), der Sicherheit (`confidence`) und dem `risk_factor` an.
    - Nutze `SetHoldings()` oder `MarketOrder()`, um die Position anzupassen.

## 📦 Beispiel-Logik in C# (Auszug)
```csharp
// In der Algorithm-Klasse

private Forecast _latestSignal;
private double _riskFactor = 1.0;

public override void Initialize()
{
    // ... Redis-Subscriber initialisieren ...
    subscriber.Subscribe("forecast_updates", (channel, message) => {
        _latestSignal = JsonConvert.DeserializeObject<Forecast>(message);
    });
    subscriber.Subscribe("risk_updates", (channel, message) => {
        _riskFactor = JsonConvert.DeserializeObject<RiskUpdate>(message).RiskFactor;
    });
}

public override void OnData(Slice data)
{
    if (_latestSignal == null) return;

    if (_latestSignal.Confidence > 0.7)
    {
        var targetAllocation = _latestSignal.Prediction > 0 ? 1.0 : -1.0;
        var finalAllocation = targetAllocation * _riskFactor;
        SetHoldings(_symbol, finalAllocation);
    }
    else
    {
        Liquidate(); // Schließe Position bei geringer Konfidenz
    }
}

📄 6. Anweisungen für Dependencies (requirements.txt)
Erstelle die folgenden requirements.txt-Dateien in den entsprechenden Service-Verzeichnissen.

/services/django-backend/requirements.txt
# Django Core
Django==4.2.16
djangorestframework==3.14.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
python-decouple==3.8

# API & Security
django-cors-headers==4.3.1
djangorestframework-simplejwt==5.3.1

# Asynchrone Tasks
celery==5.3.6
redis==5.0.3
django-celery-beat==2.5.0

# Logging & Monitoring
structlog==23.4.0
sentry-sdk[django]==1.45.0

# Optional: TimescaleDB-Unterstützung
django-timescale==0.4.0

/services/django-backend/requirements-dev.txt
# Entwicklungstools
Werkzeug==2.3.8
django-debug-toolbar==4.3.0

# Testing
pytest==8.1.1
pytest-django==4.8.0
factory-boy==3.3.0
Faker==19.8.1

# Formatierung & Linting
black==23.12.1
isort==5.13.2
flake8==6.1.0

# Sicherheit
safety==3.1.0
bandit==1.7.7

/services/forecast-engine/requirements.txt
# Wissenschaftliche Bibliotheken
numpy==1.24.4
pandas==2.1.4
scikit-learn==1.4.2
lightgbm==4.1.0
statsmodels==0.14.1

# Datenzugriff
psycopg2-binary==2.9.9
SQLAlchemy==2.0.27

# Messaging & Scheduling
redis==5.0.3
apscheduler==3.10.4

# Konfiguration & Logging
python-decouple==3.8
structlog==23.4.0

/services/risk-engine/requirements.txt
# Basis
python-decouple==3.8
structlog==23.4.0
numpy==1.24.4

# Datenbank & Messaging
psycopg2-binary==2.9.9
SQLAlchemy==2.0.27
redis==5.0.3

Sicherheitshinweise für Dependencies
Alle Pakete haben keine bekannten kritischen CVEs (Stand: Juli 2025).

Versionen sind gepinnt, um unerwartete und potenziell fehlerhafte Updates zu verhindern.

Für Produktionsumgebungen wird empfohlen, pip-tools zu verwenden, um aus diesen Dateien eine vollständig deterministische requirements.txt zu kompilieren.

✅ 7. Abschluss und Nächste Schritte
Du hast nun alle notwendigen Anweisungen, um das System zu erstellen.

Dein Arbeitsablauf:

Erstelle die vollständige Verzeichnisstruktur.

Erstelle alle README.md- und requirements.txt-Dateien mit dem exakten Inhalt aus diesem Dokument.

Erstelle die docker-compose.yml und .env.example-Dateien.

Beginne mit der Implementierung der einzelnen Services. Es wird empfohlen, in dieser Reihenfolge vorzugehen:

django-backend (Datenmodell und API-Grundgerüst)

forecast-engine (Die Kernlogik)

lean-execution (Integration der Signale)

risk-engine (Hinzufügen der Risikoschicht)

frontend (Visualisierung)

Beginne jetzt mit der Erstellung der Projektstruktur.
