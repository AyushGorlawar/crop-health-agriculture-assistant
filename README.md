# 🌱 Crop Health & Agriculture Assistant

An AI-powered web application that helps farmers detect crop diseases, get remedies, and access market information.

## 🚀 Features

- **Crop Disease Detection**: Upload images to detect diseases using AI
- **Remedy Suggestions**: Get organic and chemical treatment solutions
- **Yield Improvement Tips**: Best practices for better crop production
- **Live Market Prices**: Real-time agricultural market data
- **Multi-language Support**: English, Hindi, and regional languages
- **Weather Forecast**: Local weather information for farming
- **Crop Calendar**: Sowing and harvesting guides

## 🛠️ Tech Stack

### Backend
- **Flask**: Python web framework for API
- **TensorFlow/Keras**: AI model for disease detection
- **SQLite/PostgreSQL**: Database for remedies and tips
- **OpenCV**: Image processing
- **Requests**: API integrations

### Frontend
- **HTML5/CSS3/JavaScript**: Responsive web interface
- **Bootstrap**: Mobile-friendly UI components
- **Chart.js**: Data visualization
- **i18next**: Internationalization

### APIs & Services
- **Agmarknet API**: Market prices
- **OpenWeatherMap API**: Weather data
- **Google Translate API**: Language translation

## 📁 Project Structure

```
crop-detection/
├── backend/
│   ├── app.py                 # Flask main application
│   ├── models/                # AI models for disease detection
│   ├── api/                   # API routes
│   ├── database/              # Database models and migrations
│   ├── utils/                 # Utility functions
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── index.html             # Main landing page
│   ├── css/                   # Stylesheets
│   ├── js/                    # JavaScript files
│   ├── images/                # Static images
│   └── locales/               # Translation files
├── models/                    # Pre-trained AI models
├── data/                      # Training data and datasets
└── docs/                      # Documentation
```

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
# Open index.html in browser or serve with any static server
python -m http.server 8000
```

## 🌐 Deployment

- **Backend**: Deploy to Render/Railway/Heroku
- **Frontend**: Host on GitHub Pages
- **Mobile App**: Convert using platforms like AppGyver/Bubble

## 📱 Mobile App Conversion

The web app can be converted to mobile using:
- **AppGyver**: No-code platform
- **Bubble**: Web to mobile conversion
- **PWA**: Progressive Web App features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- PlantVillage dataset for disease detection training
- Agmarknet for market price data
- OpenWeatherMap for weather information 