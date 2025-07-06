import yfinance as yf
import pandas as pd
from datetime import datetime
import json

# Define the assets and their Yahoo Finance tickers (including currencies)
assets = {
    # Original assets
    'SP500': '^GSPC',
    'Gold': 'GC=F',
    'BTC': 'BTC-USD',
    'ETH': 'ETH-USD',
    'XRP': 'XRP-USD',
    
    # Currency pairs and indices
    'JPY_USD': 'JPY=X',      # Japanese Yen to USD (inverted - shows USD strength vs JPY)
    'EUR_USD': 'EURUSD=X',   # Euro to USD
    'USD_Index': 'DX-Y.NYB'  # US Dollar Index
}

def get_currency_description(currency):
    """Get description for currency pairs"""
    descriptions = {
        'JPY_USD': 'Japanese Yen per USD (higher values = stronger USD)',
        'EUR_USD': 'Euro to USD exchange rate',
        'USD_Index': 'US Dollar Index (DXY) - measures USD strength vs basket of currencies'
    }
    return descriptions.get(currency, 'Currency pair')

# Define date range
start_date = '2020-01-01'
end_date = '2024-12-31'

# Dictionary to store data for each asset
all_returns = {}

print("Fetching financial data including currency pairs...")
print("=" * 60)

# Fetch data for each asset
for asset_name, ticker in assets.items():
    print(f"Fetching data for {asset_name} ({ticker})...")
    
    try:
        # Download data
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        if data.empty:
            print(f"  ✗ No data found for {asset_name}")
            continue
            
        # Calculate daily returns
        data['Daily_Return'] = data['Close'].pct_change()
        
        # Create a clean dataframe with date, close price, and returns
        returns_df = pd.DataFrame({
            'Date': data.index.strftime('%Y-%m-%d'),
            'Close': data['Close'].round(6),  # More precision for currency data
            'Daily_Return': (data['Daily_Return'] * 100).round(6)  # Convert to percentage with precision
        })
        returns_df = returns_df.dropna()  # Remove first row with NaN
        
        # Save individual CSV file
        filename = f'{asset_name}_daily_returns_2020_2024.csv'
        returns_df.to_csv(filename, index=False)
        print(f"  ✓ Saved {filename} ({len(returns_df)} data points)")
        
        # Store for combined file
        all_returns[asset_name] = returns_df
        
    except Exception as e:
        print(f"  ✗ Error fetching {asset_name}: {str(e)}")

