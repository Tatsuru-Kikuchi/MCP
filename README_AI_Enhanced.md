# 🚀 AI-Enhanced Stock Analysis Dashboard

## Overview

This is a sophisticated, AI-powered stock analysis system that provides real-time predictions, advanced visualizations, and comprehensive market insights. The system compares AI-driven predictions with traditional technical analysis to give you a complete view of market opportunities.

## 🌆 Key Features

### 🤖 AI-Powered Predictions
- **Machine Learning Models**: Random Forest, Gradient Boosting, and Linear Regression
- **Real-time Analysis**: Continuous model training and prediction updates
- **Confidence Scoring**: Each prediction comes with a confidence level
- **Feature Engineering**: 25+ technical indicators and time-series features

### 📊 Advanced Dashboard
- **Interactive Charts**: Real-time price trends, volatility analysis, and risk-return profiles
- **Market Sentiment**: AI-driven sentiment analysis with visual indicators
- **Opportunity Detection**: Automatically identifies high-confidence trading opportunities
- **Risk Alerts**: Real-time volatility and correlation warnings
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices

### 🔄 Real-Time Data Processing
- **Live Market Data**: Direct integration with Yahoo Finance API
- **Auto-Refresh**: Data updates every 5 minutes
- **Historical Analysis**: Comprehensive backtesting capabilities
- **Multi-Asset Support**: Stocks, cryptocurrencies, forex, and commodities

## 📊 Supported Assets

### Traditional Assets
- **S&P 500** (^GSPC) - US stock market benchmark
- **Gold** (GC=F) - Precious metals commodity

### Cryptocurrencies
- **Bitcoin** (BTC-USD) - Leading cryptocurrency
- **Ethereum** (ETH-USD) - Second-largest cryptocurrency
- **XRP** (XRP-USD) - Digital payment cryptocurrency

### Currency Pairs
- **JPY/USD** (JPY=X) - Japanese Yen to US Dollar
- **EUR/USD** (EURUSD=X) - Euro to US Dollar
- **USD Index** (DX-Y.NYB) - US Dollar strength index

## 🚀 Quick Start

### Method 1: One-Click Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/Tatsuru-Kikuchi/MCP-stock.git
cd MCP-stock

# Switch to the enhanced branch
git checkout ai-enhanced-dashboard

# Install dependencies
pip install -r requirements_enhanced.txt

# Start the entire system
python start_system.py
```

The system will automatically:
1. ✅ Check all requirements
2. 📁 Set up necessary directories
3. 🔄 Fetch initial data and train models
4. 🚀 Start the API server
5. 🌐 Open the dashboard in your browser

### Method 2: Manual Setup

```bash
# 1. Install dependencies
pip install -r requirements_enhanced.txt

# 2. Fetch data and train models
python enhanced_fetch_data.py

# 3. Start the API server
python api_server.py

# 4. Open your browser to http://localhost:8000
```

## 📊 Dashboard Features

### 1. Market Sentiment Analysis
- **Real-time sentiment**: Bullish, Bearish, or Neutral
- **Confidence indicators**: Visual confidence bars
- **Historical sentiment trends**

### 2. AI vs Traditional Predictions
- **Side-by-side comparison**: AI predictions vs traditional technical analysis
- **Difference analysis**: Highlights where AI and traditional methods diverge
- **Confidence scoring**: Each prediction includes confidence levels

### 3. Investment Opportunities
- **Top 5 opportunities**: Ranked by confidence and potential return
- **Risk assessment**: Automatic risk level categorization
- **Real-time updates**: Opportunities update as market conditions change

### 4. Risk Management
- **Volatility alerts**: Automatic warnings for high volatility periods
- **Correlation analysis**: Interactive correlation matrix
- **Risk-return visualization**: Scatter plots showing risk vs return profiles

### 5. Interactive Charts
- **Price trends**: Multi-asset price comparison
- **Volatility analysis**: Rolling volatility calculations
- **Returns distribution**: Histogram analysis of returns
- **Technical indicators**: Moving averages, RSI, MACD, and more

## 📡 API Endpoints

The system provides a comprehensive RESTful API:

### Core Endpoints
- `GET /api/predictions` - AI vs Traditional predictions
- `GET /api/market-sentiment` - Current market sentiment
- `GET /api/prices` - Real-time asset prices
- `GET /api/opportunities` - Investment opportunities
- `GET /api/alerts` - Risk alerts and warnings
- `GET /api/correlations` - Asset correlation matrix
- `GET /api/historical-data/{asset}` - Historical data for specific asset
- `POST /api/refresh` - Trigger manual data refresh

### System Endpoints
- `GET /api/health` - System health check
- `GET /docs` - Interactive API documentation

## 🤖 AI Models & Features

### Technical Indicators
- **Moving Averages**: SMA (5, 10, 20, 50), EMA (12, 26)
- **Momentum**: MACD, RSI, Price Momentum
- **Volatility**: Bollinger Bands, ATR, Historical Volatility
- **Volume**: Volume ratios and trends
- **Time Features**: Cyclical encoding for seasonality

### Model Architecture
- **Random Forest**: Primary prediction model
- **Gradient Boosting**: Secondary validation model
- **Linear Regression**: Baseline comparison
- **Feature Engineering**: 30+ engineered features
- **Cross-validation**: Time-series aware validation

### Performance Metrics
- **R² Score**: Model accuracy measurement
- **RMSE**: Root Mean Square Error
- **Confidence Intervals**: Prediction uncertainty
- **Backtesting**: Historical performance validation

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Configure custom settings
export REFRESH_INTERVAL=300  # Data refresh interval in seconds
export MAX_HISTORY_DAYS=365  # Maximum historical data to fetch
export MODEL_RETRAIN_HOURS=24  # Model retraining frequency
```

