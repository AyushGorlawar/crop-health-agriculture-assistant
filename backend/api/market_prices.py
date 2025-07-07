import requests
import json
from datetime import datetime, date
from typing import Dict, List, Any
import os

class MarketPriceAPI:
    def __init__(self):
        self.base_url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        self.api_key = os.environ.get('AGMARKNET_API_KEY', 'demo_key')
        
        # Fallback data for demo purposes
        self.fallback_data = {
            'tomato': [
                {'market': 'Mumbai APMC', 'price': 24.50, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Delhi Azadpur', 'price': 22.00, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Bangalore APMC', 'price': 26.75, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Chennai Koyambedu', 'price': 25.30, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Kolkata APMC', 'price': 23.80, 'unit': 'kg', 'date': '2024-01-15'}
            ],
            'potato': [
                {'market': 'Mumbai APMC', 'price': 12.50, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Delhi Azadpur', 'price': 10.75, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Bangalore APMC', 'price': 14.20, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Chennai Koyambedu', 'price': 13.90, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Kolkata APMC', 'price': 11.60, 'unit': 'kg', 'date': '2024-01-15'}
            ],
            'onion': [
                {'market': 'Mumbai APMC', 'price': 18.75, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Delhi Azadpur', 'price': 16.50, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Bangalore APMC', 'price': 20.30, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Chennai Koyambedu', 'price': 19.80, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Kolkata APMC', 'price': 17.40, 'unit': 'kg', 'date': '2024-01-15'}
            ],
            'brinjal': [
                {'market': 'Mumbai APMC', 'price': 15.20, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Delhi Azadpur', 'price': 13.80, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Bangalore APMC', 'price': 17.50, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Chennai Koyambedu', 'price': 16.90, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Kolkata APMC', 'price': 14.60, 'unit': 'kg', 'date': '2024-01-15'}
            ],
            'cauliflower': [
                {'market': 'Mumbai APMC', 'price': 8.50, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Delhi Azadpur', 'price': 7.25, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Bangalore APMC', 'price': 9.80, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Chennai Koyambedu', 'price': 9.40, 'unit': 'kg', 'date': '2024-01-15'},
                {'market': 'Kolkata APMC', 'price': 8.10, 'unit': 'kg', 'date': '2024-01-15'}
            ]
        }
    
    def get_prices(self, crop_name: str, market_name: str = 'all') -> Dict[str, Any]:
        """Get market prices for a specific crop"""
        try:
            # Try to fetch from real API first
            real_data = self._fetch_from_api(crop_name, market_name)
            if real_data:
                return {
                    'crop': crop_name,
                    'prices': real_data,
                    'source': 'Agmarknet API',
                    'last_updated': datetime.now().isoformat()
                }
            
            # Fallback to demo data
            return self._get_fallback_prices(crop_name, market_name)
            
        except Exception as e:
            print(f"Error fetching market prices: {e}")
            return self._get_fallback_prices(crop_name, market_name)
    
    def _fetch_from_api(self, crop_name: str, market_name: str) -> List[Dict]:
        """Fetch prices from Agmarknet API"""
        try:
            params = {
                'api-key': self.api_key,
                'format': 'json',
                'filters[commodity]': crop_name,
                'limit': 10
            }
            
            if market_name != 'all':
                params['filters[market]'] = market_name
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_api_response(data)
            
            return None
            
        except Exception as e:
            print(f"API fetch error: {e}")
            return None
    
    def _parse_api_response(self, data: Dict) -> List[Dict]:
        """Parse API response into standardized format"""
        try:
            records = data.get('records', [])
            parsed_data = []
            
            for record in records:
                parsed_data.append({
                    'market': record.get('market', 'Unknown'),
                    'price': float(record.get('modal_price', 0)),
                    'unit': record.get('unit', 'kg'),
                    'date': record.get('date', ''),
                    'commodity': record.get('commodity', ''),
                    'state': record.get('state', '')
                })
            
            return parsed_data
            
        except Exception as e:
            print(f"Error parsing API response: {e}")
            return []
    
    def _get_fallback_prices(self, crop_name: str, market_name: str) -> Dict[str, Any]:
        """Get fallback prices from demo data"""
        crop_data = self.fallback_data.get(crop_name.lower(), [])
        
        if market_name != 'all':
            crop_data = [price for price in crop_data if market_name.lower() in price['market'].lower()]
        
        return {
            'crop': crop_name,
            'prices': crop_data,
            'source': 'Demo Data',
            'last_updated': datetime.now().isoformat(),
            'note': 'Using demo data. Connect to Agmarknet API for real-time prices.'
        }
    
    def get_supported_crops(self) -> List[str]:
        """Get list of supported crops"""
        return list(self.fallback_data.keys())
    
    def get_markets(self) -> List[str]:
        """Get list of available markets"""
        markets = set()
        for crop_data in self.fallback_data.values():
            for price_data in crop_data:
                markets.add(price_data['market'])
        return list(markets)
    
    def get_price_trends(self, crop_name: str, days: int = 7) -> Dict[str, Any]:
        """Get price trends for a crop over specified days"""
        # This would typically fetch historical data
        # For demo, we'll generate some mock trends
        
        import random
        from datetime import timedelta
        
        trends = []
        base_price = self.fallback_data.get(crop_name.lower(), [{}])[0].get('price', 20)
        
        for i in range(days):
            date_obj = datetime.now() - timedelta(days=i)
            price = base_price + random.uniform(-2, 2)
            trends.append({
                'date': date_obj.strftime('%Y-%m-%d'),
                'price': round(price, 2),
                'change': round(random.uniform(-5, 5), 2)
            })
        
        return {
            'crop': crop_name,
            'trends': trends[::-1],  # Reverse to show oldest first
            'period': f'{days} days'
        } 