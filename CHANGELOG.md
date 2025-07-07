# Changelog

All notable changes to the Financial MCP project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-07

### Added
- Initial release of Financial MCP package
- **Core Features**:
  - Financial data fetching from Yahoo Finance
  - Support for multiple asset classes (stocks, crypto, currencies)
  - Comprehensive analysis tools and metrics
  - Beautiful visualizations and charts
  - Command-line interface tools
  - Interactive web dashboard

- **Supported Assets**:
  - Traditional: S&P 500, Gold
  - Cryptocurrencies: Bitcoin, Ethereum, XRP
  - Currencies: JPY/USD, EUR/USD, USD Index

- **Analysis Features**:
  - Daily returns calculation and analysis
  - Annualized returns and volatility metrics
  - Sharpe ratio and risk-adjusted returns
  - Correlation matrix analysis
  - Risk metrics (VaR, CVaR, Maximum Drawdown)
  - Statistical analysis (skewness, kurtosis)

- **Visualizations**:
  - Cumulative returns charts
  - Rolling volatility analysis
  - Risk-return scatter plots
  - Correlation heatmaps
  - Return distribution plots

- **Command Line Tools**:
  - `financial-mcp-fetch`: Data fetching utility
  - `financial-mcp-analyze`: Analysis tool
  - `financial-mcp-visualize`: Visualization generator

- **Python API**:
  - Simple and intuitive API design
  - Modular architecture with separate modules for:
    - Data fetching (`fetch_data`)
    - Analysis (`analyze`)
    - Visualization (`visualize`)
    - Utilities (`utils`)

- **Package Infrastructure**:
  - Comprehensive test suite with pytest
  - GitHub Actions CI/CD pipeline
  - Automated PyPI publishing
  - Type hints and documentation
  - Cross-platform compatibility (Windows, macOS, Linux)
  - Python 3.7+ support

- **Documentation**:
  - Detailed README with examples
  - API documentation
  - Installation and usage guides
  - Interactive dashboard at https://tatsuru-kikuchi.github.io/MCP/

### Technical Details
- Built with pandas, numpy, matplotlib, seaborn
- Uses yfinance for reliable financial data
- Modular design for easy extension
- Comprehensive error handling
- Memory-efficient data processing
- Configurable output directories
- Support for custom date ranges and asset selection

### Security
- No sensitive data stored in package
- Safe API usage with proper error handling
- Input validation for all user inputs

---

## Development Guidelines

### Version Numbering
- **Major** (X.y.z): Breaking changes, major new features
- **Minor** (x.Y.z): New features, backwards compatible
- **Patch** (x.y.Z): Bug fixes, small improvements

### Release Process
1. Update version numbers in relevant files
2. Update this CHANGELOG.md
3. Run tests and ensure all pass
4. Create git tag with version number
5. Push to GitHub to trigger automated publishing

### Contribution Guidelines
- Follow semantic versioning
- Add tests for new features
- Update documentation
- Follow code style guidelines (Black formatting)
- Add changelog entries for notable changes
