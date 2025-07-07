# 🚀 Deployment Guide - Crop Health & Agriculture Assistant

This guide will help you deploy the Crop Health & Agriculture Assistant application to various platforms.

## 📋 Prerequisites

- Git installed on your system
- Python 3.9+ installed
- Node.js (optional, for local development)
- API keys for external services (optional)

## 🏗️ Project Structure

```
crop-detection/
├── backend/                 # Flask API backend
│   ├── app.py              # Main Flask application
│   ├── api/                # API modules
│   ├── utils/              # Utility functions
│   ├── requirements.txt    # Python dependencies
│   └── Procfile           # Heroku deployment
├── frontend/               # Web frontend
│   ├── index.html         # Main HTML file
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript modules
│   └── images/            # Static images
└── README.md              # Project documentation
```

## 🔧 Local Development Setup

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Flask application:**
   ```bash
   python app.py
   ```

   The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Serve the frontend:**
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js (if you have http-server installed)
   npx http-server -p 8000
   ```

   The frontend will be available at `http://localhost:8000`

## 🌐 Deployment Options

### Option 1: Render (Recommended for Backend)

1. **Create a Render account** at [render.com](https://render.com)

2. **Connect your GitHub repository**

3. **Create a new Web Service:**
   - **Name:** crop-health-backend
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Root Directory:** `backend`

4. **Set Environment Variables:**
   ```
   SECRET_KEY=your-secret-key-here
   OPENWEATHER_API_KEY=your-openweather-api-key
   AGMARKNET_API_KEY=your-agmarknet-api-key
   ```

5. **Deploy**

### Option 2: Railway (Alternative Backend)

1. **Create a Railway account** at [railway.app](https://railway.app)

2. **Connect your GitHub repository**

3. **Create a new service:**
   - Select your repository
   - Set root directory to `backend`
   - Railway will auto-detect Python

4. **Set Environment Variables** (same as Render)

5. **Deploy**

### Option 3: Heroku (Legacy Backend)

1. **Install Heroku CLI**

2. **Login to Heroku:**
   ```bash
   heroku login
   ```

3. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```

4. **Set environment variables:**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set OPENWEATHER_API_KEY=your-api-key
   heroku config:set AGMARKNET_API_KEY=your-api-key
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

## 📱 Frontend Deployment

### GitHub Pages (Recommended)

1. **Push your code to GitHub**

2. **Go to repository Settings > Pages**

3. **Set Source to GitHub Actions**

4. **Create `.github/workflows/deploy.yml`:**
   ```yaml
   name: Deploy to GitHub Pages
   
   on:
     push:
       branches: [ main ]
   
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v2
       
       - name: Deploy to GitHub Pages
         uses: peaceiris/actions-gh-pages@v3
         with:
           github_token: ${{ secrets.GITHUB_TOKEN }}
           publish_dir: ./frontend
   ```

5. **Update API URL in frontend:**
   - Edit `frontend/js/app.js`
   - Change `apiBaseUrl` to your deployed backend URL

### Netlify (Alternative)

1. **Create Netlify account** at [netlify.com](https://netlify.com)

2. **Connect your GitHub repository**

3. **Set build settings:**
   - **Build command:** (leave empty)
   - **Publish directory:** `frontend`

4. **Deploy**

## 🔗 Connecting Frontend to Backend

After deploying both frontend and backend:

1. **Update the API URL in frontend:**
   ```javascript
   // In frontend/js/app.js
   this.apiBaseUrl = 'https://your-backend-url.com/api';
   ```

2. **Enable CORS in backend** (already configured)

3. **Test the connection**

## 📊 Environment Variables

### Required Variables

```bash
SECRET_KEY=your-secret-key-here
```

### Optional Variables (for enhanced functionality)

```bash
OPENWEATHER_API_KEY=your-openweather-api-key
AGMARKNET_API_KEY=your-agmarknet-api-key
DATABASE_URL=your-database-url
```

## 🔒 Security Considerations

1. **Never commit API keys to version control**
2. **Use environment variables for sensitive data**
3. **Enable HTTPS in production**
4. **Set up proper CORS policies**
5. **Implement rate limiting for API endpoints**

## 📱 Mobile App Conversion

### Using AppGyver

1. **Create AppGyver account** at [appgyver.com](https://appgyver.com)

2. **Import your web app URL**

3. **Customize the mobile interface**

4. **Build and publish**

### Using Bubble

1. **Create Bubble account** at [bubble.io](https://bubble.io)

2. **Import your web application**

3. **Add mobile-specific features**

4. **Deploy as mobile app**

## 🧪 Testing

### Backend Testing

```bash
cd backend
python -m pytest tests/
```

### Frontend Testing

Open the deployed frontend and test all features:
- Image upload and disease detection
- Market price fetching
- Weather data display
- Farming tips retrieval

## 📈 Monitoring

### Backend Monitoring

- **Render/Railway:** Built-in monitoring
- **Heroku:** Heroku Metrics
- **Custom:** Add logging and monitoring tools

### Frontend Monitoring

- **Google Analytics:** Track user behavior
- **Sentry:** Error tracking
- **Custom:** Performance monitoring

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        python -m pytest

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to Render
      # Add your deployment steps here
```

## 🆘 Troubleshooting

### Common Issues

1. **CORS Errors:**
   - Ensure backend CORS is properly configured
   - Check frontend API URL

2. **API Key Issues:**
   - Verify environment variables are set
   - Check API key permissions

3. **Image Upload Failures:**
   - Check file size limits
   - Verify upload directory permissions

4. **Database Issues:**
   - Ensure database URL is correct
   - Check database connectivity

### Support

- Check the application logs
- Review error messages in browser console
- Test API endpoints individually
- Verify environment variables

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [Render Documentation](https://render.com/docs)
- [GitHub Pages Documentation](https://pages.github.com/)

## 🎉 Success!

Once deployed, your Crop Health & Agriculture Assistant will be available to farmers worldwide, helping them improve crop yields and manage diseases effectively. 