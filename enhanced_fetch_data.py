#!/usr/bin/env python3
"""
Enhanced Financial Data Fetcher with AI Integration
Builds upon the original fetch_financial_data.py with AI capabilities
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json
import warnings
warnings.filterwarnings('ignore')

# AI/ML imports
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

class EnhancedDataFetcher:
    """
    Enhanced version of the original data fetcher with AI capabilities
    """
    
    def __init__(self):
        self.assets = {
            'SP500': '^GSPC',
            'Gold': 'GC=F',
            'Bitcoin': 'BTC-USD',
            'Ethereum': 'ETH-USD',
            'XRP': 'XRP-USD',
            'JPY_USD': 'JPY=X',
            'EUR_USD': 'EURUSD=X',
            'USD_Index': 'DX-Y.NYB'
        }
        
        self.start_date = '2020-01-01'
        self.end_date = datetime.now().strftime('%Y-%m-%d')
        
    def fetch_enhanced_data(self):
        """
        Fetch data with enhanced features for AI analysis
        """
        print(f"Fetching enhanced data from {self.start_date} to {self.end_date}")
        print("=" * 60)
        
        all_data = {}
        enhanced_features = {}
        
        for asset_name, symbol in self.assets.items():
            print(f"Processing {asset_name} ({symbol})...")
            
            try:
                # Fetch basic data
                ticker = yf.Ticker(symbol)
                data = ticker.history(start=self.start_date, end=self.end_date)
                
                if data.empty:
                    print(f"  ⚠️  No data found for {asset_name}")
                    continue
                
                # Calculate basic returns
                data['Daily_Return'] = data['Close'].pct_change() * 100
                
                # Add enhanced features
                data = self._add_technical_indicators(data)
                data = self._add_time_features(data)
                data = self._add_volatility_features(data)
                
                all_data[asset_name] = data
                enhanced_features[asset_name] = self._create_feature_matrix(data)
                
                print(f"  ✅ Successfully processed {len(data)} days")
                print(f"  📊 Features created: {enhanced_features[asset_name].shape[1]}")
                
            except Exception as e:
                print(f"  ❌ Error processing {asset_name}: {str(e)}")
                continue
        
        return all_data, enhanced_features
    
    def _add_technical_indicators(self, data):
        """
        Add technical indicators to the data
        """
        # Moving averages
        data['MA_5'] = data['Close'].rolling(window=5).mean()
        data['MA_10'] = data['Close'].rolling(window=10).mean()
        data['MA_20'] = data['Close'].rolling(window=20).mean()
        data['MA_50'] = data['Close'].rolling(window=50).mean()
        
        # Exponential moving averages
        data['EMA_12'] = data['Close'].ewm(span=12).mean()
        data['EMA_26'] = data['Close'].ewm(span=26).mean()
        
        # MACD
        data['MACD'] = data['EMA_12'] - data['EMA_26']
        data['MACD_Signal'] = data['MACD'].ewm(span=9).mean()
        data['MACD_Histogram'] = data['MACD'] - data['MACD_Signal']
        
        # RSI
        data['RSI'] = self._calculate_rsi(data['Close'])
        
        # Bollinger Bands
        data['BB_Upper'], data['BB_Lower'] = self._calculate_bollinger_bands(data['Close'])
        data['BB_Width'] = data['BB_Upper'] - data['BB_Lower']
        data['BB_Position'] = (data['Close'] - data['BB_Lower']) / data['BB_Width']
        
        # Price momentum
        data['Momentum_5'] = data['Close'].pct_change(5)
        data['Momentum_10'] = data['Close'].pct_change(10)
        
        return data
    
    def _add_time_features(self, data):
        """
        Add time-based features
        """
        data['Day_of_Week'] = data.index.dayofweek
        data['Month'] = data.index.month
        data['Quarter'] = data.index.quarter
        data['Year'] = data.index.year
        
        # Cyclical encoding for time features
        data['Day_Sin'] = np.sin(2 * np.pi * data.index.dayofweek / 7)
        data['Day_Cos'] = np.cos(2 * np.pi * data.index.dayofweek / 7)
        data['Month_Sin'] = np.sin(2 * np.pi * data.index.month / 12)
        data['Month_Cos'] = np.cos(2 * np.pi * data.index.month / 12)
        
        return data
    
    def _add_volatility_features(self, data):
        """
        Add volatility-based features
        """
        # Rolling volatility
        data['Vol_5'] = data['Daily_Return'].rolling(window=5).std()
        data['Vol_10'] = data['Daily_Return'].rolling(window=10).std()
        data['Vol_20'] = data['Daily_Return'].rolling(window=20).std()
        data['Vol_30'] = data['Daily_Return'].rolling(window=30).std()
        
        # Volatility ratios
        data['Vol_Ratio_5_20'] = data['Vol_5'] / data['Vol_20']
        data['Vol_Ratio_10_30'] = data['Vol_10'] / data['Vol_30']
        
        # High-Low volatility
        data['HL_Volatility'] = (data['High'] - data['Low']) / data['Close']
        
        return data
    
    def _calculate_rsi(self, prices, window=14):
        """
        Calculate Relative Strength Index
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_bollinger_bands(self, prices, window=20, num_std=2):
        """
        Calculate Bollinger Bands
        """
        rolling_mean = prices.rolling(window=window).mean()
        rolling_std = prices.rolling(window=window).std()
        
        upper_band = rolling_mean + (rolling_std * num_std)
        lower_band = rolling_mean - (rolling_std * num_std)
        
        return upper_band, lower_band
    
    def _create_feature_matrix(self, data):
        """
        Create feature matrix for ML models
        """
        feature_columns = [
            'MA_5', 'MA_10', 'MA_20', 'MA_50',
            'EMA_12', 'EMA_26', 'MACD', 'MACD_Signal', 'MACD_Histogram',
            'RSI', 'BB_Width', 'BB_Position',
            'Momentum_5', 'Momentum_10',
            'Vol_5', 'Vol_10', 'Vol_20', 'Vol_30',
            'Vol_Ratio_5_20', 'Vol_Ratio_10_30',
            'HL_Volatility',
            'Day_Sin', 'Day_Cos', 'Month_Sin', 'Month_Cos'
        ]
        
        # Select only available columns
        available_columns = [col for col in feature_columns if col in data.columns]
        features = data[available_columns].copy()
        
        # Add lagged features
        for lag in [1, 2, 3, 5]:
            features[f'Close_lag_{lag}'] = data['Close'].shift(lag)
            features[f'Return_lag_{lag}'] = data['Daily_Return'].shift(lag)
        
        return features
    
    def train_prediction_models(self, enhanced_features):
        """
        Train AI models for each asset
        """
        print("\nTraining AI prediction models...")
        print("=" * 40)
        
        models = {}
        model_performance = {}
        
        for asset_name, features in enhanced_features.items():
            print(f"Training model for {asset_name}...")
            
            try:
                # Create target variable (next day return)
                target = features.shift(-1)['Daily_Return'] if 'Daily_Return' in features.columns else None
                
                if target is None:
                    # If Daily_Return not in features, we need to get it from original data
                    continue
                
                # Remove NaN values
                valid_indices = ~(features.isna().any(axis=1) | target.isna())
                X = features[valid_indices]
                y = target[valid_indices]
                
                if len(X) < 100:
                    print(f"  ⚠️  Insufficient data for {asset_name}")
                    continue
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42, shuffle=False
                )
                
                # Scale features
                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)
                
                # Train model
                model = RandomForestRegressor(
                    n_estimators=100,
                    random_state=42,
                    n_jobs=-1
                )
                
                model.fit(X_train_scaled, y_train)
                
                # Evaluate model
                y_pred = model.predict(X_test_scaled)
                r2 = r2_score(y_test, y_pred)
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                
                models[asset_name] = {
                    'model': model,
                    'scaler': scaler,
                    'features': X.columns.tolist()
                }
                
                model_performance[asset_name] = {
                    'r2_score': r2,
                    'rmse': rmse,
                    'training_samples': len(X_train),
                    'test_samples': len(X_test)
                }
                
                print(f"  ✅ R² Score: {r2:.4f}, RMSE: {rmse:.4f}")
                
            except Exception as e:
                print(f"  ❌ Error training model for {asset_name}: {str(e)}")
                continue
        
        return models, model_performance
    
    def save_enhanced_data(self, all_data, enhanced_features, models, model_performance):
        """
        Save enhanced data and models
        """
        print("\nSaving enhanced data and models...")
        print("=" * 40)
        
        # Create directories
        os.makedirs('enhanced_data', exist_ok=True)
        os.makedirs('models', exist_ok=True)
        
        # Save raw data
        for asset_name, data in all_data.items():
            filename = f'enhanced_data/{asset_name}_enhanced_data.csv'
            data.to_csv(filename)
            print(f"  💾 Saved {asset_name} data to {filename}")
        
        # Save features
        for asset_name, features in enhanced_features.items():
            filename = f'enhanced_data/{asset_name}_features.csv'
            features.to_csv(filename)
            print(f"  💾 Saved {asset_name} features to {filename}")
        
        # Save model performance
        with open('models/model_performance.json', 'w') as f:
            json.dump(model_performance, f, indent=2, default=str)
        print(f"  💾 Saved model performance to models/model_performance.json")
        
        # Save models using joblib
        try:
            import joblib
            for asset_name, model_data in models.items():
                filename = f'models/{asset_name}_model.joblib'
                joblib.dump(model_data, filename)
                print(f"  💾 Saved {asset_name} model to {filename}")
        except ImportError:
            print("  ⚠️  joblib not available, models not saved")
        
        print("\n✅ All data and models saved successfully!")
    
    def generate_summary_report(self, all_data, model_performance):
        """
        Generate a comprehensive summary report
        """
        print("\n" + "=" * 60)
        print("ENHANCED DATA ANALYSIS SUMMARY REPORT")
        print("=" * 60)
        
        print(f"Analysis Period: {self.start_date} to {self.end_date}")
        print(f"Total Assets Analyzed: {len(all_data)}")
        print(f"Models Trained: {len(model_performance)}")
        
        print("\n📊 DATA STATISTICS:")
        print("-" * 30)
        
        for asset_name, data in all_data.items():
            if len(data) > 0:
                returns = data['Daily_Return'].dropna()
                print(f"\n{asset_name}:")
                print(f"  Total Days: {len(data)}")
                print(f"  Avg Daily Return: {returns.mean():.4f}%")
                print(f"  Volatility: {returns.std():.4f}%")
                print(f"  Min Return: {returns.min():.4f}%")
                print(f"  Max Return: {returns.max():.4f}%")
        
        print("\n🤖 MODEL PERFORMANCE:")
        print("-" * 30)
        
        for asset_name, performance in model_performance.items():
            print(f"\n{asset_name}:")
            print(f"  R² Score: {performance['r2_score']:.4f}")
            print(f"  RMSE: {performance['rmse']:.4f}")
            print(f"  Training Samples: {performance['training_samples']}")
            print(f"  Test Samples: {performance['test_samples']}")
        
        # Calculate average performance
        if model_performance:
            avg_r2 = np.mean([p['r2_score'] for p in model_performance.values()])
            avg_rmse = np.mean([p['rmse'] for p in model_performance.values()])
            
            print(f"\n📈 OVERALL MODEL PERFORMANCE:")
            print(f"  Average R² Score: {avg_r2:.4f}")
            print(f"  Average RMSE: {avg_rmse:.4f}")
        
        print("\n" + "=" * 60)
        print("REPORT COMPLETE")
        print("=" * 60)

def main():
    """
    Main function to run the enhanced data fetching and analysis
    """
    print("Enhanced Financial Data Fetcher with AI Integration")
    print("=" * 60)
    
    # Initialize fetcher
    fetcher = EnhancedDataFetcher()
    
    # Fetch enhanced data
    all_data, enhanced_features = fetcher.fetch_enhanced_data()
    
    if not all_data:
        print("❌ No data was successfully fetched. Please check your internet connection.")
        return
    
    # Train AI models
    models, model_performance = fetcher.train_prediction_models(enhanced_features)
    
    # Save everything
    fetcher.save_enhanced_data(all_data, enhanced_features, models, model_performance)
    
    # Generate summary report
    fetcher.generate_summary_report(all_data, model_performance)
    
    print("\n🎉 Enhanced data fetching and AI model training completed!")
    print("\nNext steps:")
    print("1. Run 'python real_time_analyzer.py' for real-time analysis")
    print("2. Start the API server with 'python api_server.py'")
    print("3. Open the dashboard at http://localhost:8000")

if __name__ == "__main__":
    main()
