import axios from 'axios'
import { Forecast, StrategyConfig } from '../types'

// Create axios instance with base URL
const API_BASE_URL = 'http://localhost:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Forecast API functions
export const fetchForecasts = async (): Promise<Forecast[]> => {
  try {
    const response = await apiClient.get<Forecast[]>('/forecasts/')
    return response.data
  } catch (error) {
    console.error('Error fetching forecasts:', error)
    throw error
  }
}

// Strategy Config API functions
export const fetchStrategyConfig = async (): Promise<StrategyConfig[]> => {
  try {
    const response = await apiClient.get<StrategyConfig[]>('/strategy/config/')
    return response.data
  } catch (error) {
    console.error('Error fetching strategy config:', error)
    throw error
  }
}

export const updateStrategyConfig = async (key: string, value: string): Promise<StrategyConfig> => {
  try {
    const response = await apiClient.patch<StrategyConfig>(`/strategy/config/${key}/update/`, {
      value: value
    })
    return response.data
  } catch (error) {
    console.error(`Error updating strategy config for ${key}:`, error)
    throw error
  }
}
