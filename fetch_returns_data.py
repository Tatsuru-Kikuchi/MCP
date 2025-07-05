import yfinance as yf
import pandas as pd
from datetime import datetime
import json

# Define the assets and their Yahoo Finance tickers
assets = {
    'SP500': '^GSPC',
    'Gold': 'GC=F',
    'BTC': 'BTC-USD',
    'ETH': 'ETH-USD',
    'XRP': 'XRP-USD'
}

# Define date range
start_date = '2020-01-01'
end_date = '2024-12-31'

# Dictionary to store data for each asset
all_returns = {}

# Fetch data for each asset
for asset_name, ticker in assets.items():
    print(f"Fetching data for {asset_name} ({ticker})...")
    
    try:
        # Download data
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        if data.empty:
            print(f"No data found for {asset_name}")
            continue
            
        # Calculate daily returns
        data['Daily_Return'] = data['Close'].pct_change()
        
        # Create a clean dataframe with date, close price, and returns
        returns_df = pd.DataFrame({
            'Date': data.index.strftime('%Y-%m-%d'),
            'Close': data['Close'].round(2),
            'Daily_Return': (data['Daily_Return'] * 100).round(4)  # Convert to percentage
        })
        returns_df = returns_df.dropna()  # Remove first row with NaN
        
        # Save individual CSV file
        filename = f'{asset_name}_daily_returns_2020_2024.csv'
        returns_df.to_csv(filename, index=False)
        print(f"✓ Saved {filename}")
        
        # Store for combined file
        all_returns[asset_name] = returns_df
        
    except Exception as e:
        print(f"Error fetching {asset_name}: {str(e)}")

# Create a combined file with all assets
if all_returns:
    # Create a merged dataframe with all assets
    combined_df = None
    for asset_name, df in all_returns.items():
        if combined_df is None:
            combined_df = df.rename(columns={
                'Close': f'{asset_name}_Close',
                'Daily_Return': f'{asset_name}_Return'
            })
        else:
            asset_df = df[['Date', 'Close', 'Daily_Return']].rename(columns={
                'Close': f'{asset_name}_Close',
                'Daily_Return': f'{asset_name}_Return'
            })
            combined_df = pd.merge(combined_df, asset_df, on='Date', how='outer')
    
    # Save combined file
    combined_df.to_csv('all_assets_daily_returns_2020_2024.csv', index=False)
    print("\n✓ Saved combined file: all_assets_daily_returns_2020_2024.csv")
    
    # Create summary statistics
    summary = {}
    for asset_name in assets.keys():
        if f'{asset_name}_Return' in combined_df.columns:
            returns = combined_df[f'{asset_name}_Return'].dropna()
            summary[asset_name] = {
                'mean_daily_return': round(returns.mean(), 4),
                'std_daily_return': round(returns.std(), 4),
                'min_return': round(returns.min(), 4),
                'max_return': round(returns.max(), 4),
                'total_days': len(returns)
            }
    
    with open('returns_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print("✓ Saved summary statistics: returns_summary.json")

print("\nData collection complete!")