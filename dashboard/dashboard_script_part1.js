// Global variables
let currentData = null;
let charts = {};
let refreshInterval = null;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    setupEventListeners();
    loadData();
});

function initializeDashboard() {
    console.log('Initializing AI-Enhanced Dashboard...');
    
    // Set up auto-refresh (every 5 minutes)
    refreshInterval = setInterval(loadData, 300000);
}

function setupEventListeners() {
    document.getElementById('assetSelect').addEventListener('change', updateCharts);
    document.getElementById('timeFrame').addEventListener('change', updateCharts);
}

async function loadData() {
    try {
        showLoading(true);
        
        // In a real implementation, this would fetch from your backend API
        // For demo purposes, we'll generate sample data
        currentData = await generateSampleData();
        
        updateDashboard();
        showLoading(false);
        
    } catch (error) {
        console.error('Error loading data:', error);
        showLoading(false);
    }
}

function showLoading(show) {
    document.getElementById('loadingIndicator').style.display = show ? 'block' : 'none';
    document.getElementById('dashboardContent').style.display = show ? 'none' : 'block';
}

function refreshData() {
    loadData();
}

async function generateSampleData() {
    // This simulates real-time data that would come from your backend
    const assets = ['SP500', 'Gold', 'Bitcoin', 'Ethereum', 'XRP', 'JPY_USD', 'EUR_USD', 'USD_Index'];
    const data = {
        prices: {},
        predictions: {},
        sentiment: Math.random() > 0.5 ? (Math.random() > 0.5 ? 'bullish' : 'bearish') : 'neutral',
        alerts: [],
        opportunities: [],
        correlations: {}
    };
    
    assets.forEach(asset => {
        const basePrice = Math.random() * 1000 + 100;
        const dailyReturn = (Math.random() - 0.5) * 10;
        const volatility = Math.random() * 5 + 1;
        
        data.prices[asset] = {
            current: basePrice,
            change: dailyReturn,
            volatility: volatility,
            history: generatePriceHistory(basePrice, 30)
        };
        
        data.predictions[asset] = {
            ai: (Math.random() - 0.5) * 5,
            traditional: (Math.random() - 0.5) * 5,
            confidence: Math.random() * 0.8 + 0.2
        };
        
        // Add high volatility alerts
        if (volatility > 4) {
            data.alerts.push(`High volatility detected in ${asset}: ${volatility.toFixed(2)}%`);
        }
        
        // Add opportunities
        if (Math.abs(data.predictions[asset].ai) > 2 && data.predictions[asset].confidence > 0.7) {
            data.opportunities.push({
                asset: asset,
                prediction: data.predictions[asset].ai,
                confidence: data.predictions[asset].confidence
            });
        }
    });
    
    // Generate correlation matrix
    assets.forEach(asset1 => {
        data.correlations[asset1] = {};
        assets.forEach(asset2 => {
            if (asset1 === asset2) {
                data.correlations[asset1][asset2] = 1;
            } else {
                data.correlations[asset1][asset2] = (Math.random() - 0.5) * 2;
            }
        });
    });
    
    return data;
}

function generatePriceHistory(basePrice, days) {
    const history = [];
    let currentPrice = basePrice;
    
    for (let i = 0; i < days; i++) {
        const change = (Math.random() - 0.5) * 0.1;
        currentPrice *= (1 + change);
        history.push({
            date: new Date(Date.now() - (days - i) * 24 * 60 * 60 * 1000),
            price: currentPrice,
            return: change * 100
        });
    }
    
    return history;
}

function updateDashboard() {
    updateMarketSentiment();
    updateAlerts();
    updateOpportunities();
    updateRealTimeData();
    updatePredictionComparison();
    updateCorrelationMatrix();
    updateCharts();
}

function updateMarketSentiment() {
    const indicator = document.getElementById('sentimentIndicator');
    const sentiment = currentData.sentiment;
    
    indicator.textContent = sentiment.charAt(0).toUpperCase() + sentiment.slice(1);
    indicator.className = `sentiment-indicator ${sentiment}`;
}

function updateAlerts() {
    const container = document.getElementById('alertsContainer');
    const list = document.getElementById('alertsList');
    
    if (currentData.alerts.length > 0) {
        container.style.display = 'block';
        list.innerHTML = currentData.alerts.map(alert => 
            `<div class="alert-item">${alert}</div>`
        ).join('');
    } else {
        container.style.display = 'none';
    }
}

function updateOpportunities() {
    const list = document.getElementById('opportunitiesList');
    
    if (currentData.opportunities.length > 0) {
        list.innerHTML = currentData.opportunities
            .sort((a, b) => b.confidence - a.confidence)
            .slice(0, 5)
            .map(opp => `
                <li class="opportunity-item">
                    <strong>${opp.asset}</strong>: ${opp.prediction > 0 ? '+' : ''}${opp.prediction.toFixed(2)}%
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: ${opp.confidence * 100}%"></div>
                    </div>
                </li>
            `).join('');
    } else {
        list.innerHTML = '<li>No significant opportunities detected</li>';
    }
}

function updateRealTimeData() {
    const container = document.getElementById('realTimeData');
    
    container.innerHTML = Object.entries(currentData.prices).map(([asset, data]) => `
        <div class="data-item">
            <h4>${asset}</h4>
            <div class="data-value">$${data.current.toFixed(2)}</div>
            <div class="data-change ${data.change >= 0 ? 'positive' : 'negative'}">
                ${data.change >= 0 ? '+' : ''}${data.change.toFixed(2)}%
            </div>
        </div>
    `).join('');
}