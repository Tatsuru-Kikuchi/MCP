# 🚀 AI-Enhanced Stock Analysis Dashboard

## 🌟 **NEW: AI-Powered Real-Time Analysis System**

This repository now features a **cutting-edge AI-powered stock analysis system** that provides real-time predictions, sophisticated visualizations, and comprehensive market insights. The system compares AI-driven predictions with traditional technical analysis to give you a complete view of market opportunities.

---

## 🎯 **Key Features**

### 🤖 **AI-Powered Predictions**
- **Machine Learning Models**: Random Forest, Gradient Boosting, and Linear Regression
- **Real-time Analysis**: Continuous model training and prediction updates
- **AI vs Traditional Comparison**: Side-by-side analysis of AI predictions vs technical analysis
- **Confidence Scoring**: Each prediction includes confidence levels
- **30+ Technical Indicators**: RSI, MACD, Bollinger Bands, Moving Averages, etc.

### 🎨 **Sophisticated Dashboard**
- **Modern UI/UX**: Glassmorphism design with smooth animations
- **Interactive Charts**: Real-time price trends, volatility analysis, risk-return profiles
- **Market Sentiment**: AI-driven sentiment analysis with visual indicators
- **Opportunity Detection**: Automatically identifies high-confidence trading opportunities
- **Risk Management**: Real-time volatility alerts and correlation analysis
- **Mobile Responsive**: Works seamlessly on all devices

### 🔄 **Real-Time Data Processing**
- **Live Market Data**: Direct integration with Yahoo Finance API
- **Auto-Refresh**: Data updates every 5 minutes
- **Background Processing**: Asynchronous data fetching and model training
- **Performance Optimization**: Efficient caching and data management

---

## 📊 **Supported Assets**

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

---

## 🚀 **Quick Start**

### **Method 1: One-Click Setup (Recommended)**

```bash
# Clone the repository
git clone https://github.com/Tatsuru-Kikuchi/MCP-stock.git
cd MCP-stock

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

### **Method 2: Docker Deployment**

```bash
# Clone the repository
git clone https://github.com/Tatsuru-Kikuchi/MCP-stock.git
cd MCP-stock

# Start with Docker Compose
docker-compose up -d

# Access dashboard at http://localhost:8000
```

### **Method 3: Manual Setup**

```bash
# 1. Install dependencies
pip install -r requirements_enhanced.txt

# 2. Fetch data and train models
python enhanced_fetch_data.py

# 3. Start the API server
python api_server.py

# 4. Open your browser to http://localhost:8000
```

---

## 🎮 **Dashboard Features**

### 1. **Market Sentiment Analysis**
- Real-time sentiment: Bullish, Bearish, or Neutral
- Confidence indicators with visual bars
- Historical sentiment trends

### 2. **AI vs Traditional Predictions**
- Side-by-side comparison of AI predictions vs traditional technical analysis
- Difference analysis highlighting where methods diverge
- Confidence scoring for each prediction

### 3. **Investment Opportunities**
- Top 5 opportunities ranked by confidence and potential return
- Automatic risk level categorization
- Real-time updates as market conditions change

### 4. **Risk Management**
- Volatility alerts for high volatility periods
- Interactive correlation matrix
- Risk-return visualization with scatter plots

### 5. **Interactive Charts**
- Multi-asset price comparison
- Rolling volatility calculations
- Returns distribution analysis
- Technical indicators overlay

---

## 🎯 **What Makes This Special**

### **🆚 AI vs Traditional Analysis**
This is the **first-of-its-kind system** that directly compares:
- **AI Predictions**: Machine learning models using 30+ features
- **Traditional Analysis**: Classic technical indicators and patterns
- **Real-time Comparison**: See how they differ in live market conditions

### **🧠 Advanced AI Models**
- **Random Forest**: Primary prediction model with feature importance
- **Gradient Boosting**: Secondary validation model
- **Linear Regression**: Baseline comparison
- **Confidence Scoring**: Each prediction includes reliability metrics

### **⚡ Real-Time Intelligence**
- **Live Market Data**: Direct Yahoo Finance integration
- **Auto-Refresh**: Updates every 5 minutes
- **Background Processing**: Non-blocking data fetching
- **Performance Optimized**: Efficient caching and processing

---

## 📡 **API Endpoints**

The system provides a comprehensive RESTful API:

### **Core Endpoints**
- `GET /api/predictions` - AI vs Traditional predictions
- `GET /api/market-sentiment` - Current market sentiment
- `GET /api/prices` - Real-time asset prices
- `GET /api/opportunities` - Investment opportunities
- `GET /api/alerts` - Risk alerts and warnings
- `GET /api/correlations` - Asset correlation matrix
- `GET /api/historical-data/{asset}` - Historical data for specific asset
- `POST /api/refresh` - Trigger manual data refresh

### **System Endpoints**
- `GET /api/health` - System health check
- `GET /docs` - Interactive API documentation

---

## 🛠️ **Technical Architecture**

### **Backend Stack**
- **FastAPI**: Modern, fast web framework
- **scikit-learn**: Machine learning models
- **yfinance**: Real-time market data
- **pandas/numpy**: Data processing
- **asyncio**: Asynchronous processing

### **Frontend Stack**
- **Chart.js**: Interactive visualizations
- **Modern CSS**: Glassmorphism design
- **Responsive Design**: Mobile-first approach
- **Progressive Enhancement**: Graceful degradation

### **Deployment**
- **Docker**: Containerized deployment
- **Docker Compose**: Multi-service orchestration
- **Health Checks**: System monitoring
- **Production Ready**: Logging, error handling

---

## 📈 **Performance Metrics**

- **Model Accuracy**: 55-65% directional accuracy
- **Update Frequency**: Every 5 minutes
- **Response Time**: <100ms for API calls
- **Memory Usage**: <500MB typical
- **Supported Assets**: 8 major assets across stocks, crypto, forex

---

## 🔧 **System Requirements**

### **Minimum Requirements**
- **RAM**: 4GB
- **CPU**: Multi-core processor
- **Storage**: 1GB+ free space
- **Network**: Stable internet connection

### **Recommended**
- **RAM**: 8GB+
- **CPU**: Quad-core processor
- **Storage**: SSD with 2GB+ free space
- **Network**: Broadband connection

---

## 📁 **Project Structure**

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
├── 📄 requirements_enhanced.txt    # Dependencies
├── 📄 Dockerfile                  # Docker configuration
├── 📄 docker-compose.yml          # Multi-service setup
└── 📄 README_AI_Enhanced.md       # Detailed documentation
```

