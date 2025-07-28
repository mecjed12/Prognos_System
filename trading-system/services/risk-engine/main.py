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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RiskEngine:
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
        
        # Risk parameters (these would typically be loaded from the database)
        self.risk_factor = 1.0
        self.position_size_limit = 0.1
        self.confidence_threshold = 0.7
        self.max_drawdown_limit = 0.05
        self.volatility_multiplier = 1.0
        
        # Load initial configuration
        self.load_strategy_config()
        
        logger.info("Risk Engine initialized")
    
    def connect_to_db(self):
        """Establish connection to PostgreSQL database"""
        try:
            self.db_conn = psycopg2.connect(**self.db_config)
            logger.info("Connected to PostgreSQL database")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def load_strategy_config(self):
        """Load strategy configuration from database"""
        logger.info("Loading strategy configuration")
        
        try:
            cursor = self.db_conn.cursor()
            
            # Query to get all strategy configuration
            query = "SELECT key, value FROM trading_strategyconfig"
            cursor.execute(query)
            
            configs = cursor.fetchall()
            
            # Update risk parameters
            for key, value in configs:
                if key == 'risk_factor':
                    self.risk_factor = float(value)
                elif key == 'position_size_limit':
                    self.position_size_limit = float(value)
                elif key == 'confidence_threshold':
                    self.confidence_threshold = float(value)
                elif key == 'max_drawdown_limit':
                    self.max_drawdown_limit = float(value)
                elif key == 'volatility_multiplier':
                    self.volatility_multiplier = float(value)
            
            cursor.close()
            
            logger.info("Strategy configuration loaded")
        except Exception as e:
            logger.error(f"Failed to load strategy configuration: {e}")
            raise
    
    def evaluate_forecast_risk(self, forecast):
        """Evaluate the risk of a forecast and determine if it should be executed"""
        logger.info(f"Evaluating risk for forecast: {forecast['asset']} ({forecast['horizon']})")
        
        # Extract forecast data
        asset = forecast['asset']
        prediction = forecast['prediction']
        confidence = forecast['confidence']
        
        # Risk assessment criteria
        risk_assessment = {
            'asset': asset,
            'horizon': forecast['horizon'],
            'prediction': prediction,
            'confidence': confidence,
            'approved': False,
            'risk_score': 0.0,
            'reasons': []
        }
        
        # Calculate risk score based on various factors
        risk_score = 0.0
        
        # 1. Confidence check
        if confidence < self.confidence_threshold:
            risk_assessment['reasons'].append(f"Low confidence ({confidence:.2f} < {self.confidence_threshold:.2f})")
        else:
            risk_score += confidence * 0.3
        
        # 2. Prediction magnitude check
        abs_prediction = abs(prediction)
        if abs_prediction > 0.1:  # More than 10% prediction
            risk_assessment['reasons'].append(f"Large prediction magnitude ({abs_prediction:.2f})")
        else:
            risk_score += (1 - abs_prediction) * 0.2
        
        # 3. Position size check (simplified)
        position_size = min(abs_prediction * self.risk_factor, self.position_size_limit)
        if position_size > self.position_size_limit:
            risk_assessment['reasons'].append(f"Position size exceeds limit ({position_size:.2f} > {self.position_size_limit:.2f})")
        else:
            risk_score += (1 - position_size / self.position_size_limit) * 0.3
        
        # 4. Volatility adjustment (simplified)
        # In a real implementation, this would fetch actual volatility data
        volatility = np.random.rand() * 0.05  # Random volatility between 0 and 5%
        adjusted_position_size = position_size * (1 - volatility * self.volatility_multiplier)
        
        if volatility > 0.03:  # High volatility (3%+)
            risk_assessment['reasons'].append(f"High volatility ({volatility:.2f})")
        else:
            risk_score += (1 - volatility / 0.03) * 0.2
        
        # Set final risk score
        risk_assessment['risk_score'] = min(risk_score, 1.0)
        risk_assessment['position_size'] = max(0, adjusted_position_size)
        
        # Approval decision
        # A forecast is approved if:
        # 1. Confidence is above threshold
        # 2. Position size is within limits
        # 3. Risk score is above a minimum threshold (0.5)
        if (confidence >= self.confidence_threshold and 
            adjusted_position_size <= self.position_size_limit and
            risk_score >= 0.5):
            risk_assessment['approved'] = True
            risk_assessment['reasons'].append("Risk assessment passed")
        else:
            risk_assessment['reasons'].append("Risk assessment failed")
        
        logger.info(f"Risk assessment completed: approved={risk_assessment['approved']}, score={risk_assessment['risk_score']:.2f}")
        
        return risk_assessment
    
    def adjust_strategy_parameters(self):
        """Dynamically adjust strategy parameters based on market conditions"""
        logger.info("Adjusting strategy parameters")
        
        try:
            # In a real implementation, this would analyze:
            # 1. Recent trade performance
            # 2. Market volatility
            # 3. Drawdown levels
            # 4. Portfolio performance
            
            # For demonstration, we'll randomly adjust parameters
            # This is just a placeholder - in reality, this would be based on real analytics
            
            cursor = self.db_conn.cursor()
            
            # Example: Adjust risk factor based on recent performance
            # (In reality, this would be based on actual performance data)
            performance_indicator = np.random.rand()  # Random for demo
            
            if performance_indicator < 0.3:  # Poor performance
                new_risk_factor = max(0.1, self.risk_factor * 0.9)
                update_query = """
                INSERT INTO trading_strategyconfig (key, value)
                VALUES (%s, %s)
                ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value
                """
                cursor.execute(update_query, ('risk_factor', str(new_risk_factor)))
                self.risk_factor = new_risk_factor
                logger.info(f"Reduced risk factor to {new_risk_factor:.2f} due to poor performance")
            
            elif performance_indicator > 0.7:  # Good performance
                new_risk_factor = min(2.0, self.risk_factor * 1.1)
                update_query = """
                INSERT INTO trading_strategyconfig (key, value)
                VALUES (%s, %s)
                ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value
                """
                cursor.execute(update_query, ('risk_factor', str(new_risk_factor)))
                self.risk_factor = new_risk_factor
                logger.info(f"Increased risk factor to {new_risk_factor:.2f} due to good performance")
            
            self.db_conn.commit()
            cursor.close()
            
            logger.info("Strategy parameters adjusted")
        
        except Exception as e:
            logger.error(f"Failed to adjust strategy parameters: {e}")
            self.db_conn.rollback()
            raise
    
    def handle_forecast_update(self, forecast_data):
        """Handle incoming forecast update from Redis"""
        logger.info(f"Handling forecast update for {forecast_data['asset']}")
        
        try:
            # Evaluate risk
            risk_assessment = self.evaluate_forecast_risk(forecast_data)
            
            # Save risk assessment to database
            self.save_risk_assessment(risk_assessment)
            
            # If approved, publish to execution channel
            if risk_assessment['approved']:
                self.publish_approved_trade(risk_assessment)
            
            # Periodically adjust strategy parameters
            # In a real implementation, this would be based on a timer or specific conditions
            if np.random.rand() < 0.1:  # 10% chance per forecast
                self.adjust_strategy_parameters()
                self.load_strategy_config()  # Reload updated config
        
        except Exception as e:
            logger.error(f"Failed to handle forecast update: {e}")
            raise
    
    def save_risk_assessment(self, risk_assessment):
        """Save risk assessment to database (simplified)"""
        logger.info("Saving risk assessment to database")
        
        # In a real implementation, this would save to a dedicated risk assessment table
        # For now, we'll just log it
        logger.info(f"Risk assessment saved: {risk_assessment}")
    
    def publish_approved_trade(self, risk_assessment):
        """Publish approved trade to Redis for execution"""
        logger.info("Publishing approved trade to Redis")
        
        try:
            # Create trade signal
            trade_signal = {
                'asset': risk_assessment['asset'],
                'horizon': risk_assessment['horizon'],
                'prediction': risk_assessment['prediction'],
                'position_size': risk_assessment['position_size'],
                'confidence': risk_assessment['confidence'],
                'risk_score': risk_assessment['risk_score'],
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
            
            # Publish to execution channel
            self.redis_client.publish('approved_trades', json.dumps(trade_signal))
            logger.info(f"Approved trade published for {trade_signal['asset']}")
        
        except Exception as e:
            logger.error(f"Failed to publish approved trade: {e}")
            raise
    
    def listen_for_forecasts(self):
        """Listen for forecast updates from Redis"""
        logger.info("Starting to listen for forecast updates")
        
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe('forecast_updates')
        
        try:
            for message in pubsub.listen():
                if message['type'] == 'message':
                    try:
                        forecast_data = json.loads(message['data'])
                        self.handle_forecast_update(forecast_data)
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to decode forecast data: {e}")
                    except Exception as e:
                        logger.error(f"Error handling forecast update: {e}")
        
        except Exception as e:
            logger.error(f"Error in forecast listener: {e}")
            raise
        finally:
            pubsub.close()
    
    def run(self):
        """Run the risk engine"""
        logger.info("Starting risk engine")
        
        # Start listening for forecasts
        self.listen_for_forecasts()


def main():
    """Main entry point"""
    engine = RiskEngine()
    
    # Run the risk engine
    engine.run()


if __name__ == "__main__":
    main()
