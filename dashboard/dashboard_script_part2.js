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