import React, { useEffect, useRef } from 'react'
import { createChart, ColorType } from 'lightweight-charts'
import { Forecast } from '../types'
import './ForecastChart.css'

interface ForecastChartProps {
  forecasts: Forecast[]
}

const ForecastChart: React.FC<ForecastChartProps> = ({ forecasts }) => {
  const chartContainerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!chartContainerRef.current || forecasts.length === 0) return

    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: 'white' },
        textColor: 'rgba(33, 56, 77, 1)',
      },
      grid: {
        vertLines: { color: 'rgba(197, 203, 206, 0.5)' },
        horzLines: { color: 'rgba(197, 203, 206, 0.5)' },
      },
      width: chartContainerRef.current.clientWidth,
      height: 400,
    })

    // Group forecasts by asset
    const forecastsByAsset: Record<string, Forecast[]> = {}
    forecasts.forEach(forecast => {
      if (!forecastsByAsset[forecast.asset]) {
        forecastsByAsset[forecast.asset] = []
      }
      forecastsByAsset[forecast.asset].push(forecast)
    })

    // Create series for each asset
    Object.entries(forecastsByAsset).forEach(([asset, assetForecasts]) => {
      const series = chart.addLineSeries({
        title: asset,
      })

      const data = assetForecasts
        .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
        .map(forecast => ({
          time: new Date(forecast.timestamp).toISOString().split('T')[0],
          value: forecast.prediction,
        }))

      series.setData(data)
    })

    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({ width: chartContainerRef.current.clientWidth })
      }
    }

    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
      chart.remove()
    }
  }, [forecasts])

  return (
    <div ref={chartContainerRef} className="chart-container" />
  )
}

export default ForecastChart
