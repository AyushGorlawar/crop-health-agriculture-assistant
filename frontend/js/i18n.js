// Internationalization Module
class I18nModule {
    constructor() {
        this.translations = {
            'en': {
                // Navigation
                'app_title': 'Crop Health Assistant',
                'disease_detection': 'Disease Detection',
                'market_prices': 'Market Prices',
                'weather': 'Weather',
                'farming_tips': 'Farming Tips',
                
                // Disease Detection
                'upload_image': 'Upload Crop Image',
                'click_to_upload': 'Click to upload or drag and drop',
                'supports_formats': 'Supports: JPG, PNG, JPEG (Max: 16MB)',
                'analyze_image': 'Analyze Image',
                'analysis_results': 'Analysis Results',
                'upload_to_start': 'Upload an image to get started',
                'image_selected': 'Image selected successfully!',
                'analyzing_image': 'Analyzing image for diseases...',
                'fetching_remedies': 'Fetching remedies...',
                'fetching_tips': 'Fetching yield tips...',
                'treatment_options': 'Treatment Options',
                'organic_remedies': 'Organic Remedies',
                'chemical_treatments': 'Chemical Treatments',
                'preventive_measures': 'Preventive Measures',
                'yield_improvement': 'Yield Improvement Tips',
                
                // Market Prices
                'select_crop': 'Select Crop',
                'all_markets': 'All Markets',
                'get_prices': 'Get Prices',
                'market_prices_title': 'Market Prices',
                'market_information': 'Market Information',
                'crop': 'Crop',
                'source': 'Source',
                'last_updated': 'Last Updated',
                'no_price_data': 'No price data available',
                'price_comparison': 'Market Prices Comparison',
                'price_trends': 'Price Trends',
                'fetching_prices': 'Fetching market prices...',
                
                // Weather
                'location': 'Location',
                'get_weather': 'Get Weather',
                'weather_forecast': 'Weather Forecast',
                'weather_information': 'Weather Information',
                'current_weather': 'Current Weather',
                'day_forecast': '5-Day Forecast',
                'humidity': 'Humidity',
                'wind': 'Wind',
                'pressure': 'Pressure',
                'no_weather_data': 'No weather data available',
                'farming_recommendations': 'Farming Recommendations',
                'fetching_weather': 'Fetching weather data...',
                
                // Farming Tips
                'select_crop_tips': 'Select Crop',
                'get_tips': 'Get Tips',
                'farming_guide': 'Farming Guide',
                'select_crop_guide': 'Select a crop to get farming tips and calendar',
                'yield_improvement_guide': 'Yield Improvement Guide',
                'crop_calendar': 'Crop Calendar & Sowing Guide',
                'sowing_times': 'Sowing Times',
                'harvest_times': 'Harvest Times',
                'growth_duration': 'Growth Duration',
                'plant_spacing': 'Plant Spacing',
                'seed_rate': 'Seed Rate',
                'kharif_season': 'Kharif Season',
                'rabi_season': 'Rabi Season',
                'zaid_season': 'Zaid Season',
                'fetching_tips': 'Fetching farming tips...',
                
                // Common
                'processing': 'Processing...',
                'error_occurred': 'An error occurred. Please try again.',
                'please_select_image': 'Please select an image first',
                'please_upload_valid': 'Please upload a valid image file (JPG, PNG)',
                'image_size_limit': 'Image size should be less than 16MB',
                'failed_to_fetch': 'Failed to fetch data',
                'no_data_available': 'No data available',
                
                // Severity levels
                'high': 'High',
                'medium': 'Medium',
                'low': 'Low',
                'healthy': 'Healthy',
                'disease': 'Disease',
                'severe': 'Severe'
            },
            'hi': {
                // Navigation
                'app_title': 'फसल स्वास्थ्य सहायक',
                'disease_detection': 'रोग पहचान',
                'market_prices': 'बाजार मूल्य',
                'weather': 'मौसम',
                'farming_tips': 'खेती के सुझाव',
                
                // Disease Detection
                'upload_image': 'फसल की छवि अपलोड करें',
                'click_to_upload': 'अपलोड करने के लिए क्लिक करें या खींचें और छोड़ें',
                'supports_formats': 'समर्थन: JPG, PNG, JPEG (अधिकतम: 16MB)',
                'analyze_image': 'छवि का विश्लेषण करें',
                'analysis_results': 'विश्लेषण परिणाम',
                'upload_to_start': 'शुरू करने के लिए एक छवि अपलोड करें',
                'image_selected': 'छवि सफलतापूर्वक चुनी गई!',
                'analyzing_image': 'रोगों के लिए छवि का विश्लेषण कर रहा है...',
                'fetching_remedies': 'उपचार प्राप्त कर रहा है...',
                'fetching_tips': 'उपज सुझाव प्राप्त कर रहा है...',
                'treatment_options': 'उपचार विकल्प',
                'organic_remedies': 'जैविक उपचार',
                'chemical_treatments': 'रासायनिक उपचार',
                'preventive_measures': 'निवारक उपाय',
                'yield_improvement': 'उपज सुधार सुझाव',
                
                // Market Prices
                'select_crop': 'फसल चुनें',
                'all_markets': 'सभी बाजार',
                'get_prices': 'मूल्य प्राप्त करें',
                'market_prices_title': 'बाजार मूल्य',
                'market_information': 'बाजार जानकारी',
                'crop': 'फसल',
                'source': 'स्रोत',
                'last_updated': 'अंतिम अपडेट',
                'no_price_data': 'कोई मूल्य डेटा उपलब्ध नहीं',
                'price_comparison': 'बाजार मूल्य तुलना',
                'price_trends': 'मूल्य रुझान',
                'fetching_prices': 'बाजार मूल्य प्राप्त कर रहा है...',
                
                // Weather
                'location': 'स्थान',
                'get_weather': 'मौसम प्राप्त करें',
                'weather_forecast': 'मौसम पूर्वानुमान',
                'weather_information': 'मौसम जानकारी',
                'current_weather': 'वर्तमान मौसम',
                'day_forecast': '5-दिन का पूर्वानुमान',
                'humidity': 'आर्द्रता',
                'wind': 'हवा',
                'pressure': 'दबाव',
                'no_weather_data': 'कोई मौसम डेटा उपलब्ध नहीं',
                'farming_recommendations': 'खेती के सुझाव',
                'fetching_weather': 'मौसम डेटा प्राप्त कर रहा है...',
                
                // Common
                'processing': 'प्रक्रिया कर रहा है...',
                'error_occurred': 'एक त्रुटि हुई। कृपया पुनः प्रयास करें।',
                'please_select_image': 'कृपया पहले एक छवि चुनें',
                'please_upload_valid': 'कृपया एक वैध छवि फ़ाइल अपलोड करें (JPG, PNG)',
                'image_size_limit': 'छवि का आकार 16MB से कम होना चाहिए',
                'failed_to_fetch': 'डेटा प्राप्त करने में विफल',
                'no_data_available': 'कोई डेटा उपलब्ध नहीं',
                
                // Severity levels
                'high': 'उच्च',
                'medium': 'मध्यम',
                'low': 'कम',
                'healthy': 'स्वस्थ',
                'disease': 'रोग',
                'severe': 'गंभीर'
            }
        };
        
        this.currentLanguage = 'en';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadLanguage();
    }