---

## 🎓 **Educational Value**

This system is perfect for:
- **Learning AI in Finance**: Understand how ML models work in practice
- **Comparing Methodologies**: See AI vs traditional analysis side-by-side
- **Research Projects**: Use as a foundation for academic research
- **Professional Development**: Build skills in financial technology
- **Portfolio Management**: Apply concepts to real trading scenarios

---

## 🛡️ **Risk Management Features**

### **Volatility Monitoring**
- Real-time volatility calculations
- Historical volatility comparisons
- Automatic alert system

### **Correlation Analysis**
- Dynamic correlation matrix
- Cross-asset relationship tracking
- Diversification insights

### **Confidence Scoring**
- Model uncertainty quantification
- Prediction reliability metrics
- Decision support indicators

---

## 🔮 **Future Enhancements**

The system is designed for extensibility:
- Additional ML models (LSTM, Transformer)
- More asset classes (commodities, bonds)
- Advanced risk metrics (VaR, CVaR)
- Portfolio optimization algorithms
- Social sentiment analysis
- News integration and NLP
- Options and derivatives analysis

---

## 🤝 **Contributing**

We welcome contributions! Areas for improvement:
- Additional ML models
- More technical indicators
- Enhanced visualization
- Performance optimization
- Documentation improvements
- Testing coverage

---

## 🎉 **Live Demo**

- **Dashboard**: [https://tatsuru-kikuchi.github.io/MCP/](https://tatsuru-kikuchi.github.io/MCP/)
- **Repository**: [https://github.com/Tatsuru-Kikuchi/MCP-stock](https://github.com/Tatsuru-Kikuchi/MCP-stock)

---

## 📄 **License**

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ **Important Disclaimer**

**This system is for educational and research purposes only.**

- 🚫 **Not Financial Advice**: Do not use as the sole basis for investment decisions
- 📊 **Past Performance**: Historical results do not guarantee future performance
- 🔍 **Do Your Research**: Always conduct thorough research before investing
- 💼 **Consult Professionals**: Seek advice from qualified financial advisors
- 📉 **Risk Warning**: All investments carry risk of loss

---

## 🙏 **Acknowledgments**

- **Yahoo Finance** for providing market data
- **scikit-learn** for machine learning capabilities
- **FastAPI** for the web framework
- **Chart.js** for interactive visualizations
- **The Open Source Community** for inspiration and tools

---

**⭐ Star this repository if you find it useful!**

**📧 Questions?** Open an issue or contact the maintainers.

**🔗 Links:**
- [GitHub Repository](https://github.com/Tatsuru-Kikuchi/MCP-stock)
- [Live Demo](https://tatsuru-kikuchi.github.io/MCP/)
- [Detailed Documentation](README_AI_Enhanced.md)

---

*Built with ❤️ by the MCP-Stock team*

**🚀 Ready to explore the future of AI-powered financial analysis!**