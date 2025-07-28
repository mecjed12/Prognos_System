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
```

## 📦 Beispiel-Ausgabe (JSON für Redis)
```json
{
  "risk_factor": 0.8,
  "reasons": ["low_confidence", "high_volatility"],
  "timestamp": "2025-04-05T12:05:00Z"
}
```