    setupEventListeners() {
        // Listen for language change events
        window.addEventListener('languageChanged', (e) => {
            this.changeLanguage(e.detail.language);
        });
    }

    loadLanguage() {
        this.currentLanguage = localStorage.getItem('language') || 'en';
        this.updatePageContent();
    }

    changeLanguage(language) {
        this.currentLanguage = language;
        this.updatePageContent();
    }

    updatePageContent() {
        // Update all translatable elements
        this.translateElements();
    }

    translateElements() {
        // Update navigation
        this.updateText('app_title', '.navbar-brand');
        this.updateText('disease_detection', '#disease-tab');
        this.updateText('market_prices', '#market-tab');
        this.updateText('weather', '#weather-tab');
        this.updateText('farming_tips', '#tips-tab');
        
        // Update form labels and buttons
        this.updateText('upload_image', '.card-header h5');
        this.updateText('analyze_image', '#analyzeBtn');
        this.updateText('analysis_results', '.card-header h5');
        this.updateText('select_crop', 'label[for="cropSelect"]');
        this.updateText('get_prices', '#fetchPricesBtn');
        this.updateText('get_weather', '#fetchWeatherBtn');
        this.updateText('get_tips', '#fetchTipsBtn');
        
        // Update placeholders and help text
        this.updatePlaceholder('click_to_upload', '.upload-content p');
        this.updatePlaceholder('supports_formats', '.upload-content .text-muted');
    }

    updateText(key, selector) {
        const element = document.querySelector(selector);
        if (element) {
            const translation = this.getTranslation(key);
            if (translation) {
                element.textContent = translation;
            }
        }
    }

    updatePlaceholder(key, selector) {
        const element = document.querySelector(selector);
        if (element) {
            const translation = this.getTranslation(key);
            if (translation) {
                element.textContent = translation;
            }
        }
    }

    getTranslation(key) {
        return this.translations[this.currentLanguage]?.[key] || 
               this.translations['en']?.[key] || 
               key;
    }

    translate(key, params = {}) {
        let translation = this.getTranslation(key);
        
        // Replace parameters
        Object.entries(params).forEach(([param, value]) => {
            translation = translation.replace(`{${param}}`, value);
        });
        
        return translation;
    }

    // Method to translate dynamic content
    translateDynamicContent(container, data) {
        if (!container || !data) return;
        
        // This method can be used to translate dynamic content
        // that's loaded via AJAX or generated dynamically
        const elements = container.querySelectorAll('[data-i18n]');
        
        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.getTranslation(key);
            if (translation) {
                element.textContent = translation;
            }
        });
    }

    // Get current language
    getCurrentLanguage() {
        return this.currentLanguage;
    }

    // Get available languages
    getAvailableLanguages() {
        return Object.keys(this.translations);
    }

    // Check if translation exists
    hasTranslation(key) {
        return !!this.translations[this.currentLanguage]?.[key];
    }
}

// Initialize i18n module
document.addEventListener('DOMContentLoaded', () => {
    window.i18n = new I18nModule();
}); 