import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

def create_visualizations():
    """Create key visualizations from the daily returns data including currency analysis using log returns for better visualization"""
    
    print("Loading data...")
    # Try to load the new currency-enhanced data file first, fallback to original
    try:
        df = pd.read_csv('daily_returns_with_currencies_2020_2025.csv')
        print("Loaded currency-enhanced dataset")
    except FileNotFoundError:
        try:
            df = pd.read_csv('all_assets_daily_returns_2020_2024.csv')
            print("Loaded original dataset (no currencies)")
        except FileNotFoundError:
            print("Error: No data files found!")
            print("Please run the data collection script first.")
            return
    
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    # Get return columns and asset names
    return_columns = [col for col in df.columns if col.endswith('_Daily_Return')]
    assets = [col.replace('_Daily_Return', '') for col in return_columns]
    
    # Separate currencies from other assets for analysis
    currency_assets = [asset for asset in assets if asset in ['JPY_USD', 'EUR_USD', 'USD_Index']]
    other_assets = [asset for asset in assets if asset not in currency_assets]
    
    print(f"Found assets: {assets}")
    print(f"Currency assets: {currency_assets}")
    print(f"Other assets: {other_assets}")
    
    # Convert to log returns for better visualization
    print("Converting to log returns...")
    for asset in assets:
        # Convert simple returns to log returns
        simple_returns = df[f'{asset}_Daily_Return'] / 100  # Convert percentage to decimal
        log_returns = np.log(1 + simple_returns) * 100  # Convert back to percentage for easier interpretation
        df[f'{asset}_LogReturn'] = log_returns
    
    log_return_columns = [f'{asset}_LogReturn' for asset in assets]
    
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # 1. Cumulative Returns Chart (from Log Returns) - All Assets
    print("Creating cumulative returns chart from log returns...")
    plt.figure(figsize=(16, 10))
    
    # Define colors for different asset types
    crypto_colors = ['#ff9500', '#627eea', '#23292f']  # Orange, Blue, Dark for BTC, ETH, XRP
    traditional_colors = ['#1f77b4', '#d62728']  # Blue, Red for SP500, Gold
    currency_colors = ['#2ca02c', '#9467bd', '#8c564b']  # Green, Purple, Brown for currencies
    
    color_map = {}
    crypto_assets = [a for a in assets if a in ['BTC', 'ETH', 'XRP']]
    traditional_assets = [a for a in assets if a in ['SP500', 'Gold']]
    
    # Assign colors
    for i, asset in enumerate(crypto_assets):
        color_map[asset] = crypto_colors[i % len(crypto_colors)]
    for i, asset in enumerate(traditional_assets):
        color_map[asset] = traditional_colors[i % len(traditional_colors)]
    for i, asset in enumerate(currency_assets):
        color_map[asset] = currency_colors[i % len(currency_colors)]
    
    for asset in assets:
        log_returns = df[f'{asset}_LogReturn'] / 100  # Convert to decimal
        cumulative_log_returns = log_returns.cumsum()
        cumulative_simple_returns = (np.exp(cumulative_log_returns) - 1) * 100  # Convert to percentage
        
        color = color_map.get(asset, '#000000')
        linestyle = '--' if asset in currency_assets else '-'
        linewidth = 2.5 if asset in currency_assets else 2
        
        plt.plot(df.index, cumulative_simple_returns, 
                label=asset, color=color, linewidth=linewidth, linestyle=linestyle)
    
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Cumulative Return (%)', fontsize=12)
    plt.title('Cumulative Returns from Log Returns - All Assets Including Currencies (2020-2025)', fontsize=16, pad=20)
    plt.legend(loc='best', fontsize=10, ncol=2)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('cumulative_returns_with_currencies_2020_2025.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: cumulative_returns_with_currencies_2020_2025.png")
    
    # 2. Currency-Specific Analysis
    if currency_assets:
        print("Creating currency-specific visualizations...")
        
        # Currency correlation with other assets
        fig, axes = plt.subplots(1, len(currency_assets), figsize=(5*len(currency_assets), 6))
        if len(currency_assets) == 1:
            axes = [axes]
        
        for i, currency in enumerate(currency_assets):
            currency_returns = df[f'{currency}_LogReturn'].dropna()
            correlations = []
            asset_names = []
            
            for other_asset in other_assets:
                if f'{other_asset}_LogReturn' in df.columns:
                    other_returns = df[f'{other_asset}_LogReturn'].dropna()
                    # Align the data
                    aligned_data = pd.concat([currency_returns, other_returns], axis=1, join='inner')
                    if len(aligned_data) > 0:
                        corr = aligned_data.iloc[:, 0].corr(aligned_data.iloc[:, 1])
                        correlations.append(corr)
                        asset_names.append(other_asset)
            
            # Create bar plot
            bars = axes[i].bar(asset_names, correlations, 
                              color=['green' if x > 0 else 'red' for x in correlations],
                              alpha=0.7)
            axes[i].set_title(f'{currency} Correlation with Other Assets', fontsize=12)
            axes[i].set_ylabel('Correlation Coefficient')
            axes[i].set_ylim(-1, 1)
            axes[i].axhline(y=0, color='black', linestyle='-', alpha=0.3)
            axes[i].tick_params(axis='x', rotation=45)
            
            # Add value labels on bars
            for bar, corr in zip(bars, correlations):
                height = bar.get_height()
                axes[i].text(bar.get_x() + bar.get_width()/2., height,
                           f'{corr:.2f}', ha='center', va='bottom' if height > 0 else 'top')
        
        plt.tight_layout()
        plt.savefig('currency_correlations_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Saved: currency_correlations_analysis.png")
        
        # Currency volatility comparison
        plt.figure(figsize=(12, 8))
        
        volatilities = []
        volatility_labels = []
        colors = []
        
        for asset in assets:
            returns = df[f'{asset}_LogReturn'].dropna()
            if len(returns) > 0:
                vol = returns.std() * np.sqrt(252)  # Annualized volatility
                volatilities.append(vol)
                volatility_labels.append(asset)
                
                if asset in currency_assets:
                    colors.append('blue')
                elif asset in crypto_assets:
                    colors.append('orange')
                else:
                    colors.append('gray')
        
        # Sort by volatility
        sorted_data = sorted(zip(volatilities, volatility_labels, colors), reverse=True)
        sorted_volatilities, sorted_labels, sorted_colors = zip(*sorted_data)
        
        bars = plt.bar(sorted_labels, sorted_volatilities, color=sorted_colors, alpha=0.7)
        plt.title('Annualized Volatility Comparison - All Assets Including Currencies', fontsize=16)
        plt.ylabel('Annualized Volatility (%)')
        plt.xticks(rotation=45)
        
        # Add value labels
        for bar, vol in zip(bars, sorted_volatilities):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{vol:.1f}%', ha='center', va='bottom')
        
        # Create legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='blue', alpha=0.7, label='Currencies'),
            Patch(facecolor='orange', alpha=0.7, label='Cryptocurrencies'),
            Patch(facecolor='gray', alpha=0.7, label='Traditional Assets')
        ]
        plt.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        plt.savefig('volatility_comparison_with_currencies.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Saved: volatility_comparison_with_currencies.png")
    
    # 3. Enhanced Correlation Heatmap (Log Returns)
    print("Creating enhanced correlation heatmap for log returns...")
    correlation_matrix = df[log_return_columns].corr()
    
    # Rename columns for better display
    correlation_matrix.columns = assets
    correlation_matrix.index = assets
    
    plt.figure(figsize=(12, 10))
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))  # Mask upper triangle
    
    sns.heatmap(correlation_matrix, 
                mask=mask,
                annot=True, 
                fmt='.3f',
                cmap='RdBu_r', 
                center=0,
                square=True,
                linewidths=1,
                cbar_kws={"shrink": .8})
    plt.title('Daily Log Returns Correlation Matrix - All Assets Including Currencies', fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig('correlation_matrix_with_currencies_2020_2025.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: correlation_matrix_with_currencies_2020_2025.png")
    
    # 4. Risk-Return Scatter Plot (Log Returns)
    print("Creating risk-return scatter plot using log returns...")
    plt.figure(figsize=(12, 10))
    
    for asset in assets:
        log_returns = df[f'{asset}_LogReturn'].dropna()
        if len(log_returns) > 0:
            annual_return = log_returns.mean() * 252
            annual_vol = log_returns.std() * np.sqrt(252)
            
            # Choose marker and color based on asset type
            if asset in currency_assets:
                marker = 's'  # Square for currencies
                color = 'blue'
                size = 200
            elif asset in crypto_assets:
                marker = '^'  # Triangle for crypto
                color = 'orange'
                size = 200
            else:
                marker = 'o'  # Circle for traditional assets
                color = 'gray'
                size = 200
            
            plt.scatter(annual_vol, annual_return, s=size, alpha=0.7, 
                       marker=marker, color=color, edgecolors='black', linewidth=1)
            plt.annotate(asset, (annual_vol, annual_return), 
                        xytext=(5, 5), textcoords='offset points', fontsize=12, fontweight='bold')
    
    plt.xlabel('Annualized Volatility (%) - Log Returns', fontsize=12)
    plt.ylabel('Annualized Return (%) - Log Returns', fontsize=12)
    plt.title('Risk-Return Profile using Log Returns - All Assets Including Currencies', fontsize=16, pad=20)
    plt.grid(True, alpha=0.3)
    
    # Create legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='s', color='w', markerfacecolor='blue', markersize=12, label='Currencies'),
        Line2D([0], [0], marker='^', color='w', markerfacecolor='orange', markersize=12, label='Cryptocurrencies'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=12, label='Traditional Assets')
    ]
    plt.legend(handles=legend_elements, loc='best')
    
    plt.tight_layout()
    plt.savefig('risk_return_profile_with_currencies_2020_2025.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: risk_return_profile_with_currencies_2020_2025.png")
    
    # 5. Log Returns Distribution Comparison (Enhanced)
    print("Creating enhanced log returns distribution comparison...")
    n_assets = len(assets)
    n_cols = 3
    n_rows = (n_assets + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    axes = axes.flatten() if n_rows > 1 else [axes] if n_cols == 1 else axes
    
    for i, asset in enumerate(assets):
        log_returns = df[f'{asset}_LogReturn'].dropna()
        
        if asset in currency_assets:
            color = 'lightblue'
            edge_color = 'blue'
        elif asset in crypto_assets:
            color = 'lightsalmon'
            edge_color = 'orange'
        else:
            color = 'lightgray'
            edge_color = 'black'
        
        axes[i].hist(log_returns, bins=50, density=True, alpha=0.7, 
                    color=color, edgecolor=edge_color)
        axes[i].set_title(f'{asset} Log Returns Distribution', fontsize=12, fontweight='bold')
        axes[i].set_xlabel('Daily Log Return (%)')
        axes[i].set_ylabel('Density')
        
        # Add normal distribution overlay
        from scipy import stats
        x = np.linspace(log_returns.min(), log_returns.max(), 100)
        axes[i].plot(x, stats.norm.pdf(x, log_returns.mean(), log_returns.std()), 
                    'r-', linewidth=2, label='Normal')
        axes[i].legend()
    
    # Remove empty subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
    
    plt.tight_layout()
    plt.savefig('log_returns_distributions_with_currencies_2020_2025.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: log_returns_distributions_with_currencies_2020_2025.png")
    
    # 6. Currency-Specific Time Series Analysis
    if currency_assets:
        print("Creating currency time series analysis...")
        fig, axes = plt.subplots(len(currency_assets), 1, figsize=(14, 6*len(currency_assets)))
        if len(currency_assets) == 1:
            axes = [axes]
        
        for i, currency in enumerate(currency_assets):
            # Plot cumulative returns
            log_returns = df[f'{currency}_LogReturn'] / 100
            cumulative_returns = (np.exp(log_returns.cumsum()) - 1) * 100
            
            axes[i].plot(df.index, cumulative_returns, linewidth=2, color='blue', alpha=0.8)
            axes[i].set_title(f'{currency} Cumulative Returns Over Time', fontsize=14, fontweight='bold')
            axes[i].set_ylabel('Cumulative Return (%)')
            axes[i].grid(True, alpha=0.3)
            
            # Add major economic events as vertical lines (sample dates)
            if currency == 'USD_Index':
                # Sample events - you can add more specific dates
                axes[i].axvline(pd.to_datetime('2020-03-15'), color='red', linestyle='--', alpha=0.7, label='COVID-19 Market Crash')
                axes[i].axvline(pd.to_datetime('2022-03-01'), color='orange', linestyle='--', alpha=0.7, label='Ukraine Conflict')
            
            axes[i].legend()
        
        plt.tight_layout()
        plt.savefig('currency_time_series_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Saved: currency_time_series_analysis.png")
    
    # 7. Monthly Returns Heatmap for Currencies
    if currency_assets:
        print("Creating monthly returns heatmaps for currencies...")
        
        for currency in currency_assets:
            monthly_log_returns = df[f'{currency}_LogReturn'].resample('M').sum()
            
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
            plt.title(f'{currency} Monthly Log Returns Heatmap (%)', fontsize=16)
            plt.xlabel('Month')
            plt.ylabel('Year')
            plt.tight_layout()
            plt.savefig(f'{currency.lower()}_monthly_returns_heatmap.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"✓ Saved: {currency.lower()}_monthly_returns_heatmap.png")
    
    # Print enhanced summary statistics
    print("\n" + "="*80)
    print("ENHANCED SUMMARY STATISTICS (LOG RETURNS WITH CURRENCIES)")
    print("="*80)
    
    # Group assets by type for better organization
    asset_groups = {
        'Traditional Assets': [a for a in assets if a in ['SP500', 'Gold']],
        'Cryptocurrencies': [a for a in assets if a in ['BTC', 'ETH', 'XRP']],
        'Currencies': currency_assets
    }
    
    for group_name, group_assets in asset_groups.items():
        if group_assets:
            print(f"\n{group_name.upper()}:")
            print("-" * 40)
            
            for asset in group_assets:
                if f'{asset}_LogReturn' in df.columns:
                    log_returns = df[f'{asset}_LogReturn'].dropna()
                    annual_return = log_returns.mean() * 252
                    annual_vol = log_returns.std() * np.sqrt(252)
                    sharpe = (log_returns.mean() / log_returns.std()) * np.sqrt(252)
                    
                    # Calculate cumulative return from log returns
                    log_returns_decimal = log_returns / 100
                    final_cumulative = (np.exp(log_returns_decimal.cumsum().iloc[-1]) - 1) * 100
                    
                    print(f"\n{asset}:")
                    print(f"  Annualized Return: {annual_return:.2f}%")
                    print(f"  Annualized Volatility: {annual_vol:.2f}%")
                    print(f"  Sharpe Ratio: {sharpe:.3f}")
                    print(f"  Total Cumulative Return: {final_cumulative:.2f}%")
                    print(f"  Best Daily Log Return: {log_returns.max():.2f}%")
                    print(f"  Worst Daily Log Return: {log_returns.min():.2f}%")
                    print(f"  Skewness: {log_returns.skew():.3f}")
                    print(f"  Kurtosis: {log_returns.kurtosis():.3f}")
    
    # Currency-specific insights
    if currency_assets:
        print(f"\n" + "="*80)
        print("CURRENCY-SPECIFIC INSIGHTS")
        print("="*80)
        
        for currency in currency_assets:
            print(f"\n{currency} Analysis:")
            log_returns = df[f'{currency}_LogReturn'].dropna()
            
            # Calculate rolling volatility
            rolling_vol = log_returns.rolling(window=30).std() * np.sqrt(252)
            
            print(f"  Average 30-day rolling volatility: {rolling_vol.mean():.2f}%")
            print(f"  Max 30-day rolling volatility: {rolling_vol.max():.2f}%")
            print(f"  Min 30-day rolling volatility: {rolling_vol.min():.2f}%")
            
            # VaR calculation (5% VaR)
            var_5 = np.percentile(log_returns, 5)
            print(f"  Value at Risk (5%): {var_5:.2f}%")
            
            # Count of extreme moves
            extreme_up = (log_returns > log_returns.quantile(0.95)).sum()
            extreme_down = (log_returns < log_returns.quantile(0.05)).sum()
            print(f"  Extreme positive days (>95th percentile): {extreme_up}")
            print(f"  Extreme negative days (<5th percentile): {extreme_down}")
    
    print("\n" + "="*80)
    print("Currency Analysis Visualization Complete!")
    print("Key Features Added:")
    print("• Currency correlation analysis with other assets")
    print("• Enhanced volatility comparison across asset classes")
    print("• Currency-specific time series analysis")
    print("• Monthly returns heatmaps for each currency")
    print("• Risk metrics including VaR and extreme move analysis")
    print("• Asset classification and grouped statistical analysis")
    print("="*80)

if __name__ == "__main__":
    try:
        from scipy import stats
        create_visualizations()
    except FileNotFoundError:
        print("Error: Data files not found!")
        print("Please run the updated 'collect_daily_returns.py' script first to download currency data.")
    except ImportError as e:
        print(f"Error: Missing required library - {e}")
        print("Please install requirements: pip install -r requirements.txt scipy")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
