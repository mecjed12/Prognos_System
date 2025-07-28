#!/usr/bin/env python3

import os
import sys
import time
import logging
import redis
import json
import psycopg2
from datetime import datetime
from decouple import config
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ForecastEngine:
    def __init__(self):
        # Load configuration
        self.db_config = {
            'host': config('DB_HOST', default='postgres'),
            'database': config('DB_NAME', default='tradingdb'),
            'user': config('DB_USER', default='trader'),
            'password': config('DB_PASS', default='secure_password_change_me'),
            'port': config('DB_PORT', default='5432', cast=int)
        }
        
        self.redis_config = {
            'host': config('REDIS_HOST', default='redis'),
            'port': config('REDIS_PORT', default='63379', cast=int),
            'password': config('REDIS_PASSWORD', default='redis_password')
        }
        
        # Connect to Redis
        self.redis_client = redis.Redis(
            host=self.redis_config['host'],
            port=self.redis_config['port'],
            password=self.redis_config['password'],
            decode_responses=True
        )
        
        # Connect to PostgreSQL
        self.db_conn = None
        self.connect_to_db()
        
        # Initialize model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.is_trained = False
        
        logger.info("Forecast Engine initialized")
    
    def connect_to_db(self):
        """Establish connection to PostgreSQL database"""
        try:
            self.db_conn = psycopg2.connect(**self.db_config)
            logger.info("Connected to PostgreSQL database")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def load_historical_data(self, asset, days=30):
        """Load historical market data for training"""
        # This is a placeholder implementation
        # In a real implementation, this would fetch actual market data
        logger.info(f"Loading historical data for {asset} ({days} days)")
        
        # Generate synthetic data for demonstration
        np.random.seed(42)
        dates = pd.date_range(end=datetime.now(), periods=days*24, freq='H')
        prices = 100 + np.cumsum(np.random.randn(len(dates)) * 0.1)
        
        df = pd.DataFrame({
            'timestamp': dates,
            'open': prices,
            'high': prices * (1 + np.random.rand(len(prices)) * 0.01),
            'low': prices * (1 - np.random.rand(len(prices)) * 0.01),
            'close': prices * (1 + np.random.rand(len(prices)) * 0.001 - 0.0005),
            'volume': np.random.randint(1000, 10000, len(prices))
        })
        
        return df
    
    def engineer_features(self, df):
        """Engineer features for machine learning model"""
        logger.info("Engineering features")
        
        # Calculate technical indicators
        df['returns'] = df['close'].pct_change()
        df['volatility'] = df['returns'].rolling(window=24).std()
        df['sma_24'] = df['close'].rolling(window=24).mean()
        df['sma_168'] = df['close'].rolling(window=168).mean()  # 1 week
        df['rsi'] = self.calculate_rsi(df['close'])
        df['ema_12'] = df['close'].ewm(span=12).mean()
        df['ema_26'] = df['close'].ewm(span=26).mean()
        df['macd'] = df['ema_12'] - df['ema_26']
        
        # Lag features
        df['close_lag_1'] = df['close'].shift(1)
        df['close_lag_2'] = df['close'].shift(2)
        df['close_lag_3'] = df['close'].shift(3)
        
        # Target variable (next hour's return)
        df['target'] = df['returns'].shift(-1)
        
        # Drop rows with NaN values
        df = df.dropna()
        
        return df
    
    def calculate_rsi(self, prices, window=14):
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def train_model(self, asset):
        """Train the machine learning model"""
        logger.info(f"Training model for {asset}")
        
        # Load and prepare data
        df = self.load_historical_data(asset)
        df = self.engineer_features(df)
        
        # Select features for training
        feature_columns = [
            'volatility', 'sma_24', 'sma_168', 'rsi', 'macd',
            'close_lag_1', 'close_lag_2', 'close_lag_3'
        ]
        
        X = df[feature_columns]
        y = df['target']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        logger.info(f"Model trained. MSE: {mse:.6f}")
        
        return mse
    
    def generate_forecast(self, asset, horizon='1h'):
        """Generate a forecast for the given asset"""
        if not self.is_trained:
            logger.warning("Model is not trained yet. Training now...")
            self.train_model(asset)
        
        logger.info(f"Generating forecast for {asset} ({horizon})")
        
        # Load recent data
        df = self.load_historical_data(asset, days=7)
        df = self.engineer_features(df)
        
        # Select features
        feature_columns = [
            'volatility', 'sma_24', 'sma_168', 'rsi', 'macd',
            'close_lag_1', 'close_lag_2', 'close_lag_3'
        ]
        
        # Use the latest data point
        latest_features = df[feature_columns].iloc[-1].values.reshape(1, -1)
        
        # Generate prediction
        prediction = self.model.predict(latest_features)[0]
        
        # Calculate confidence (simplified)
        # In a real implementation, this would be more sophisticated
        confidence = 0.7 + np.random.rand() * 0.3  # Random confidence between 0.7 and 1.0
        
        # Create forecast object
        forecast = {
            'asset': asset,
            'horizon': horizon,
            'prediction': float(prediction),
            'confidence': float(confidence),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        logger.info(f"Generated forecast: {forecast}")
        return forecast
    
    def save_forecast_to_db(self, forecast):
        """Save forecast to PostgreSQL database"""
        logger.info("Saving forecast to database")
        
        try:
            cursor = self.db_conn.cursor()
            
            insert_query = """
            INSERT INTO trading_forecast (asset, horizon, prediction, confidence, timestamp)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (
                forecast['asset'],
                forecast['horizon'],
                forecast['prediction'],
                forecast['confidence'],
                forecast['timestamp']
            ))
            
            self.db_conn.commit()
            cursor.close()
            
            logger.info("Forecast saved to database")
        except Exception as e:
            logger.error(f"Failed to save forecast to database: {e}")
            self.db_conn.rollback()
            raise
    
    def publish_forecast_to_redis(self, forecast):
        """Publish forecast to Redis channel"""
        logger.info("Publishing forecast to Redis")
        
        try:
            self.redis_client.publish('forecast_updates', json.dumps(forecast))
            logger.info("Forecast published to Redis")
        except Exception as e:
            logger.error(f"Failed to publish forecast to Redis: {e}")
            raise
    
    def run_forecast_cycle(self, assets=['BTCUSD', 'ETHUSD', 'SOLUSD']):
        """Run a complete forecast cycle for all assets"""
        logger.info("Starting forecast cycle")
        
        for asset in assets:
            try:
                # Generate forecast
                forecast = self.generate_forecast(asset)
                
                # Save to database
                self.save_forecast_to_db(forecast)
                
                # Publish to Redis
                self.publish_forecast_to_redis(forecast)
                
            except Exception as e:
                logger.error(f"Failed to process forecast for {asset}: {e}")
                continue
        
        logger.info("Forecast cycle completed")
    
    def run(self, interval=3600):  # Default: every hour
        """Run the forecast engine continuously"""
        logger.info(f"Starting forecast engine with {interval}s interval")
        
        # Initial training
        assets = ['BTCUSD', 'ETHUSD', 'SOLUSD']
        for asset in assets:
            try:
                self.train_model(asset)
            except Exception as e:
                logger.error(f"Failed to train model for {asset}: {e}")
        
        # Run forecast cycle
        while True:
            try:
                self.run_forecast_cycle(assets)
                logger.info(f"Sleeping for {interval} seconds")
                time.sleep(interval)
            except KeyboardInterrupt:
                logger.info("Received interrupt signal. Shutting down.")
                break
            except Exception as e:
                logger.error(f"Error in forecast cycle: {e}")
                time.sleep(60)  # Wait 1 minute before retrying


def main():
    """Main entry point"""
    engine = ForecastEngine()
    
    # Check if we should run once or continuously
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        engine.run_forecast_cycle()
    else:
        # Run continuously
        engine.run()


if __name__ == "__main__":
    main()
