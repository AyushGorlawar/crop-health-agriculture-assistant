// Main application JavaScript file
class CropHealthApp {
    constructor() {
        // Use environment variable or default to localhost for development
        this.apiBaseUrl = window.location.hostname === 'localhost' 
            ? 'http://localhost:5000/api'
            : 'https://crop-health-backend.onrender.com/api';
        this.currentLanguage = 'en';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeLanguage();
        this.showWelcomeMessage();
    }

    setupEventListeners() {
        // Language selector
        document.querySelectorAll('#language-menu .dropdown-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const lang = e.target.dataset.lang;
                this.changeLanguage(lang);
            });
        });

        // Tab switching
        document.querySelectorAll('[data-bs-toggle="tab"]').forEach(tab => {
            tab.addEventListener('shown.bs.tab', (e) => {
                this.onTabChange(e.target.id);
            });
        });
    }

    initializeLanguage() {
        // Set default language
        this.currentLanguage = localStorage.getItem('language') || 'en';
        this.updateLanguageDisplay();
    }

    changeLanguage(lang) {
        this.currentLanguage = lang;
        localStorage.setItem('language', lang);
        this.updateLanguageDisplay();
        
        // Trigger language change event
        window.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
    }

    updateLanguageDisplay() {
        const languageNames = {
            'en': 'English',
            'hi': 'हिंदी',
            'mr': 'मराठी',
            'te': 'తెలుగు'
        };
        
        document.getElementById('current-language').textContent = languageNames[this.currentLanguage] || 'English';
    }

    onTabChange(tabId) {
        // Handle tab-specific initialization
        switch(tabId) {
            case 'market-tab':
                this.initializeMarketPrices();
                break;
            case 'weather-tab':
                this.initializeWeather();
                break;
            case 'tips-tab':
                this.initializeFarmingTips();
                break;
        }
    }

    showWelcomeMessage() {
        const welcomeMessages = {
            'en': 'Welcome to Crop Health Assistant! Upload an image to detect diseases.',
            'hi': 'फसल स्वास्थ्य सहायक में आपका स्वागत है! रोगों का पता लगाने के लिए एक छवि अपलोड करें।',
            'mr': 'पीक आरोग्य सहाय्यकामध्ये आपले स्वागत आहे! रोग शोधण्यासाठी एक प्रतिमा अपलोड करा।',
            'te': 'పంట ఆరోగ్య సహాయకుడికి స్వాగతం! వ్యాధులను గుర్తించడానికి ఒక చిత్రాన్ని అప్‌లోడ్ చేయండి।'
        };
        
        // Show welcome message in results area
        const resultsArea = document.getElementById('resultsArea');
        if (resultsArea) {
            resultsArea.innerHTML = `
                <div class="text-center text-muted">
                    <i class="fas fa-microscope fa-3x mb-3"></i>
                    <p>${welcomeMessages[this.currentLanguage] || welcomeMessages['en']}</p>
                </div>
            `;
        }
    }

    // API Helper Methods
    async makeApiCall(endpoint, options = {}) {
        try {
            const url = `${this.apiBaseUrl}${endpoint}`;
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API call failed:', error);
            throw error;
        }
    }

    // Loading Modal
    showLoading(message = 'Processing...') {
        document.getElementById('loadingText').textContent = message;
        const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
        modal.show();
    }

    hideLoading() {
        const modal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
        if (modal) {
            modal.hide();
        }
    }

    // Notification System
    showNotification(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    // Error Handling
    handleError(error, context = '') {
        console.error(`Error in ${context}:`, error);
        
        const errorMessages = {
            'en': 'An error occurred. Please try again.',
            'hi': 'एक त्रुटि हुई। कृपया पुनः प्रयास करें।',
            'mr': 'एक त्रुटी आली. कृपया पुन्हा प्रयत्न करा.',
            'te': 'ఒక లోపం జరిగింది. దయచేసి మళ్లీ ప్రయత్నించండి.'
        };
        
        this.showNotification(
            errorMessages[this.currentLanguage] || errorMessages['en'],
            'danger'
        );
    }

    // Utility Methods
    formatCurrency(amount, currency = '₹') {
        return `${currency}${parseFloat(amount).toFixed(2)}`;
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString();
    }

    formatDateTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString();
    }

    // Image handling
    validateImage(file) {
        const maxSize = 16 * 1024 * 1024; // 16MB
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        
        if (!allowedTypes.includes(file.type)) {
            throw new Error('Please upload a valid image file (JPG, PNG)');
        }
        
        if (file.size > maxSize) {
            throw new Error('Image size should be less than 16MB');
        }
        
        return true;
    }

    // Initialize specific modules
    initializeMarketPrices() {
        // This will be called when market prices tab is opened
        if (window.marketPricesModule) {
            window.marketPricesModule.initialize();
        }
    }

    initializeWeather() {
        // This will be called when weather tab is opened
        if (window.weatherModule) {
            window.weatherModule.initialize();
        }
    }

    initializeFarmingTips() {
        // This will be called when farming tips tab is opened
        if (window.farmingTipsModule) {
            window.farmingTipsModule.initialize();
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new CropHealthApp();
});

// Export for use in other modules
window.CropHealthApp = CropHealthApp; 