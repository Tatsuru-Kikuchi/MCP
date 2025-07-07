# Changelog

All notable changes to the financial-mcp project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial PyPI package structure
- Complete test suite with pytest
- GitHub Actions for CI/CD
- Command-line interface tools
- Comprehensive documentation

## [1.0.0] - 2025-07-07

### Added
- Initial release of financial-mcp package
- Financial data fetching from Yahoo Finance
- Support for multiple asset classes:
  - Traditional assets (S&P 500, Gold)
  - Cryptocurrencies (Bitcoin, Ethereum, XRP)
  - Currency pairs (JPY/USD, EUR/USD, USD Index)
- Comprehensive financial analysis:
  - Daily returns calculation
  - Volatility analysis
  - Correlation matrices
  - Risk metrics (VaR, CVaR, Maximum Drawdown)
  - Sharpe ratio calculation
- Data visualization capabilities:
  - Cumulative returns charts
  - Correlation heatmaps
  - Risk-return scatter plots
  - Volatility trend analysis
  - Return distribution plots
- Interactive web dashboard
- Command-line tools:
  - `financial-mcp-fetch`: Data fetching
  - `financial-mcp-analyze`: Data analysis
  - `financial-mcp-visualize`: Chart generation
- Python API for programmatic access
- Comprehensive test suite
- Documentation and examples

### Features
- **Multi-Asset Support**: Analyze stocks, cryptocurrencies, commodities, and currencies
- **Risk Management**: Calculate VaR, CVaR, and maximum drawdown
- **Correlation Analysis**: Understand relationships between different assets
- **Time Series Analysis**: Track performance over configurable time periods
- **Interactive Visualizations**: Generate publication-ready charts
- **Flexible Data Export**: Save results in CSV and JSON formats
- **Command Line Interface**: Easy-to-use CLI commands
- **Python API**: Full programmatic access to all functionality

### Technical Details
- Python 3.7+ compatibility
- Built on pandas, numpy, matplotlib, and seaborn
- Yahoo Finance integration via yfinance
- Comprehensive error handling
- Type hints for better code quality
- Extensive test coverage
- Cross-platform compatibility (Windows, macOS, Linux)

### Documentation
- Complete API documentation
- Usage examples and tutorials
- Interactive dashboard at https://tatsuru-kikuchi.github.io/MCP/
- GitHub repository with detailed README

### Data Sources
- Yahoo Finance for real-time and historical data
- Support for 8 major financial instruments
- Daily data from 2020-2024 (configurable)

### Output Formats
- CSV files for data export
- JSON files for analysis results
- PNG images for visualizations
- Interactive HTML dashboard

### Installation
```bash
pip install financial-mcp
```

### Quick Start
```python
import financial_mcp as fmcp

# Fetch data
all_data, daily_returns = fmcp.fetch_financial_data()

# Analyze
analysis = fmcp.analyze_returns(daily_returns_df)

# Visualize
fmcp.create_visualizations(daily_returns_df)
```

[Unreleased]: https://github.com/Tatsuru-Kikuchi/MCP/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Tatsuru-Kikuchi/MCP/releases/tag/v1.0.0
