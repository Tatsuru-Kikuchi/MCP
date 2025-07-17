// Combined dashboard script - includes all parts

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

function updatePredictionComparison() {
    const container = document.getElementById('predictionComparison');
    
    container.innerHTML = Object.entries(currentData.predictions).map(([asset, pred]) => `
        <div class="prediction-item">
            <h4>${asset}</h4>
            <div class="prediction-values">
                <span class="ai-prediction">AI: ${pred.ai > 0 ? '+' : ''}${pred.ai.toFixed(2)}%</span>
                <span class="traditional-prediction">Trad: ${pred.traditional > 0 ? '+' : ''}${pred.traditional.toFixed(2)}%</span>
            </div>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: ${pred.confidence * 100}%"></div>
            </div>
        </div>
    `).join('');
}

function updateCorrelationMatrix() {
    const container = document.getElementById('correlationMatrix');
    const assets = Object.keys(currentData.correlations);
    
    let html = '<table class="correlation-table"><tr><th></th>';
    assets.forEach(asset => {
        html += `<th>${asset}</th>`;
    });
    html += '</tr>';
    
    assets.forEach(asset1 => {
        html += `<tr><th>${asset1}</th>`;
        assets.forEach(asset2 => {
            const corr = currentData.correlations[asset1][asset2];
            const absCorr = Math.abs(corr);
            let className = 'corr-low';
            
            if (absCorr > 0.7) className = 'corr-high';
            else if (absCorr > 0.3) className = 'corr-medium';
            
            html += `<td class="${className}">${corr.toFixed(2)}</td>`;
        });
        html += '</tr>';
    });
    
    html += '</table>';
    container.innerHTML = html;
}

function updateCharts() {
    const selectedAsset = document.getElementById('assetSelect').value;
    const timeFrame = document.getElementById('timeFrame').value;
    
    updatePriceChart(selectedAsset);
    updateVolatilityChart(selectedAsset);
    updateReturnsChart(selectedAsset);
    updateRiskReturnChart();
}

function updatePriceChart(selectedAsset) {
    const ctx = document.getElementById('priceChart').getContext('2d');
    
    if (charts.price) {
        charts.price.destroy();
    }
    
    const assets = selectedAsset === 'all' ? Object.keys(currentData.prices) : [selectedAsset];
    const datasets = assets.map((asset, index) => {
        const colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#34495e'];
        const data = currentData.prices[asset].history;
        
        return {
            label: asset,
            data: data.map(d => ({ x: d.date, y: d.price })),
            borderColor: colors[index % colors.length],
            backgroundColor: colors[index % colors.length] + '20',
            fill: false,
            tension: 0.1
        };
    });
    
    charts.price = new Chart(ctx, {
        type: 'line',
        data: { datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                },
                y: {
                    beginAtZero: false
                }
            },
            plugins: {
                legend: {
                    display: assets.length > 1
                }
            }
        }
    });
}

function updateVolatilityChart(selectedAsset) {
    const ctx = document.getElementById('volatilityChart').getContext('2d');
    
    if (charts.volatility) {
        charts.volatility.destroy();
    }
    
    const assets = selectedAsset === 'all' ? Object.keys(currentData.prices) : [selectedAsset];
    const data = assets.map(asset => currentData.prices[asset].volatility);
    
    charts.volatility = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: assets,
            datasets: [{
                label: 'Volatility (%)',
                data: data,
                backgroundColor: assets.map((_, i) => {
                    const colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#34495e'];
                    return colors[i % colors.length];
                })
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function updateReturnsChart(selectedAsset) {
    const ctx = document.getElementById('returnsChart').getContext('2d');
    
    if (charts.returns) {
        charts.returns.destroy();
    }
    
    const assets = selectedAsset === 'all' ? Object.keys(currentData.prices) : [selectedAsset];
    const datasets = assets.map((asset, index) => {
        const colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#34495e'];
        const returns = currentData.prices[asset].history.map(d => d.return);
        
        return {
            label: asset,
            data: returns,
            backgroundColor: colors[index % colors.length] + '80',
            borderColor: colors[index % colors.length],
            borderWidth: 1
        };
    });
    
    charts.returns = new Chart(ctx, {
        type: 'bar',
        data: { 
            labels: currentData.prices[Object.keys(currentData.prices)[0]].history.map(d => d.date.toLocaleDateString()),
            datasets 
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: assets.length > 1
                }
            }
        }
    });
}

function updateRiskReturnChart() {
    const ctx = document.getElementById('riskReturnChart').getContext('2d');
    
    if (charts.riskReturn) {
        charts.riskReturn.destroy();
    }
    
    const assets = Object.keys(currentData.prices);
    const data = assets.map(asset => {
        const returns = currentData.prices[asset].history.map(d => d.return);
        const avgReturn = returns.reduce((a, b) => a + b, 0) / returns.length;
        const volatility = currentData.prices[asset].volatility;
        
        return {
            x: volatility,
            y: avgReturn,
            label: asset
        };
    });
    
    charts.riskReturn = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Risk vs Return',
                data: data,
                backgroundColor: assets.map((_, i) => {
                    const colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#34495e'];
                    return colors[i % colors.length];
                })
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Risk (Volatility %)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Return (%)'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${data[context.dataIndex].label}: Risk ${context.parsed.x.toFixed(2)}%, Return ${context.parsed.y.toFixed(2)}%`;
                        }
                    }
                }
            }
        }
    });
}