print("\n" + "=" * 60)
print("Creating combined dataset and analysis...")

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
    combined_df.to_csv('all_assets_daily_returns_with_currencies_2020_2024.csv', index=False)
    print("✓ Saved combined file: all_assets_daily_returns_with_currencies_2020_2024.csv")
    
    # Create enhanced summary statistics
    summary = {}
    currency_assets = ['JPY_USD', 'EUR_USD', 'USD_Index']
    crypto_assets = ['BTC', 'ETH', 'XRP']
    traditional_assets = ['SP500', 'Gold']
    
    for asset_name in assets.keys():
        if f'{asset_name}_Return' in combined_df.columns:
            returns = combined_df[f'{asset_name}_Return'].dropna()
            
            # Basic statistics
            basic_stats = {
                'mean_daily_return': round(returns.mean(), 6),
                'std_daily_return': round(returns.std(), 6),
                'min_return': round(returns.min(), 6),
                'max_return': round(returns.max(), 6),
                'total_days': len(returns),
                'annualized_return': round(returns.mean() * 252, 4),
                'annualized_volatility': round(returns.std() * (252 ** 0.5), 4),
                'sharpe_ratio': round((returns.mean() / returns.std()) * (252 ** 0.5), 4) if returns.std() != 0 else 0
            }
            
            # Asset classification
            if asset_name in currency_assets:
                basic_stats['asset_type'] = 'Currency'
            elif asset_name in crypto_assets:
                basic_stats['asset_type'] = 'Cryptocurrency'
            elif asset_name in traditional_assets:
                basic_stats['asset_type'] = 'Traditional'
            else:
                basic_stats['asset_type'] = 'Other'
            
            # Additional risk metrics
            basic_stats['skewness'] = round(returns.skew(), 4)
            basic_stats['kurtosis'] = round(returns.kurtosis(), 4)
            basic_stats['var_5_percent'] = round(returns.quantile(0.05), 4)  # 5% VaR
            basic_stats['positive_days'] = int((returns > 0).sum())
            basic_stats['negative_days'] = int((returns < 0).sum())
            basic_stats['positive_percentage'] = round((returns > 0).sum() / len(returns) * 100, 2)
            
            summary[asset_name] = basic_stats
    
    # Save enhanced summary
    with open('returns_summary_with_currencies.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print("✓ Saved enhanced summary: returns_summary_with_currencies.json")
    
    # Create correlation analysis
    print("\nCalculating correlations...")
    return_columns = [col for col in combined_df.columns if col.endswith('_Return')]
    correlation_data = combined_df[return_columns].corr()
    
    # Rename for better readability
    correlation_data.columns = [col.replace('_Return', '') for col in correlation_data.columns]
    correlation_data.index = [idx.replace('_Return', '') for idx in correlation_data.index]
    
    correlation_data.to_csv('correlation_matrix_with_currencies.csv')
    print("✓ Saved correlation matrix: correlation_matrix_with_currencies.csv")
    
    # Currency-specific analysis
    print("\nPerforming currency-specific analysis...")
    currency_analysis = {}
    
    for currency in currency_assets:
        if f'{currency}_Return' in combined_df.columns:
            currency_returns = combined_df[f'{currency}_Return'].dropna()
            combined_df['Date'] = pd.to_datetime(combined_df['Date'])
            currency_df = combined_df[['Date', f'{currency}_Return']].dropna()
            currency_df.set_index('Date', inplace=True)
            
            currency_analysis[currency] = {
                'description': get_currency_description(currency),
                'correlations_with_others': {},
                'monthly_stats': {},
                'quarterly_stats': {},
                'risk_metrics': {}
            }
            
            # Correlations with other assets
            for other_asset in assets.keys():
                if other_asset != currency and f'{other_asset}_Return' in combined_df.columns:
                    other_returns = combined_df[f'{other_asset}_Return'].dropna()
                    # Align the series for correlation calculation
                    aligned_currency = currency_returns.reindex(combined_df.index).dropna()
                    aligned_other = other_returns.reindex(combined_df.index).dropna()
                    
                    # Find common indices
                    common_idx = aligned_currency.index.intersection(aligned_other.index)
                    if len(common_idx) > 30:  # Require at least 30 overlapping observations
                        corr = aligned_currency.loc[common_idx].corr(aligned_other.loc[common_idx])
                        currency_analysis[currency]['correlations_with_others'][other_asset] = round(corr, 4)
            
            # Monthly analysis
            monthly_returns = currency_df[f'{currency}_Return'].resample('M').apply(
                lambda x: (1 + x/100).prod() - 1
            ) * 100
            
            currency_analysis[currency]['monthly_stats'] = {
                'avg_monthly_return': round(monthly_returns.mean(), 4),
                'monthly_volatility': round(monthly_returns.std(), 4),
                'best_month': round(monthly_returns.max(), 4),
                'worst_month': round(monthly_returns.min(), 4),
                'positive_months': int((monthly_returns > 0).sum()),
                'total_months': len(monthly_returns)
            }
            
            # Quarterly analysis
            quarterly_returns = currency_df[f'{currency}_Return'].resample('Q').apply(
                lambda x: (1 + x/100).prod() - 1
            ) * 100
            
            currency_analysis[currency]['quarterly_stats'] = {
                'avg_quarterly_return': round(quarterly_returns.mean(), 4),
                'quarterly_volatility': round(quarterly_returns.std(), 4),
                'best_quarter': round(quarterly_returns.max(), 4),
                'worst_quarter': round(quarterly_returns.min(), 4)
            }
            
            # Risk metrics
            currency_analysis[currency]['risk_metrics'] = {
                'value_at_risk_5pct': round(currency_returns.quantile(0.05), 4),
                'value_at_risk_1pct': round(currency_returns.quantile(0.01), 4),
                'max_drawdown_daily': round(currency_returns.min(), 4),
                'extreme_positive_days': int((currency_returns > currency_returns.quantile(0.95)).sum()),
                'extreme_negative_days': int((currency_returns < currency_returns.quantile(0.05)).sum())
            }
    
    # Save currency analysis
    with open('currency_specific_analysis.json', 'w') as f:
        json.dump(currency_analysis, f, indent=2)
    print("✓ Saved currency analysis: currency_specific_analysis.json")
    
    # Print summary
    print("\n" + "=" * 60)
    print("DATA COLLECTION SUMMARY")
    print("=" * 60)
    
    print(f"\nSuccessfully collected data for {len(all_returns)} assets:")
    
    # Group by asset type
    for asset_type in ['Traditional', 'Cryptocurrency', 'Currency']:
        type_assets = [asset for asset, stats in summary.items() if stats.get('asset_type') == asset_type]
        if type_assets:
            print(f"\n{asset_type} Assets ({len(type_assets)}):")
            for asset in type_assets:
                stats = summary[asset]
                print(f"  • {asset}: {stats['total_days']} days, "
                      f"Annualized Return: {stats['annualized_return']:.2f}%, "
                      f"Volatility: {stats['annualized_volatility']:.2f}%")
    
    # Currency insights
    if currency_analysis:
        print("\n" + "=" * 60)
        print("CURRENCY INSIGHTS")
        print("=" * 60)
        
        for currency, analysis in currency_analysis.items():
            print(f"\n{currency}:")
            print(f"  Description: {analysis['description']}")
            print(f"  Monthly Performance: {analysis['monthly_stats']['avg_monthly_return']:.2f}% avg")
            print(f"  Monthly Volatility: {analysis['monthly_stats']['monthly_volatility']:.2f}%")
            print(f"  5% VaR: {analysis['risk_metrics']['value_at_risk_5pct']:.2f}%")
            
            # Top correlations
            correlations = analysis['correlations_with_others']
            if correlations:
                sorted_corrs = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
                print("  Highest correlations:")
                for asset, corr in sorted_corrs:
                    print(f"    - {asset}: {corr:.3f}")

print("\n" + "=" * 60)
print("Data collection with currency analysis complete!")
print("Files generated:")
print("• Individual asset CSV files")
print("• Combined dataset with currencies")
print("• Enhanced summary statistics")
print("• Correlation matrix")
print("• Currency-specific analysis")
print("=" * 60)
