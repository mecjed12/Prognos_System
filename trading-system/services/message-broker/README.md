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
```