### Custom Asset Configuration
Edit `real_time_analyzer.py` to add custom assets:

```python
self.assets = {
    'CUSTOM_ASSET': 'TICKER_SYMBOL',
    # Add more assets here
}
```

## 📁 Project Structure

```
MCP-stock/
├── 📄 real_time_analyzer.py          # Core AI analysis engine
├── 📄 enhanced_fetch_data.py         # Enhanced data fetcher
├── 📄 api_server.py                  # FastAPI server
├── 📄 start_system.py               # System startup script
├── 📂 dashboard/                    # Dashboard files
│   ├── dashboard_html.html         # Main dashboard
│   ├── dashboard_styles.css        # Styling
│   └── dashboard_script.js         # Interactive functionality
├── 📂 enhanced_data/               # Enhanced datasets
├── 📂 models/                      # Trained AI models
├── 📂 analysis_results/            # Analysis outputs
└── 📄 requirements_enhanced.txt    # Dependencies
```

## 🔬 Advanced Usage

### Running Individual Components

```bash
# Run only the AI analyzer
python real_time_analyzer.py

# Fetch and enhance data
python enhanced_fetch_data.py

# Start API server only
python api_server.py
```

### Custom Analysis

```python
from real_time_analyzer import RealTimeStockAnalyzer

# Initialize analyzer
analyzer = RealTimeStockAnalyzer()

# Fetch real-time data
data = analyzer.fetch_real_time_data()

# Train models
analyzer.train_ai_models(data)

# Generate predictions
ai_predictions = analyzer.predict_future_returns(data)
traditional_predictions = analyzer.traditional_analysis(data)

# Compare results
comparison = analyzer.compare_predictions(ai_predictions, traditional_predictions)
```

## 🛠️ Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill process using port 8000
   sudo lsof -t -i tcp:8000 | xargs kill -9
   ```

2. **Missing Dependencies**
   ```bash
   # Install all requirements
   pip install -r requirements_enhanced.txt
   ```

3. **Data Fetch Errors**
   - Check internet connection
   - Verify Yahoo Finance API availability
   - Try running with fewer assets initially

4. **Model Training Issues**
   - Ensure sufficient historical data (>100 days)
   - Check for data quality issues
   - Verify scikit-learn version compatibility

### Performance Optimization

- **Reduce refresh interval** for faster updates
- **Limit historical data** to improve processing speed
- **Use SSD storage** for better I/O performance
- **Increase system memory** for larger datasets

## 📈 Performance Metrics

### Typical Model Performance
- **R² Score**: 0.15-0.35 (varies by asset)
- **RMSE**: 1.5-3.0% (daily returns)
- **Prediction Accuracy**: 55-65% directional accuracy
- **Update Frequency**: Every 5 minutes

### System Requirements
- **RAM**: Minimum 4GB, Recommended 8GB+
- **CPU**: Multi-core processor recommended
- **Storage**: 1GB+ free space
- **Network**: Stable internet connection

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/MCP-stock.git
cd MCP-stock

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements_enhanced.txt

# Run tests
python -m pytest tests/
```

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**Important**: This system is for educational and research purposes only. 

- 🚫 **Not Financial Advice**: Do not use this system as the sole basis for investment decisions
- 📊 **Past Performance**: Historical results do not guarantee future performance
- 🔍 **Do Your Research**: Always conduct thorough research before making investments
- 💼 **Consult Professionals**: Seek advice from qualified financial advisors
- 📉 **Risk Warning**: All investments carry risk of loss

## 🙏 Acknowledgments

- **Yahoo Finance** for providing market data
- **scikit-learn** for machine learning capabilities
- **FastAPI** for the web framework
- **Chart.js** for interactive visualizations
- **The Open Source Community** for inspiration and tools

---

**🌟 Star this repository if you find it useful!**

**📧 Questions?** Open an issue or contact the maintainers.

**🔗 Links:**
- [GitHub Repository](https://github.com/Tatsuru-Kikuchi/MCP-stock)
- [Live Demo](https://tatsuru-kikuchi.github.io/MCP/)
- [API Documentation](http://localhost:8000/docs)

---

*Built with ❤️ by the MCP-Stock team*