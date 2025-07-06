#!/usr/bin/env python3
"""
Financial Data Fetcher for S&P 500, Gold, BTC, ETH, XRP, and Currency Pairs
Fetches daily price data from Yahoo Finance and calculates daily returns
Period: January 1, 2020 to December 31, 2024
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def fetch_financial_data():
    """
    Fetch historical data for specified assets and calculate daily returns
    """
    
    # Define the assets and their Yahoo Finance symbols
    assets = {
        # Original assets
        'SP500': '^GSPC',      # S&P 500 Index
        'Gold': 'GC=F',        # Gold Futures
        'Bitcoin': 'BTC-USD',   # Bitcoin
        'Ethereum': 'ETH-USD',  # Ethereum
        'XRP': 'XRP-USD',      # XRP
        
        # Currency pairs and indices
        'JPY_USD': 'JPY=X',     # Japanese Yen to USD
        'EUR_USD': 'EURUSD=X',  # Euro to USD
        'USD_Index': 'DX-Y.NYB' # US Dollar Index
    }
    
    # Define date range
    start_date = '2020-01-01'
    end_date = '2024-12-31'
    
    print(f"Fetching data from {start_date} to {end_date}")
    print("Assets:", list(assets.keys()))
    print("-" * 50)
    
    # Dictionary to store all data
    all_data = {}
    daily_returns = {}
    
    # Fetch data for each asset
    for asset_name, symbol in assets.items():
        print(f"Fetching data for {asset_name} ({symbol})...")
        
        try:
            # Download data from Yahoo Finance
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date)
            
            if data.empty:
                print(f"  Warning: No data found for {asset_name}")
                continue
            
            # Calculate daily returns (percentage change in adjusted close)
            data['Daily_Return'] = data['Close'].pct_change() * 100
            
            # Store the data
            all_data[asset_name] = data
            daily_returns[asset_name] = data['Daily_Return'].dropna()
            
            print(f"  Successfully fetched {len(data)} days of data")
            print(f"  Date range: {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}")
            print(f"  Daily returns calculated: {len(daily_returns[asset_name])} observations")
            
        except Exception as e:
            print(f"  Error fetching data for {asset_name}: {str(e)}")
            continue
    
    return all_data, daily_returns

def save_data_to_csv(all_data, daily_returns):
    """
    Save the fetched data and daily returns to CSV files
    """
    
    # Create data directory if it doesn't exist
    data_dir = 'financial_data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    print("\nSaving data to CSV files...")
    print("-" * 50)
    
    # Save individual asset data
    for asset_name, data in all_data.items():
        filename = f"{data_dir}/{asset_name}_daily_data_2020_2024.csv"
        data.to_csv(filename)
        print(f"Saved {asset_name} full data to {filename}")
    
    # Create a combined daily returns DataFrame
    combined_returns = pd.DataFrame()
    for asset_name, returns in daily_returns.items():
        combined_returns[asset_name] = returns
    
    # Save combined daily returns
    returns_filename = f"{data_dir}/combined_daily_returns_2020_2024.csv"
    combined_returns.to_csv(returns_filename)
    print(f"Saved combined daily returns to {returns_filename}")
    
    # Create summary statistics
    summary_stats = combined_returns.describe()
    summary_filename = f"{data_dir}/daily_returns_summary_stats.csv"
    summary_stats.to_csv(summary_filename)
    print(f"Saved summary statistics to {summary_filename}")
    
    return combined_returns

def analyze_returns(daily_returns_df):
    """
    Perform basic analysis on the daily returns
    """
    print("\nDaily Returns Analysis Summary:")
    print("=" * 50)
    
    for asset in daily_returns_df.columns:
        returns = daily_returns_df[asset].dropna()
        
        print(f"\n{asset}:")
        print(f"  Total observations: {len(returns)}")
        print(f"  Mean daily return: {returns.mean():.4f}%")
        print(f"  Standard deviation: {returns.std():.4f}%")
        print(f"  Min daily return: {returns.min():.4f}%")
        print(f"  Max daily return: {returns.max():.4f}%")
        print(f"  Annualized volatility: {returns.std() * np.sqrt(252):.4f}%")
        
        # Add currency-specific information
        if asset in ['JPY_USD', 'EUR_USD', 'USD_Index']:
            print(f"  Asset type: Currency")
    
    # Calculate correlation matrix
    print(f"\nCorrelation Matrix:")
    print("-" * 30)
    correlation_matrix = daily_returns_df.corr()
    print(correlation_matrix.round(4))
    
    # Separate correlation analysis for currencies
    currency_cols = ['JPY_USD', 'EUR_USD', 'USD_Index']
    if all(col in daily_returns_df.columns for col in currency_cols):
        print(f"\nCurrency Correlations with Other Assets:")
        print("-" * 40)
        non_currency_cols = [col for col in daily_returns_df.columns if col not in currency_cols]
        for currency in currency_cols:
            print(f"\n{currency}:")
            for asset in non_currency_cols:
                corr = daily_returns_df[currency].corr(daily_returns_df[asset])
                print(f"  vs {asset}: {corr:.4f}")
    
    return correlation_matrix

def main():
    """
    Main function to execute the data fetching and analysis
    """
    print("Financial Data Fetcher with Currency Analysis")
    print("=" * 50)
    print("Fetching daily data for S&P 500, Gold, Bitcoin, Ethereum, XRP,")
    print("and Currency Pairs (JPY/USD, EUR/USD, USD Index)")
    print("Period: January 1, 2020 to December 31, 2024")
    print("Source: Yahoo Finance")
    print()
    
    # Fetch the data
    all_data, daily_returns = fetch_financial_data()
    
    if not daily_returns:
        print("No data was successfully fetched. Please check your internet connection and try again.")
        return
    
    # Save to CSV files
    combined_returns = save_data_to_csv(all_data, daily_returns)
    
    # Perform analysis
    correlation_matrix = analyze_returns(combined_returns)
    
    print("\n" + "=" * 50)
    print("Data fetching and analysis completed successfully!")
    print("Files saved in 'financial_data' directory:")
    print("- Individual asset data files")
    print("- combined_daily_returns_2020_2024.csv")
    print("- daily_returns_summary_stats.csv")

if __name__ == "__main__":
    main()
