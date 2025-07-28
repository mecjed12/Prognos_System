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
```
