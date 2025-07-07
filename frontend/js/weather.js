// Weather Module
class WeatherModule {
    constructor() {
        this.locationSelect = document.getElementById('locationSelect');
        this.fetchWeatherBtn = document.getElementById('fetchWeatherBtn');
        this.weatherContent = document.getElementById('weatherContent');
        this.init();
    }

    init() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.fetchWeatherBtn.addEventListener('click', () => {
            this.fetchWeather();
        });

        // Auto-fetch when location changes
        this.locationSelect.addEventListener('change', () => {
            this.fetchWeather();
        });
    }

    async fetchWeather() {
        const location = this.locationSelect.value;

        try {
            window.app.showLoading('Fetching weather data...');
            
            const response = await window.app.makeApiCall(`/weather?location=${encodeURIComponent(location)}`);
            
            if (response.success) {
                this.displayWeather(response.weather);
                this.getFarmingAdvice(location);
            } else {
                throw new Error(response.error || 'Failed to fetch weather');
            }

        } catch (error) {
            window.app.handleError(error, 'weather');
        } finally {
            window.app.hideLoading();
        }
    }

    displayWeather(data) {
        const { location, data: weatherData, source } = data;
        
        if (!weatherData || !weatherData.current) {
            this.weatherContent.innerHTML = `
                <div class="text-center text-muted">
                    <i class="fas fa-cloud fa-3x mb-3"></i>
                    <p>No weather data available for ${location}</p>
                </div>
            `;
            return;
        }

        const current = weatherData.current;
        const forecast = weatherData.forecast || [];

        const weatherHtml = `
            <div class="mb-3">
                <h6><i class="fas fa-info-circle me-2"></i>Weather Information</h6>
                <p class="mb-1"><strong>Location:</strong> ${location}</p>
                <p class="mb-1"><strong>Source:</strong> ${source}</p>
            </div>
            
            <!-- Current Weather -->
            <div class="weather-card mb-4">
                <div class="row align-items-center">
                    <div class="col-md-6">
                        <div class="weather-temp">${current.temp}°C</div>
                        <div class="weather-desc">${current.description}</div>
                    </div>
                    <div class="col-md-6 text-end">
                        <div class="mb-2">
                            <i class="fas fa-tint me-2"></i>
                            Humidity: ${current.humidity}%
                        </div>
                        <div class="mb-2">
                            <i class="fas fa-wind me-2"></i>
                            Wind: ${current.wind_speed} m/s
                        </div>
                        <div>
                            <i class="fas fa-tachometer-alt me-2"></i>
                            Pressure: ${current.pressure} hPa
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Forecast -->
            ${forecast.length > 0 ? `
                <h6><i class="fas fa-calendar-alt me-2"></i>5-Day Forecast</h6>
                <div class="row">
                    ${forecast.map(day => `
                        <div class="col-md-2 col-sm-4 col-6 mb-3">
                            <div class="card text-center">
                                <div class="card-body">
                                    <div class="fw-bold">${this.formatDate(day.date)}</div>
                                    <div class="text-primary">${day.temp_max}°C</div>
                                    <div class="text-muted">${day.temp_min}°C</div>
                                    <small class="text-muted">${day.description}</small>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            ` : ''}
        `;
        
        this.weatherContent.innerHTML = weatherHtml;
    }

    async getFarmingAdvice(location) {
        try {
            const response = await window.app.makeApiCall(`/weather/advice?location=${encodeURIComponent(location)}`);
            
            if (response.success) {
                this.displayFarmingAdvice(response.advice);
            }

        } catch (error) {
            console.error('Error fetching farming advice:', error);
        }
    }

    displayFarmingAdvice(advice) {
        if (!advice || !advice.farming_recommendations || advice.farming_recommendations.length === 0) {
            return;
        }

        const adviceHtml = `
            <div class="mt-4">
                <h6><i class="fas fa-seedling me-2"></i>Farming Recommendations</h6>
                ${advice.farming_recommendations.map(rec => `
                    <div class="tip-card">
                        <div class="d-flex align-items-start">
                            <span class="badge bg-${this.getPriorityColor(rec.priority)} me-2">${rec.priority}</span>
                            <div>
                                <strong>${this.formatRecommendationType(rec.type)}:</strong>
                                ${rec.message}
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        
        this.weatherContent.insertAdjacentHTML('beforeend', adviceHtml);
    }

    getPriorityColor(priority) {
        switch (priority.toLowerCase()) {
            case 'high':
                return 'danger';
            case 'medium':
                return 'warning';
            case 'low':
            default:
                return 'success';
        }
    }

    formatRecommendationType(type) {
        const types = {
            'temperature': 'Temperature',
            'humidity': 'Humidity',
            'precipitation': 'Precipitation',
            'sunlight': 'Sunlight'
        };
        return types[type] || type;
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            weekday: 'short',
            month: 'short',
            day: 'numeric'
        });
    }

    initialize() {
        // Auto-fetch weather when module is initialized
        this.fetchWeather();
    }
}

// Initialize weather module
document.addEventListener('DOMContentLoaded', () => {
    window.weatherModule = new WeatherModule();
}); 