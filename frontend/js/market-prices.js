// Market Prices Module
class MarketPricesModule {
    constructor() {
        this.cropSelect = document.getElementById('cropSelect');
        this.marketSelect = document.getElementById('marketSelect');
        this.fetchPricesBtn = document.getElementById('fetchPricesBtn');
        this.pricesTable = document.getElementById('pricesTable');
        this.priceChart = document.getElementById('priceChart');
        this.chartInstance = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.fetchPricesBtn.addEventListener('click', () => {
            this.fetchPrices();
        });

        // Auto-fetch when crop or market changes
        this.cropSelect.addEventListener('change', () => {
            this.fetchPrices();
        });

        this.marketSelect.addEventListener('change', () => {
            this.fetchPrices();
        });
    }

    async fetchPrices() {
        const crop = this.cropSelect.value;
        const market = this.marketSelect.value;

        try {
            window.app.showLoading('Fetching market prices...');
            
            const response = await window.app.makeApiCall(`/market-prices?crop=${encodeURIComponent(crop)}&market=${encodeURIComponent(market)}`);
            
            if (response.success) {
                this.displayPrices(response.prices);
                this.updateChart(response.prices);
            } else {
                throw new Error(response.error || 'Failed to fetch prices');
            }

        } catch (error) {
            window.app.handleError(error, 'market prices');
        } finally {
            window.app.hideLoading();
        }
    }

    displayPrices(data) {
        const { crop, prices, source, last_updated } = data;
        
        if (!prices || prices.length === 0) {
            this.pricesTable.innerHTML = `
                <div class="text-center text-muted">
                    <i class="fas fa-chart-line fa-3x mb-3"></i>
                    <p>No price data available for ${crop}</p>
                </div>
            `;
            return;
        }

        const pricesHtml = `
            <div class="mb-3">
                <h6><i class="fas fa-info-circle me-2"></i>Market Information</h6>
                <p class="mb-1"><strong>Crop:</strong> ${crop}</p>
                <p class="mb-1"><strong>Source:</strong> ${source}</p>
                <p class="mb-1"><strong>Last Updated:</strong> ${window.app.formatDateTime(last_updated)}</p>
            </div>
            
            <div class="row">
                ${prices.map(price => `
                    <div class="col-md-6 col-lg-4 mb-3">
                        <div class="price-card">
                            <div class="d-flex justify-content-between align-items-start">
                                <div>
                                    <div class="price-value">${window.app.formatCurrency(price.price)}</div>
                                    <div class="price-market">${price.market}</div>
                                </div>
                                <div class="text-end">
                                    <small>per ${price.unit}</small><br>
                                    <small>${price.date}</small>
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        
        this.pricesTable.innerHTML = pricesHtml;
    }

    updateChart(data) {
        if (!data || data.length === 0) return;

        const ctx = this.priceChart.getContext('2d');
        
        // Destroy existing chart
        if (this.chartInstance) {
            this.chartInstance.destroy();
        }

        const chartData = {
            labels: data.map(price => price.market),
            datasets: [{
                label: 'Price (₹/kg)',
                data: data.map(price => price.price),
                backgroundColor: 'rgba(25, 135, 84, 0.2)',
                borderColor: 'rgba(25, 135, 84, 1)',
                borderWidth: 2,
                borderRadius: 5,
                fill: true
            }]
        };

        this.chartInstance = new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Market Prices Comparison'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Price (₹/kg)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Market'
                        }
                    }
                }
            }
        });
    }

    async getPriceTrends(crop, days = 7) {
        try {
            const response = await window.app.makeApiCall(`/market-prices/trends?crop=${encodeURIComponent(crop)}&days=${days}`);
            
            if (response.success) {
                this.displayTrends(response.trends);
            } else {
                throw new Error(response.error || 'Failed to fetch trends');
            }

        } catch (error) {
            window.app.handleError(error, 'price trends');
        }
    }

    displayTrends(trends) {
        const trendsHtml = `
            <div class="mt-4">
                <h6><i class="fas fa-chart-area me-2"></i>Price Trends (${trends.period})</h6>
                <div class="table-responsive">
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Price</th>
                                <th>Change</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${trends.trends.map(trend => `
                                <tr>
                                    <td>${trend.date}</td>
                                    <td>${window.app.formatCurrency(trend.price)}</td>
                                    <td class="${trend.change >= 0 ? 'text-success' : 'text-danger'}">
                                        ${trend.change >= 0 ? '+' : ''}${trend.change}%
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
        
        this.pricesTable.insertAdjacentHTML('beforeend', trendsHtml);
    }

    initialize() {
        // Auto-fetch prices when module is initialized
        this.fetchPrices();
    }
}

// Initialize market prices module
document.addEventListener('DOMContentLoaded', () => {
    window.marketPricesModule = new MarketPricesModule();
}); 