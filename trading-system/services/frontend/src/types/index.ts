export interface Forecast {
  id: number;
  asset: string;
  horizon: string;
  prediction: number;
  confidence: number;
  timestamp: string;
}

export interface StrategyConfig {
  id: number;
  key: string;
  value: string;
}

export interface ApiResponse<T> {
  data: T;
  status: string;
}
