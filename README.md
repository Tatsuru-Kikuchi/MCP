# Daily Returns Data (2020-2024)

This repository contains daily returns data for the following assets from January 1, 2020 to December 31, 2024:

- **S&P 500** (^GSPC)
- **Gold** (GC=F)
- **Bitcoin** (BTC-USD)
- **Ethereum** (ETH-USD)
- **XRP** (XRP-USD)

## Files

### Individual Asset Files
- `SP500_daily_returns_2020_2024.csv` - S&P 500 daily returns
- `Gold_daily_returns_2020_2024.csv` - Gold futures daily returns
- `BTC_daily_returns_2020_2024.csv` - Bitcoin daily returns
- `ETH_daily_returns_2020_2024.csv` - Ethereum daily returns
- `XRP_daily_returns_2020_2024.csv` - XRP daily returns

### Combined Data
- `all_assets_daily_returns_2020_2024.csv` - All assets in one file

### Summary Statistics
- `returns_summary.json` - Summary statistics for all assets

## Data Format

Each CSV file contains:
- **Date**: Trading date (YYYY-MM-DD)
- **Close**: Closing price for that day
- **Daily_Return**: Percentage return from previous day (in %)

## Data Source

Data was fetched from Yahoo Finance using the `yfinance` Python library.

## Usage

To fetch updated data, run:
```bash
python fetch_returns_data.py
```

## Requirements

- Python 3.7+
- yfinance
- pandas

## Installation

```bash
pip install yfinance pandas
```