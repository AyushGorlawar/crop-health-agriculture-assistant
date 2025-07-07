import json
from typing import Dict, List, Any

class RemediesAPI:
    def __init__(self):
        # Comprehensive database of remedies and farming tips
        self.remedies_database = {
            'tomato': {
                'early_blight': {
                    'organic': [
                        'Remove and destroy infected leaves',
                        'Improve air circulation by spacing plants properly',
                        'Apply neem oil spray (2-3 tablespoons per gallon of water)',
                        'Use copper-based fungicides as preventive measure',
                        'Mulch around plants to prevent soil splash'
                    ],
                    'chemical': [
                        'Apply chlorothalonil (Bravo) at first sign of disease',
                        'Use mancozeb-based fungicides',
                        'Apply copper sulfate solution',
                        'Use systemic fungicides like azoxystrobin'
                    ],
                    'preventive': [
                        'Plant resistant varieties',
                        'Avoid overhead watering',
                        'Rotate crops every 3-4 years',
                        'Maintain proper plant spacing',
                        'Remove plant debris after harvest'
                    ]
                },
                'late_blight': {
                    'organic': [
                        'Remove infected plants immediately',
                        'Apply copper sulfate solution',
                        'Use baking soda spray (1 tablespoon per gallon)',
                        'Improve drainage and air circulation',
                        'Apply compost tea to boost plant immunity'
                    ],
                    'chemical': [
                        'Apply chlorothalonil immediately',
                        'Use metalaxyl-based fungicides',
                        'Apply copper hydroxide',
                        'Use systemic fungicides'
                    ],
                    'preventive': [
                        'Plant resistant varieties',
                        'Avoid overhead irrigation',
                        'Monitor weather conditions',
                        'Apply preventive fungicides before rain'
                    ]
                },
                'healthy': {
                    'maintenance': [
                        'Regular watering (1-2 inches per week)',
                        'Fertilize with balanced NPK (10-10-10)',
                        'Prune suckers regularly',
                        'Support plants with cages or stakes',
                        'Monitor for pests and diseases'
                    ]
                }
            },
            'potato': {
                'early_blight': {
                    'organic': [
                        'Remove infected leaves',
                        'Apply neem oil spray',
                        'Use copper-based fungicides',
                        'Improve soil drainage',
                        'Apply compost tea'
                    ],
                    'chemical': [
                        'Apply chlorothalonil',
                        'Use mancozeb fungicides',
                        'Apply copper sulfate'
                    ],
                    'preventive': [
                        'Plant certified disease-free seed',
                        'Rotate crops',
                        'Avoid overhead watering',
                        'Remove plant debris'
                    ]
                }
            }
        }
        
        self.yield_tips = {
            'tomato': {
                'soil_preparation': [
                    'Test soil pH (6.0-6.8 is ideal)',
                    'Add organic matter (compost, manure)',
                    'Ensure good drainage',
                    'Apply balanced fertilizer before planting'
                ],
                'planting': [
                    'Plant after last frost date',
                    'Space plants 2-3 feet apart',
                    'Plant deep (up to first true leaves)',
                    'Use supports or cages'
                ],
                'watering': [
                    'Water deeply 1-2 times per week',
                    'Avoid overhead watering',
                    'Water at base of plants',
                    'Mulch to retain moisture'
                ],
                'fertilization': [
                    'Apply balanced fertilizer at planting',
                    'Side-dress with nitrogen when fruits form',
                    'Use calcium nitrate to prevent blossom end rot',
                    'Apply foliar feed monthly'
                ],
                'pest_management': [
                    'Monitor for hornworms and aphids',
                    'Use neem oil for organic control',
                    'Plant marigolds as companion plants',
                    'Hand-pick large pests'
                ]
            },
            'potato': {
                'soil_preparation': [
                    'Loose, well-draining soil',
                    'pH 5.0-6.5',
                    'Add compost and aged manure',
                    'Remove rocks and debris'
                ],
                'planting': [
                    'Plant in early spring',
                    'Cut seed potatoes into pieces with 2-3 eyes',
                    'Plant 4-6 inches deep',
                    'Space 12-15 inches apart'
                ],
                'watering': [
                    'Keep soil consistently moist',
                    'Water deeply once per week',
                    'Reduce watering when plants flower',
                    'Stop watering 2 weeks before harvest'
                ],
                'fertilization': [
                    'Apply balanced fertilizer at planting',
                    'Side-dress when plants are 6 inches tall',
                    'Use high-potassium fertilizer for tuber development'
                ]
            }
        }
        
        self.crop_calendar = {
            'tomato': {
                'india': {
                    'sowing_time': {
                        'kharif': 'June-July',
                        'rabi': 'October-November',
                        'zaid': 'January-February'
                    },
                    'harvest_time': {
                        'kharif': 'September-October',
                        'rabi': 'January-March',
                        'zaid': 'April-May'
                    },
                    'growth_duration': '90-120 days',
                    'spacing': '60x45 cm',
                    'seed_rate': '400-500 g/ha'
                }
            },
            'potato': {
                'india': {
                    'sowing_time': {
                        'kharif': 'June-July',
                        'rabi': 'October-November'
                    },
                    'harvest_time': {
                        'kharif': 'September-October',
                        'rabi': 'January-March'
                    },
                    'growth_duration': '90-110 days',
                    'spacing': '60x20 cm',
                    'seed_rate': '2.5-3.0 tonnes/ha'
                }
            }
        }
    
    def get_remedies(self, disease: str, crop_type: str = '') -> Dict[str, Any]:
        """Get remedies for a specific disease"""
        try:
            # Find the crop type if not provided
            if not crop_type:
                crop_type = self._find_crop_by_disease(disease)
            
            if not crop_type or crop_type not in self.remedies_database:
                return {
                    'error': 'Crop not found in database',
                    'suggestions': [
                        'Ensure proper plant spacing for air circulation',
                        'Avoid overhead watering',
                        'Remove infected plant parts',
                        'Apply organic fungicides like neem oil',
                        'Consult local agricultural extension office'
                    ]
                }
            
            crop_remedies = self.remedies_database[crop_type]
            
            # Find the specific disease
            disease_key = self._find_disease_key(disease, crop_remedies)
            
            if not disease_key:
                return {
                    'error': 'Disease not found in database',
                    'general_tips': [
                        'Maintain good plant hygiene',
                        'Ensure proper spacing',
                        'Use disease-resistant varieties',
                        'Practice crop rotation',
                        'Monitor plants regularly'
                    ]
                }
            
            remedies = crop_remedies[disease_key]
            
            return {
                'crop': crop_type,
                'disease': disease,
                'remedies': remedies,
                'additional_tips': self._get_additional_tips(crop_type, disease_key)
            }
            
        except Exception as e:
            print(f"Error getting remedies: {e}")
            return {
                'error': 'Failed to fetch remedies',
                'general_advice': 'Contact local agricultural expert for specific treatment'
            }
    
    def get_yield_tips(self, crop_type: str) -> Dict[str, Any]:
        """Get yield improvement tips for a crop"""
        try:
            if crop_type not in self.yield_tips:
                return {
                    'error': 'Crop not found in database',
                    'general_tips': [
                        'Test soil before planting',
                        'Use quality seeds/seedlings',
                        'Maintain proper spacing',
                        'Water regularly and deeply',
                        'Fertilize appropriately',
                        'Control pests and diseases',
                        'Harvest at optimal time'
                    ]
                }
            
            tips = self.yield_tips[crop_type]
            
            return {
                'crop': crop_type,
                'tips': tips,
                'best_practices': self._get_best_practices(crop_type)
            }
            
        except Exception as e:
            print(f"Error getting yield tips: {e}")
            return {
                'error': 'Failed to fetch yield tips',
                'general_advice': 'Follow local agricultural recommendations'
            }
    
    def get_crop_calendar(self, crop_type: str, location: str = 'india') -> Dict[str, Any]:
        """Get crop calendar and sowing guide"""
        try:
            if crop_type not in self.crop_calendar:
                return {
                    'error': 'Crop calendar not available',
                    'general_guidelines': [
                        'Plant during appropriate season for your region',
                        'Consider local climate and rainfall patterns',
                        'Follow local agricultural calendar',
                        'Consult local extension office for specific dates'
                    ]
                }
            
            calendar = self.crop_calendar[crop_type]
            location_data = calendar.get(location, calendar.get('india', {}))
            
            return {
                'crop': crop_type,
                'location': location,
                'calendar': location_data,
                'seasonal_advice': self._get_seasonal_advice(crop_type, location)
            }
            
        except Exception as e:
            print(f"Error getting crop calendar: {e}")
            return {
                'error': 'Failed to fetch crop calendar',
                'general_advice': 'Follow local agricultural calendar'
            }
    
    def _find_crop_by_disease(self, disease: str) -> str:
        """Find crop type based on disease name"""
        disease_lower = disease.lower()
        
        for crop, diseases in self.remedies_database.items():
            for disease_key in diseases.keys():
                if disease_key in disease_lower or disease_lower in disease_key:
                    return crop
        
        return ''
    
    def _find_disease_key(self, disease: str, crop_remedies: Dict) -> str:
        """Find disease key in crop remedies"""
        disease_lower = disease.lower()
        
        for disease_key in crop_remedies.keys():
            if disease_key in disease_lower or disease_lower in disease_key:
                return disease_key
        
        return ''
    
    def _get_additional_tips(self, crop_type: str, disease: str) -> List[str]:
        """Get additional tips for disease management"""
        general_tips = [
            'Always follow safety precautions when using chemicals',
            'Test treatments on small area first',
            'Keep records of treatments applied',
            'Monitor effectiveness of treatments',
            'Consider integrated pest management (IPM) approach'
        ]
        
        return general_tips
    
    def _get_best_practices(self, crop_type: str) -> List[str]:
        """Get best practices for crop cultivation"""
        practices = [
            'Use certified seeds or healthy seedlings',
            'Practice crop rotation to prevent disease buildup',
            'Maintain soil health with organic matter',
            'Monitor plants regularly for early detection',
            'Use appropriate irrigation methods',
            'Harvest at optimal maturity for best quality'
        ]
        
        return practices
    
    def _get_seasonal_advice(self, crop_type: str, location: str) -> Dict[str, str]:
        """Get seasonal advice for crop cultivation"""
        advice = {
            'spring': 'Prepare soil and start early season crops',
            'summer': 'Monitor for pests and ensure adequate irrigation',
            'autumn': 'Harvest and prepare for winter crops',
            'winter': 'Plan for next season and maintain soil health'
        }
        
        return advice 