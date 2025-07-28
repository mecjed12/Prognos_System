import React, { useState, useEffect } from 'react'
import './App.css'
import { fetchForecasts, fetchStrategyConfig } from './services/api'
import { Forecast, StrategyConfig } from './types'
import ForecastChart from './components/ForecastChart'
import StrategyConfigPanel from './components/StrategyConfigPanel'

function App() {
  const [forecasts, setForecasts] = useState<Forecast[]>([])
  const [strategyConfig, setStrategyConfig] = useState<StrategyConfig[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true)
        const [forecastData, configData] = await Promise.all([
          fetchForecasts(),
          fetchStrategyConfig()
        ])
        setForecasts(forecastData)
        setStrategyConfig(configData)
        setError(null)
      } catch (err) {
        setError('Failed to load data')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    loadData()
    const interval = setInterval(loadData, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  if (loading) return <div className="loading">Loading...</div>
  if (error) return <div className="error">Error: {error}</div>

  return (
    <div className="App">
      <header className="App-header">
        <h1>Adaptive Trading System</h1>
      </header>
      <main>
        <section className="forecasts">
          <h2>Market Forecasts</h2>
          <ForecastChart forecasts={forecasts} />
        </section>
        <section className="strategy-config">
          <h2>Strategy Configuration</h2>
          <StrategyConfigPanel config={strategyConfig} />
        </section>
      </main>
    </div>
  )
}

export default App
