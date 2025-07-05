import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def create_visualizations():
    """Create key visualizations from the daily returns data"""
    
    print("Loading data...")
    # Load the combined data file
    df = pd.read_csv('all_assets_daily_returns_2020_2024.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    # Get return columns and asset names
    return_columns = [col for col in df.columns if col.endswith('_Return')]
    assets = [col.replace('_Return', '') for col in return_columns]
    
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # 1. Cumulative Returns Chart
    print("Creating cumulative returns chart...")
    plt.figure(figsize=(14, 8))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for i, asset in enumerate(assets):
        cumulative_returns = (1 + df[f'{asset}_Return']/100).cumprod() - 1
        plt.plot(df.index, cumulative_returns * 100, label=asset, color=colors[i], linewidth=2)
    
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Cumulative Return (%)', fontsize=12)
    plt.title('Cumulative Returns (2020-2024)', fontsize=16, pad=20)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('cumulative_returns_2020_2024.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: cumulative_returns_2020_2024.png")
    
    # 2. Correlation Heatmap
    print("Creating correlation heatmap...")
    correlation_matrix = df[return_columns].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, 
                annot=True, 
                fmt='.3f',
                cmap='RdBu_r', 
                center=0,
                square=True,
                linewidths=1,
                cbar_kws={"shrink": .8})
    plt.title('Daily Returns Correlation Matrix (2020-2024)', fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig('correlation_matrix_2020_2024.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: correlation_matrix_2020_2024.png")
    
    # 3. Risk-Return Scatter Plot
    print("Creating risk-return scatter plot...")
    plt.figure(figsize=(10, 8))
    
    for asset in assets:
        returns = df[f'{asset}_Return'].dropna()
        annual_return = returns.mean() * 252
        annual_vol = returns.std() * np.sqrt(252)
        
        plt.scatter(annual_vol, annual_return, s=200, alpha=0.7)
        plt.annotate(asset, (annual_vol, annual_return), 
                    xytext=(5, 5), textcoords='offset points', fontsize=12)
    
    plt.xlabel('Annualized Volatility (%)', fontsize=12)
    plt.ylabel('Annualized Return (%)', fontsize=12)
    plt.title('Risk-Return Profile (2020-2024)', fontsize=16, pad=20)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('risk_return_profile_2020_2024.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: risk_return_profile_2020_2024.png")
    
    # 4. Monthly Returns Heatmap (S&P 500 as example)
    print("Creating monthly returns heatmap for S&P 500...")
    monthly_returns = df['SP500_Return'].resample('M').apply(lambda x: ((1 + x/100).prod() - 1) * 100)
    
    # Pivot to create year-month matrix
    monthly_pivot = monthly_returns.to_frame('return')
    monthly_pivot['Year'] = monthly_pivot.index.year
    monthly_pivot['Month'] = monthly_pivot.index.month
    monthly_matrix = monthly_pivot.pivot(index='Year', columns='Month', values='return')
    
    plt.figure(figsize=(12, 6))
    sns.heatmap(monthly_matrix, 
                annot=True, 
                fmt='.1f',
                cmap='RdYlGn', 
                center=0,
                cbar_kws={'label': 'Return (%)'})
    plt.title('S&P 500 Monthly Returns Heatmap (%)', fontsize=16)
    plt.xlabel('Month')
    plt.ylabel('Year')
    plt.tight_layout()
    plt.savefig('sp500_monthly_returns_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: sp500_monthly_returns_heatmap.png")
    
    # Print summary statistics
    print("\n" + "="*60)
    print("SUMMARY STATISTICS (2020-2024)")
    print("="*60)
    
    for asset in assets:
        returns = df[f'{asset}_Return'].dropna()
        annual_return = returns.mean() * 252
        annual_vol = returns.std() * np.sqrt(252)
        sharpe = (returns.mean() / returns.std()) * np.sqrt(252)
        final_cumulative = ((1 + returns/100).cumprod() - 1).iloc[-1] * 100
        
        print(f"\n{asset}:")
        print(f"  Annualized Return: {annual_return:.2f}%")
        print(f"  Annualized Volatility: {annual_vol:.2f}%")
        print(f"  Sharpe Ratio: {sharpe:.3f}")
        print(f"  Total Cumulative Return: {final_cumulative:.2f}%")
        print(f"  Best Daily Return: {returns.max():.2f}%")
        print(f"  Worst Daily Return: {returns.min():.2f}%")
    
    print("\n" + "="*60)
    print("Visualization complete! Check the generated PNG files.")
    print("="*60)

if __name__ == "__main__":
    try:
        import numpy as np
        create_visualizations()
    except FileNotFoundError:
        print("Error: Data files not found!")
        print("Please run 'fetch_returns_data.py' first to download the data.")
    except ImportError as e:
        print(f"Error: Missing required library - {e}")
        print("Please install requirements: pip install -r requirements.txt")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
