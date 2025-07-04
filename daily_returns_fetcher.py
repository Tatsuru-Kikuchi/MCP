import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def fetch_daily_returns(symbols, start_date, end_date):
    """
    Fetch daily returns for given symbols from Yahoo Finance
    
    Parameters:
    symbols (dict): Dictionary with asset names as keys and Yahoo Finance symbols as values
    start_date (str): Start date in 'YYYY-MM-DD' format
    end_date (str): End date in 'YYYY-MM-DD' format
    
    Returns:
    pd.DataFrame: DataFrame with daily returns for all assets
    """
    
    print(f"Fetching data from {start_date} to {end_date}")
    print("Assets:", list(symbols.keys()))
    
    # Dictionary to store all returns
    all_returns = {}
    
    for asset_name, symbol in symbols.items():
        try:
            print(f"Fetching data for {asset_name} ({symbol})...")
            
            # Download data
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date)
            
            if data.empty:
                print(f"Warning: No data found for {asset_name} ({symbol})")
                continue
            
            # Calculate daily returns
            daily_returns = data['Close'].pct_change().dropna()
            
            # Store in dictionary
            all_returns[asset_name] = daily_returns
            
            print(f"Successfully fetched {len(daily_returns)} daily returns for {asset_name}")
            
        except Exception as e:
            print(f"Error fetching data for {asset_name} ({symbol}): {str(e)}")
            continue
    
    # Combine all returns into a single DataFrame
    if all_returns:
        returns_df = pd.DataFrame(all_returns)
        returns_df.index.name = 'Date'
        return returns_df
    else:
        print("No data was successfully fetched for any asset.")
        return pd.DataFrame()

def main():
    # Define symbols for each asset
    # Note: Some symbols might need adjustment based on Yahoo Finance availability
    symbols = {
        'SP500': '^GSPC',      # S&P 500 Index
        'Gold': 'GC=F',        # Gold Futures
        'BTC': 'BTC-USD',      # Bitcoin
        'ETH': 'ETH-USD',      # Ethereum
        'XRP': 'XRP-USD'       # XRP
    }
    
    # Define date range
    start_date = '2021-01-01'
    end_date = '2025-12-31'
    
    # Fetch daily returns
    returns_df = fetch_daily_returns(symbols, start_date, end_date)
    
    if not returns_df.empty:
        # Display summary statistics
        print("\nSummary Statistics:")
        print("=" * 50)
        print(f"Date range: {returns_df.index.min()} to {returns_df.index.max()}")
        print(f"Number of trading days: {len(returns_df)}")
        print(f"Assets: {', '.join(returns_df.columns)}")
        
        print("\nDaily Returns Statistics:")
        print(returns_df.describe())
        
        # Save to CSV
        csv_filename = 'daily_returns_2021_2025.csv'
        returns_df.to_csv(csv_filename)
        print(f"\nData saved to {csv_filename}")
        
        # Display first few rows
        print("\nFirst 10 rows of data:")
        print(returns_df.head(10))
        
        # Display last few rows
        print("\nLast 10 rows of data:")
        print(returns_df.tail(10))
        
        return returns_df
    else:
        print("Failed to fetch any data.")
        return None

if __name__ == "__main__":
    # Install required packages if not already installed
    print("Make sure you have yfinance installed: pip install yfinance")
    print("Starting data fetch...")
    
    # Run the main function
    df = main()
