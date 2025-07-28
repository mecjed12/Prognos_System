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
```
