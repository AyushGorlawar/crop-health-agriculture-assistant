import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os

class WeatherAPI:
    def __init__(self):
        self.api_key = os.environ.get('OPENWEATHER_API_KEY', 'demo_key')
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
        # Fallback weather data for demo purposes
        self.fallback_data = {
            'Mumbai': {
                'current': {
                    'temp': 28.5,
                    'humidity': 75,
                    'description': 'Partly cloudy',
                    'icon': '02d'
                },
                'forecast': [
                    {'date': '2024-01-15', 'temp_max': 30, 'temp_min': 25, 'description': 'Sunny'},
                    {'date': '2024-01-16', 'temp_max': 29, 'temp_min': 24, 'description': 'Partly cloudy'},
                    {'date': '2024-01-17', 'temp_max': 31, 'temp_min': 26, 'description': 'Light rain'},
                    {'date': '2024-01-18', 'temp_max': 28, 'temp_min': 23, 'description': 'Cloudy'},
                    {'date': '2024-01-19', 'temp_max': 32, 'temp_min': 27, 'description': 'Sunny'}
                ]
            },
            'Delhi': {
                'current': {
                    'temp': 22.0,
                    'humidity': 45,
                    'description': 'Clear sky',
                    'icon': '01d'
                },
                'forecast': [
                    {'date': '2024-01-15', 'temp_max': 24, 'temp_min': 18, 'description': 'Clear sky'},
                    {'date': '2024-01-16', 'temp_max': 26, 'temp_min': 20, 'description': 'Sunny'},
                    {'date': '2024-01-17', 'temp_max': 25, 'temp_min': 19, 'description': 'Partly cloudy'},
                    {'date': '2024-01-18', 'temp_max': 23, 'temp_min': 17, 'description': 'Clear sky'},
                    {'date': '2024-01-19', 'temp_max': 27, 'temp_min': 21, 'description': 'Sunny'}
                ]
            },
            'Bangalore': {
                'current': {
                    'temp': 24.0,
                    'humidity': 65,
                    'description': 'Light rain',
                    'icon': '10d'
                },
                'forecast': [
                    {'date': '2024-01-15', 'temp_max': 26, 'temp_min': 20, 'description': 'Light rain'},
                    {'date': '2024-01-16', 'temp_max': 25, 'temp_min': 19, 'description': 'Cloudy'},
                    {'date': '2024-01-17', 'temp_max': 27, 'temp_min': 21, 'description': 'Partly cloudy'},
                    {'date': '2024-01-18', 'temp_max': 28, 'temp_min': 22, 'description': 'Sunny'},
                    {'date': '2024-01-19', 'temp_max': 26, 'temp_min': 20, 'description': 'Light rain'}
                ]
            }
        }
    
    def get_forecast(self, location: str, days: int = 5) -> Dict[str, Any]:
        """Get weather forecast for a location"""
        try:
            # Try to fetch from real API first
            real_data = self._fetch_from_api(location, days)
            if real_data:
                return {
                    'location': location,
                    'data': real_data,
                    'source': 'OpenWeatherMap API',
                    'last_updated': datetime.now().isoformat()
                }
            
            # Fallback to demo data
            return self._get_fallback_weather(location, days)
            
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return self._get_fallback_weather(location, days)
    
    def _fetch_from_api(self, location: str, days: int) -> Dict[str, Any]:
        """Fetch weather data from OpenWeatherMap API"""
        try:
            # Get current weather
            current_url = f"{self.base_url}/weather"
            current_params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            current_response = requests.get(current_url, params=current_params, timeout=10)
            
            if current_response.status_code != 200:
                return None
            
            current_data = current_response.json()
            
            # Get forecast
            forecast_url = f"{self.base_url}/forecast"
            forecast_params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            forecast_response = requests.get(forecast_url, params=forecast_params, timeout=10)
            
            if forecast_response.status_code != 200:
                return None
            
            forecast_data = forecast_response.json()
            
            return self._parse_weather_data(current_data, forecast_data, days)
            
        except Exception as e:
            print(f"Weather API fetch error: {e}")
            return None
    
    def _parse_weather_data(self, current_data: Dict, forecast_data: Dict, days: int) -> Dict[str, Any]:
        """Parse API response into standardized format"""
        try:
            # Parse current weather
            current = {
                'temp': current_data['main']['temp'],
                'humidity': current_data['main']['humidity'],
                'description': current_data['weather'][0]['description'],
                'icon': current_data['weather'][0]['icon'],
                'wind_speed': current_data['wind']['speed'],
                'pressure': current_data['main']['pressure']
            }
            
            # Parse forecast
            forecast = []
            daily_data = {}
            
            for item in forecast_data['list']:
                date_str = item['dt_txt'].split(' ')[0]
                if date_str not in daily_data:
                    daily_data[date_str] = {
                        'temp_max': item['main']['temp_max'],
                        'temp_min': item['main']['temp_min'],
                        'description': item['weather'][0]['description'],
                        'humidity': item['main']['humidity']
                    }
                else:
                    daily_data[date_str]['temp_max'] = max(daily_data[date_str]['temp_max'], item['main']['temp_max'])
                    daily_data[date_str]['temp_min'] = min(daily_data[date_str]['temp_min'], item['main']['temp_min'])
            
            # Convert to list format
            for date_str, data in list(daily_data.items())[:days]:
                forecast.append({
                    'date': date_str,
                    'temp_max': round(data['temp_max'], 1),
                    'temp_min': round(data['temp_min'], 1),
                    'description': data['description'],
                    'humidity': data['humidity']
                })
            
            return {
                'current': current,
                'forecast': forecast
            }
            
        except Exception as e:
            print(f"Error parsing weather data: {e}")
            return None
    
    def _get_fallback_weather(self, location: str, days: int) -> Dict[str, Any]:
        """Get fallback weather data"""
        location_data = self.fallback_data.get(location, self.fallback_data['Mumbai'])
        
        return {
            'location': location,
            'data': {
                'current': location_data['current'],
                'forecast': location_data['forecast'][:days]
            },
            'source': 'Demo Data',
            'last_updated': datetime.now().isoformat(),
            'note': 'Using demo data. Connect to OpenWeatherMap API for real-time weather.'
        }
    
    def get_farming_advice(self, location: str) -> Dict[str, Any]:
        """Get farming-specific weather advice"""
        weather_data = self.get_forecast(location)
        current = weather_data['data']['current']
        
        advice = {
            'location': location,
            'current_conditions': current,
            'farming_recommendations': []
        }
        
        # Temperature-based advice
        temp = current['temp']
        if temp < 10:
            advice['farming_recommendations'].append({
                'type': 'temperature',
                'message': 'Low temperature - protect sensitive crops with covers',
                'priority': 'high'
            })
        elif temp > 35:
            advice['farming_recommendations'].append({
                'type': 'temperature',
                'message': 'High temperature - increase irrigation frequency',
                'priority': 'high'
            })
        
        # Humidity-based advice
        humidity = current['humidity']
        if humidity > 80:
            advice['farming_recommendations'].append({
                'type': 'humidity',
                'message': 'High humidity - watch for fungal diseases, ensure good ventilation',
                'priority': 'medium'
            })
        elif humidity < 30:
            advice['farming_recommendations'].append({
                'type': 'humidity',
                'message': 'Low humidity - increase irrigation, consider mulching',
                'priority': 'medium'
            })
        
        # Weather description-based advice
        description = current['description'].lower()
        if 'rain' in description:
            advice['farming_recommendations'].append({
                'type': 'precipitation',
                'message': 'Rain expected - avoid spraying pesticides, check drainage',
                'priority': 'medium'
            })
        elif 'sunny' in description or 'clear' in description:
            advice['farming_recommendations'].append({
                'type': 'sunlight',
                'message': 'Clear weather - good for harvesting and drying crops',
                'priority': 'low'
            })
        
        return advice
    
    def get_supported_locations(self) -> List[str]:
        """Get list of supported locations"""
        return list(self.fallback_data.keys()) 