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
  - Abonnement von `forecast_updates` für Echtzeit-Prognosen.
  - Abonnement von `trade_executions` für Echtzeit-Ausführungsberichte.

## 📊 Beispiel-Ausgabe
- Interaktive Charts mit Prognose-Kegel und Konfidenzintervallen.
- Heatmap zur Risiko- und Positionsverteilung.
- Echtzeit-Performance-Metriken (Sharpe Ratio, Drawdown, etc.).
- Konfigurationspanel mit dynamischen Slidern für Risikoparameter.

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
```

## 🐳 Mit Docker verwenden (Empfohlen)

```bash
# Starten des Frontend-Services mit Docker Compose
docker-compose up -d frontend

# Zugriff auf die Anwendung unter http://localhost:3000
```

## 🛠️ Fehlerbehebung

### "Cannot find module 'react'" Fehler

Dieser Fehler tritt auf, wenn die npm-Abhängigkeiten nicht installiert sind:

1. Stellen Sie sicher, dass Node.js und npm installiert sind
2. Führen Sie `npm install` im Frontend-Verzeichnis aus
3. Überprüfen Sie, ob alle Abhängigkeiten in package.json installiert sind

### TypeScript-Fehler

1. Stellen Sie sicher, dass TypeScript installiert ist: `npm install --save-dev typescript`
2. Installieren Sie React-Typen: `npm install --save-dev @types/react @types/react-dom`
3. Überprüfen Sie die tsconfig.json-Datei auf korrekte Konfiguration
