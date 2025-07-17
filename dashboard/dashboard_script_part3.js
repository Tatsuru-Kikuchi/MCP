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
        type: 'histogram',
        data: { datasets },
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

// WebSocket connection for real-time updates (optional)
function initWebSocket() {
    // This would connect to your WebSocket server for real-time updates
    // const ws = new WebSocket('ws://localhost:8080/ws');
    // ws.onmessage = function(event) {
    //     const data = JSON.parse(event.data);
    //     updateRealTimeData(data);
    // };
}

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        updateDashboard,
        updateCharts,
        generateSampleData
    };
}