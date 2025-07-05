import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

def create_visualizations():
    """Create key visualizations from the daily returns data using log returns for better visualization"""
    
    print("Loading data...")
    # Load the combined data file
    df = pd.read_csv('all_assets_daily_returns_2020_2024.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    # Get return columns and asset names
    return_columns = [col for col in df.columns if col.endswith('_Return')]
    assets = [col.replace('_Return', '') for col in return_columns]
    
    # Convert to log returns for better visualization
    print("Converting to log returns...")
    for asset in assets:
        # Convert simple returns to log returns
        simple_returns = df[f'{asset}_Return'] / 100  # Convert percentage to decimal
        log_returns = np.log(1 + simple_returns) * 100  # Convert back to percentage for easier interpretation
        df[f'{asset}_LogReturn'] = log_returns
    
    log_return_columns = [f'{asset}_LogReturn' for asset in assets]
    
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # 1. Cumulative Returns Chart (from Log Returns)
    print("Creating cumulative returns chart from log returns...")
    plt.figure(figsize=(14, 8))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for i, asset in enumerate(assets):
        log_returns = df[f'{asset}_LogReturn'] / 100  # Convert to decimal
        cumulative_log_returns = log_returns.cumsum()
        cumulative_simple_returns = (np.exp(cumulative_log_returns) - 1) * 100  # Convert to percentage
        plt.plot(df.index, cumulative_simple_returns, label=asset, color=colors[i], linewidth=2)
    
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Cumulative Return (%)', fontsize=12)
    plt.title('Cumulative Returns from Log Returns (2020-2024)', fontsize=16, pad=20)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('cumulative_returns_log_2020_2024.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: cumulative_returns_log_2020_2024.png")
    
    # 2. Correlation Heatmap (Log Returns)
    print("Creating correlation heatmap for log returns...")
    correlation_matrix = df[log_return_columns].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, 
                annot=True, 
                fmt='.3f',
                cmap='RdBu_r', 
                center=0,
                square=True,
                linewidths=1,
                cbar_kws={"shrink": .8})
    plt.title('Daily Log Returns Correlation Matrix (2020-2024)', fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig('correlation_matrix_log_returns_2020_2024.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: correlation_matrix_log_returns_2020_2024.png")
    
    # 3. Risk-Return Scatter Plot (Log Returns)
    print("Creating risk-return scatter plot using log returns...")
    plt.figure(figsize=(10, 8))
    
    for asset in assets:
        log_returns = df[f'{asset}_LogReturn'].dropna()
        annual_return = log_returns.mean() * 252
        annual_vol = log_returns.std() * np.sqrt(252)
        
        plt.scatter(annual_vol, annual_return, s=200, alpha=0.7)
        plt.annotate(asset, (annual_vol, annual_return), 
                    xytext=(5, 5), textcoords='offset points', fontsize=12)
    
    plt.xlabel('Annualized Volatility (%) - Log Returns', fontsize=12)
    plt.ylabel('Annualized Return (%) - Log Returns', fontsize=12)
    plt.title('Risk-Return Profile using Log Returns (2020-2024)', fontsize=16, pad=20)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('risk_return_profile_log_returns_2020_2024.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: risk_return_profile_log_returns_2020_2024.png")
    
    # 4. Log Returns Distribution Comparison
    print("Creating log returns distribution comparison...")
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, asset in enumerate(assets):
        log_returns = df[f'{asset}_LogReturn'].dropna()
        axes[i].hist(log_returns, bins=50, density=True, alpha=0.7, color='skyblue', edgecolor='black')
        axes[i].set_title(f'{asset} Log Returns Distribution', fontsize=12)
        axes[i].set_xlabel('Daily Log Return (%)')
        axes[i].set_ylabel('Density')
        
        # Add normal distribution overlay
        from scipy import stats
        x = np.linspace(log_returns.min(), log_returns.max(), 100)
        axes[i].plot(x, stats.norm.pdf(x, log_returns.mean(), log_returns.std()), 'r-', linewidth=2, label='Normal')
        axes[i].legend()
    
    # Remove empty subplot
    fig.delaxes(axes[-1])
    plt.tight_layout()
    plt.savefig('log_returns_distributions_2020_2024.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: log_returns_distributions_2020_2024.png")
    
    # 5. Monthly Returns Heatmap for S&P 500 (Log Returns)
    print("Creating monthly log returns heatmap for S&P 500...")
    monthly_log_returns = df['SP500_LogReturn'].resample('M').sum()
    
    # Pivot to create year-month matrix
    monthly_pivot = monthly_log_returns.to_frame('return')
    monthly_pivot['Year'] = monthly_pivot.index.year
    monthly_pivot['Month'] = monthly_pivot.index.month
    monthly_matrix = monthly_pivot.pivot(index='Year', columns='Month', values='return')
    
    plt.figure(figsize=(12, 6))
    sns.heatmap(monthly_matrix, 
                annot=True, 
                fmt='.1f',
                cmap='RdYlGn', 
                center=0,
                cbar_kws={'label': 'Log Return (%)'})
    plt.title('S&P 500 Monthly Log Returns Heatmap (%)', fontsize=16)
    plt.xlabel('Month')
    plt.ylabel('Year')
    plt.tight_layout()
    plt.savefig('sp500_monthly_log_returns_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: sp500_monthly_log_returns_heatmap.png")
    
    # 6. Simple vs Log Returns Comparison (Bitcoin as example)
    print("Creating simple vs log returns comparison...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Simple returns
    bitcoin_simple = df['Bitcoin_Return'].dropna()
    ax1.hist(bitcoin_simple, bins=50, density=True, alpha=0.7, color='orange', edgecolor='black')
    ax1.set_title('Bitcoin Simple Returns Distribution', fontsize=14)
    ax1.set_xlabel('Daily Return (%)')
    ax1.set_ylabel('Density')
    ax1.axvline(bitcoin_simple.mean(), color='red', linestyle='--', label=f'Mean: {bitcoin_simple.mean():.3f}%')
    ax1.legend()
    
    # Log returns
    bitcoin_log = df['Bitcoin_LogReturn'].dropna()
    ax2.hist(bitcoin_log, bins=50, density=True, alpha=0.7, color='blue', edgecolor='black')
    ax2.set_title('Bitcoin Log Returns Distribution', fontsize=14)
    ax2.set_xlabel('Daily Log Return (%)')
    ax2.set_ylabel('Density')
    ax2.axvline(bitcoin_log.mean(), color='red', linestyle='--', label=f'Mean: {bitcoin_log.mean():.3f}%')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('bitcoin_simple_vs_log_returns_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: bitcoin_simple_vs_log_returns_comparison.png")
    
    # Print summary statistics
    print("\n" + "="*60)
    print("SUMMARY STATISTICS (LOG RETURNS 2020-2024)")
    print("="*60)
    
    for asset in assets:
        log_returns = df[f'{asset}_LogReturn'].dropna()
        annual_return = log_returns.mean() * 252
        annual_vol = log_returns.std() * np.sqrt(252)
        sharpe = (log_returns.mean() / log_returns.std()) * np.sqrt(252)
        
        # Calculate cumulative return from log returns
        log_returns_decimal = log_returns / 100
        final_cumulative = (np.exp(log_returns_decimal.cumsum().iloc[-1]) - 1) * 100
        
        print(f"\n{asset} (Log Returns):")
        print(f"  Annualized Return: {annual_return:.2f}%")
        print(f"  Annualized Volatility: {annual_vol:.2f}%")
        print(f"  Sharpe Ratio: {sharpe:.3f}")
        print(f"  Total Cumulative Return: {final_cumulative:.2f}%")
        print(f"  Best Daily Log Return: {log_returns.max():.2f}%")
        print(f"  Worst Daily Log Return: {log_returns.min():.2f}%")
        print(f"  Skewness: {log_returns.skew():.3f}")
        print(f"  Kurtosis: {log_returns.kurtosis():.3f}")
    
    # Print comparison of simple vs log returns for Bitcoin
    print(f"\n" + "="*60)
    print("BITCOIN: SIMPLE vs LOG RETURNS COMPARISON")
    print("="*60)
    bitcoin_simple = df['Bitcoin_Return'].dropna()
    bitcoin_log = df['Bitcoin_LogReturn'].dropna()
    
    print(f"Simple Returns - Mean: {bitcoin_simple.mean():.4f}%, Std: {bitcoin_simple.std():.4f}%, Skew: {bitcoin_simple.skew():.4f}")
    print(f"Log Returns    - Mean: {bitcoin_log.mean():.4f}%, Std: {bitcoin_log.std():.4f}%, Skew: {bitcoin_log.skew():.4f}")
    print("\nLog returns show improved statistical properties:")
    print("✓ Reduced skewness (closer to normal distribution)")
    print("✓ Better for statistical modeling and risk analysis")
    print("✓ Time-additive property (can sum over periods)")
    print("✓ More appropriate for portfolio optimization")
    
    print("\n" + "="*60)
    print("Log Returns Visualization complete! Check the generated PNG files.")
    print("Benefits of log returns:")
    print("• Better statistical properties for analysis")
    print("• Improved visualization of high-volatility assets")
    print("• More suitable for risk modeling and portfolio optimization")
    print("="*60)

if __name__ == "__main__":
    try:
        from scipy import stats
        create_visualizations()
    except FileNotFoundError:
        print("Error: Data files not found!")
        print("Please run 'fetch_returns_data.py' first to download the data.")
    except ImportError as e:
        print(f"Error: Missing required library - {e}")
        print("Please install requirements: pip install -r requirements.txt scipy")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
