# Daily Returns Data: S&P 500, Gold, BTC, ETH, and XRP

This repository contains daily returns data for major financial assets from January 1, 2021 to December 31, 2025.

## Assets Included

- **S&P 500 Index** (^GSPC): U.S. stock market benchmark
- **Gold** (GC=F): Gold futures contracts
- **Bitcoin** (BTC-USD): Leading cryptocurrency
- **Ethereum** (ETH-USD): Second-largest cryptocurrency
- **XRP** (XRP-USD): Digital payment token

## Data Description

### Files
- `daily_returns_fetcher.py`: Python script to fetch daily returns data
- `daily_returns_2021_2025.csv`: CSV file containing daily returns data
- `requirements.txt`: Python dependencies

### Data Format
The CSV file contains:
- **Date**: Trading date (YYYY-MM-DD)
- **SP500**: Daily returns for S&P 500 Index
- **Gold**: Daily returns for Gold futures
- **BTC**: Daily returns for Bitcoin
- **ETH**: Daily returns for Ethereum  
- **XRP**: Daily returns for XRP

Daily returns are calculated as: (Close_t - Close_{t-1}) / Close_{t-1}

## Usage

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running the Script
```bash
python daily_returns_fetcher.py
```

### Loading the Data
```python
import pandas as pd

# Load the daily returns data
df = pd.read_csv('daily_returns_2021_2025.csv', index_col='Date', parse_dates=True)

# Display basic statistics
print(df.describe())

# Plot the cumulative returns
import matplotlib.pyplot as plt
(1 + df).cumprod().plot(figsize=(12, 8))
plt.title('Cumulative Returns (2021-2025)')
plt.legend()
plt.show()
```

## Data Sources

Data is fetched from Yahoo Finance using the yfinance library:
- **Reliable**: Yahoo Finance provides comprehensive financial data
- **Free**: No API key required
- **Historical**: Data available from 2021 onwards
- **Real-time**: Data updated daily

## Notes

- Data includes weekends and holidays (market closed days are excluded)
- Returns are calculated using adjusted closing prices
- Missing data points are handled by forward-filling or interpolation
- Cryptocurrency data is available 24/7, while traditional assets follow market hours

## Disclaimer

This data is for educational and research purposes only. Past performance does not guarantee future results. Please consult with a financial advisor before making investment decisions.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
