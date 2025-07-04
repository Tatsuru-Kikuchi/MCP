import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import warnings
warnings.filterwarnings('ignore')

def get_daily_returns_data():
    """
    Collect daily returns data for S&P 500, Gold, BTC, ETH, and XRP
    from January 1, 2020 to December 31, 2025
    """
    
    # Define the assets and their Yahoo Finance tickers
    assets = {
        'SP500': '^GSPC',     # S&P 500 Index
        'Gold': 'GC=F',       # Gold Futures
        'BTC': 'BTC-USD',     # Bitcoin
        'ETH': 'ETH-USD',     # Ethereum
        'XRP': 'XRP-USD'      # XRP
    }
    
    # Define date range
    start_date = '2020-01-01'
    end_date = '2025-12-31'
    
    print(f"Collecting data from {start_date} to {end_date}")
    
    # Dictionary to store all data
    all_data = {}
    daily_returns = {}
    
    for asset_name, ticker in assets.items():
        try:
            print(f"Downloading {asset_name} ({ticker})...")
            
            # Download historical data
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)
            
            if data.empty:
                print(f"Warning: No data found for {asset_name}")
                continue
            
            # Calculate daily returns (percentage change)
            data['Daily_Return'] = data['Adj Close'].pct_change() * 100
            
            # Store the data
            all_data[asset_name] = data
            daily_returns[asset_name] = data['Daily_Return'].dropna()
            
            print(f"Successfully collected {len(data)} data points for {asset_name}")
            
        except Exception as e:
            print(f"Error downloading {asset_name}: {str(e)}")
    
    return all_data, daily_returns

def create_summary_statistics(daily_returns):
    """Create summary statistics for the dashboard"""
    
    summary_stats = {}
    
    for asset, returns in daily_returns.items():
        if len(returns) == 0:
            continue
            
        stats = {
            'mean_return': returns.mean(),
            'std_return': returns.std(),
            'min_return': returns.min(),
            'max_return': returns.max(),
            'sharpe_ratio': returns.mean() / returns.std() * np.sqrt(252) if returns.std() != 0 else 0,
            'total_observations': len(returns),
            'positive_days': (returns > 0).sum(),
            'negative_days': (returns < 0).sum(),
            'zero_days': (returns == 0).sum(),
            'start_date': returns.index[0].strftime('%Y-%m-%d'),
            'end_date': returns.index[-1].strftime('%Y-%m-%d'),
            'best_day': returns.max(),
            'worst_day': returns.min(),
            'volatility_annualized': returns.std() * np.sqrt(252)
        }
        summary_stats[asset] = stats
    
    return summary_stats

def create_correlation_matrix(daily_returns):
    """Create correlation matrix between assets"""
    
    # Create a combined dataframe for correlation analysis
    combined_returns = pd.DataFrame()
    
    for asset, returns in daily_returns.items():
        combined_returns[asset] = returns
    
    # Calculate correlation matrix
    correlation_matrix = combined_returns.corr()
    
    return correlation_matrix

def save_data_to_files(all_data, daily_returns, summary_stats, correlation_matrix):
    """Save data to CSV and JSON files"""
    
    # Create a combined dataframe for daily returns
    combined_returns = pd.DataFrame()
    
    for asset, returns in daily_returns.items():
        combined_returns[f'{asset}_Daily_Return'] = returns
    
    # Save combined daily returns to CSV
    combined_returns.to_csv('daily_returns_2020_2025.csv')
    print("Saved daily_returns_2020_2025.csv")
    
    # Save individual asset data
    for asset, data in all_data.items():
        filename = f'{asset}_historical_data_2020_2025.csv'
        data.to_csv(filename)
        print(f"Saved {filename}")
    
    # Save summary statistics to JSON
    with open('summary_statistics.json', 'w') as f:
        # Convert numpy types to Python types for JSON serialization
        json_stats = {}
        for asset, stats in summary_stats.items():
            json_stats[asset] = {k: float(v) if isinstance(v, (np.float64, np.int64)) else v 
                               for k, v in stats.items()}
        json.dump(json_stats, f, indent=2)
    print("Saved summary_statistics.json")
    
    # Save correlation matrix to CSV
    correlation_matrix.to_csv('correlation_matrix.csv')
    print("Saved correlation_matrix.csv")
    
    return combined_returns

def create_monthly_summary(daily_returns):
    """Create monthly summary statistics"""
    
    monthly_stats = {}
    
    for asset, returns in daily_returns.items():
        if len(returns) == 0:
            continue
            
        # Resample to monthly
        monthly_returns = returns.resample('M').apply(lambda x: (1 + x/100).prod() - 1) * 100
        
        monthly_stats[asset] = {
            'monthly_returns': monthly_returns.tolist(),
            'monthly_dates': [d.strftime('%Y-%m') for d in monthly_returns.index],
            'best_month': monthly_returns.max(),
            'worst_month': monthly_returns.min(),
            'avg_monthly_return': monthly_returns.mean(),
            'monthly_volatility': monthly_returns.std()
        }
    
    return monthly_stats

def main():
    """Main function to execute the data collection"""
    print("Starting financial data collection...")
    print("=" * 50)
    
    # Collect the data
    all_data, daily_returns = get_daily_returns_data()
    
    if not daily_returns:
        print("No data was collected. Exiting.")
        return
    
    print("\n" + "=" * 50)
    print("Calculating summary statistics...")
    
    # Create summary statistics
    summary_stats = create_summary_statistics(daily_returns)
    
    # Create correlation matrix
    correlation_matrix = create_correlation_matrix(daily_returns)
    
    # Create monthly summary
    monthly_summary = create_monthly_summary(daily_returns)
    
    print("\n" + "=" * 50)
    print("Saving data to files...")
    
    # Save all data
    combined_returns = save_data_to_files(all_data, daily_returns, summary_stats, correlation_matrix)
    
    # Save monthly summary
    with open('monthly_summary.json', 'w') as f:
        json_stats = {}
        for asset, stats in monthly_summary.items():
            json_stats[asset] = {k: [float(v) if isinstance(v, (np.float64, np.int64)) else v for v in val] 
                               if isinstance(val, list) else float(val) if isinstance(val, (np.float64, np.int64)) else val
                               for k, val in stats.items()}
        json.dump(json_stats, f, indent=2)
    print("Saved monthly_summary.json")
    
    print("\n" + "=" * 50)
    print("Data collection completed successfully!")
    print("\nSummary:")
    
    for asset, stats in summary_stats.items():
        print(f"\n{asset}:")
        print(f"  - Mean daily return: {stats['mean_return']:.4f}%")
        print(f"  - Volatility (std): {stats['std_return']:.4f}%")
        print(f"  - Annualized volatility: {stats['volatility_annualized']:.4f}%")
        print(f"  - Sharpe ratio (annualized): {stats['sharpe_ratio']:.4f}")
        print(f"  - Best day: {stats['best_day']:.4f}%")
        print(f"  - Worst day: {stats['worst_day']:.4f}%")
        print(f"  - Total observations: {stats['total_observations']}")
        print(f"  - Positive days: {stats['positive_days']} ({stats['positive_days']/stats['total_observations']*100:.1f}%)")
        print(f"  - Date range: {stats['start_date']} to {stats['end_date']}")
    
    print("\n" + "=" * 50)
    print("Correlation Matrix:")
    print(correlation_matrix.round(3))

if __name__ == "__main__":
    main()
