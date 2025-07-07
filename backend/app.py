from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import json
import requests
from datetime import datetime
import logging
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import io
import base64

# Import our custom modules
from api.disease_detection import DiseaseDetector
from api.market_prices import MarketPriceAPI
from api.weather_api import WeatherAPI
from api.remedies import RemediesAPI
from utils.image_processor import ImageProcessor
from config import config

app = Flask(__name__)
CORS(app)

# Configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db = SQLAlchemy(app)

# Initialize API services
disease_detector = DiseaseDetector()
market_api = MarketPriceAPI()
weather_api = WeatherAPI()
remedies_api = RemediesAPI()
image_processor = ImageProcessor()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Models
class CropAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255))
    crop_type = db.Column(db.String(100))
    disease_detected = db.Column(db.String(200))
    confidence = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_location = db.Column(db.String(100))

class MarketPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100))
    market_name = db.Column(db.String(100))
    price = db.Column(db.Float)
    unit = db.Column(db.String(20))
    date = db.Column(db.Date)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def home():
    """API Home endpoint"""
    return jsonify({
        'message': 'Crop Health & Agriculture Assistant API',
        'version': '1.0.0',
        'endpoints': {
            'disease_detection': '/api/detect-disease',
            'market_prices': '/api/market-prices',
            'weather': '/api/weather',
            'remedies': '/api/remedies',
            'yield_tips': '/api/yield-tips',
            'crop_calendar': '/api/crop-calendar'
        }
    })

@app.route('/api/detect-disease', methods=['POST'])
def detect_disease():
    """Detect crop disease from uploaded image"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Process image
        image_data = file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Detect disease
        result = disease_detector.detect(image)
        
        # Save analysis to database
        filename = secure_filename(file.filename or 'unknown.jpg')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        analysis = CropAnalysis(
            image_path=filepath,
            crop_type=result.get('crop_type', 'Unknown'),
            disease_detected=result.get('disease', 'Healthy'),
            confidence=result.get('confidence', 0.0),
            user_location=request.form.get('location', 'Unknown')
        )
        db.session.add(analysis)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'result': result,
            'analysis_id': analysis.id
        })
        
    except Exception as e:
        logger.error(f"Error in disease detection: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/market-prices', methods=['GET'])
def get_market_prices():
    """Get current market prices for crops"""
    try:
        crop_name = request.args.get('crop', 'tomato')
        market_name = request.args.get('market', 'all')
        
        prices = market_api.get_prices(crop_name, market_name)
        
        return jsonify({
            'success': True,
            'prices': prices,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching market prices: {str(e)}")
        return jsonify({'error': 'Failed to fetch market prices'}), 500

@app.route('/api/weather', methods=['GET'])
def get_weather():
    """Get weather forecast for farming"""
    try:
        location = request.args.get('location', 'Mumbai')
        
        weather_data = weather_api.get_forecast(location)
        
        return jsonify({
            'success': True,
            'weather': weather_data,
            'location': location
        })
        
    except Exception as e:
        logger.error(f"Error fetching weather: {str(e)}")
        return jsonify({'error': 'Failed to fetch weather data'}), 500

@app.route('/api/remedies', methods=['GET'])
def get_remedies():
    """Get remedies for detected disease"""
    try:
        disease = request.args.get('disease', '')
        crop_type = request.args.get('crop', '')
        
        remedies = remedies_api.get_remedies(disease, crop_type)
        
        return jsonify({
            'success': True,
            'remedies': remedies
        })
        
    except Exception as e:
        logger.error(f"Error fetching remedies: {str(e)}")
        return jsonify({'error': 'Failed to fetch remedies'}), 500

@app.route('/api/yield-tips', methods=['GET'])
def get_yield_tips():
    """Get yield improvement tips for crop"""
    try:
        crop_type = request.args.get('crop', 'tomato')
        
        tips = remedies_api.get_yield_tips(crop_type)
        
        return jsonify({
            'success': True,
            'tips': tips
        })
        
    except Exception as e:
        logger.error(f"Error fetching yield tips: {str(e)}")
        return jsonify({'error': 'Failed to fetch yield tips'}), 500

@app.route('/api/crop-calendar', methods=['GET'])
def get_crop_calendar():
    """Get crop calendar and sowing guide"""
    try:
        crop_type = request.args.get('crop', 'tomato')
        location = request.args.get('location', 'India')
        
        calendar = remedies_api.get_crop_calendar(crop_type, location)
        
        return jsonify({
            'success': True,
            'calendar': calendar
        })
        
    except Exception as e:
        logger.error(f"Error fetching crop calendar: {str(e)}")
        return jsonify({'error': 'Failed to fetch crop calendar'}), 500

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get supported languages"""
    languages = [
        {'code': 'en', 'name': 'English'},
        {'code': 'hi', 'name': 'हिंदी (Hindi)'},
        {'code': 'mr', 'name': 'मराठी (Marathi)'},
        {'code': 'te', 'name': 'తెలుగు (Telugu)'},
        {'code': 'ta', 'name': 'தமிழ் (Tamil)'},
        {'code': 'bn', 'name': 'বাংলা (Bengali)'}
    ]
    
    return jsonify({
        'success': True,
        'languages': languages
    })

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """Translate text to different language"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        target_lang = data.get('target_lang', 'en')
        
        # Simple translation mapping (in production, use Google Translate API)
        translations = {
            'hi': {
                'tomato': 'टमाटर',
                'healthy': 'स्वस्थ',
                'disease': 'रोग',
                'remedy': 'उपचार'
            }
        }
        
        translated_text = translations.get(target_lang, {}).get(text.lower(), text)
        
        return jsonify({
            'success': True,
            'translated_text': translated_text,
            'original_text': text,
            'target_language': target_lang
        })
        
    except Exception as e:
        logger.error(f"Error translating text: {str(e)}")
        return jsonify({'error': 'Translation failed'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 