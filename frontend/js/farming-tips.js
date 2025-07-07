// Farming Tips Module
class FarmingTipsModule {
    constructor() {
        this.tipsCropSelect = document.getElementById('tipsCropSelect');
        this.fetchTipsBtn = document.getElementById('fetchTipsBtn');
        this.tipsContent = document.getElementById('tipsContent');
        this.init();
    }

    init() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.fetchTipsBtn.addEventListener('click', () => {
            this.fetchTips();
        });

        // Auto-fetch when crop changes
        this.tipsCropSelect.addEventListener('change', () => {
            this.fetchTips();
        });
    }

    async fetchTips() {
        const crop = this.tipsCropSelect.value;

        try {
            window.app.showLoading('Fetching farming tips...');
            
            const response = await window.app.makeApiCall(`/yield-tips?crop=${encodeURIComponent(crop)}`);
            
            if (response.success) {
                this.displayTips(response.tips);
                this.fetchCropCalendar(crop);
            } else {
                throw new Error(response.error || 'Failed to fetch tips');
            }

        } catch (error) {
            window.app.handleError(error, 'farming tips');
        } finally {
            window.app.hideLoading();
        }
    }

    displayTips(tips) {
        if (!tips || Object.keys(tips).length === 0) {
            this.tipsContent.innerHTML = `
                <div class="text-center text-muted">
                    <i class="fas fa-lightbulb fa-3x mb-3"></i>
                    <p>No farming tips available for this crop</p>
                </div>
            `;
            return;
        }

        const tipsHtml = `
            <div class="mb-4">
                <h6><i class="fas fa-chart-line me-2"></i>Yield Improvement Guide</h6>
                
                ${Object.entries(tips).map(([category, tipList]) => `
                    <div class="tip-card">
                        <h6><i class="fas fa-seedling me-2"></i>${this.formatCategoryName(category)}</h6>
                        <ul class="mb-0">
                            ${tipList.map(tip => `<li>${tip}</li>`).join('')}
                        </ul>
                    </div>
                `).join('')}
            </div>
        `;
        
        this.tipsContent.innerHTML = tipsHtml;
    }

    async fetchCropCalendar(crop) {
        try {
            const response = await window.app.makeApiCall(`/crop-calendar?crop=${encodeURIComponent(crop)}&location=india`);
            
            if (response.success) {
                this.displayCropCalendar(response.calendar);
            }

        } catch (error) {
            console.error('Error fetching crop calendar:', error);
        }
    }

    displayCropCalendar(calendar) {
        if (!calendar || !calendar.calendar) {
            return;
        }

        const calData = calendar.calendar;
        
        const calendarHtml = `
            <div class="mt-4">
                <h6><i class="fas fa-calendar-alt me-2"></i>Crop Calendar & Sowing Guide</h6>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">
                                <h6 class="mb-0"><i class="fas fa-clock me-2"></i>Sowing Times</h6>
                            </div>
                            <div class="card-body">
                                ${Object.entries(calData.sowing_time || {}).map(([season, time]) => `
                                    <div class="mb-2">
                                        <strong>${this.formatSeasonName(season)}:</strong> ${time}
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">
                                <h6 class="mb-0"><i class="fas fa-cut me-2"></i>Harvest Times</h6>
                            </div>
                            <div class="card-body">
                                ${Object.entries(calData.harvest_time || {}).map(([season, time]) => `
                                    <div class="mb-2">
                                        <strong>${this.formatSeasonName(season)}:</strong> ${time}
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row mt-3">
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body text-center">
                                <i class="fas fa-calendar-day fa-2x text-primary mb-2"></i>
                                <h6>Growth Duration</h6>
                                <p class="mb-0">${calData.growth_duration || 'N/A'}</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body text-center">
                                <i class="fas fa-ruler fa-2x text-success mb-2"></i>
                                <h6>Plant Spacing</h6>
                                <p class="mb-0">${calData.spacing || 'N/A'}</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body text-center">
                                <i class="fas fa-seedling fa-2x text-warning mb-2"></i>
                                <h6>Seed Rate</h6>
                                <p class="mb-0">${calData.seed_rate || 'N/A'}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.tipsContent.insertAdjacentHTML('beforeend', calendarHtml);
    }

    formatCategoryName(category) {
        return category.split('_').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    }

    formatSeasonName(season) {
        const seasons = {
            'kharif': 'Kharif Season',
            'rabi': 'Rabi Season',
            'zaid': 'Zaid Season'
        };
        return seasons[season] || season;
    }

    initialize() {
        // Auto-fetch tips when module is initialized
        this.fetchTips();
    }
}

// Initialize farming tips module
document.addEventListener('DOMContentLoaded', () => {
    window.farmingTipsModule = new FarmingTipsModule();
}); 