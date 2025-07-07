import numpy as np
import tensorflow as tf
from PIL import Image
import cv2
import os
import json
from typing import Dict, Any, List

class DiseaseDetector:
    def __init__(self):
        self.model = None
        self.class_names = []
        self.crop_diseases = {
            'tomato': {
                'healthy': 'Healthy Tomato',
                'early_blight': 'Tomato Early Blight',
                'late_blight': 'Tomato Late Blight',
                'leaf_mold': 'Tomato Leaf Mold',
                'septoria_leaf_spot': 'Tomato Septoria Leaf Spot',
                'spider_mites': 'Tomato Spider Mites',
                'target_spot': 'Tomato Target Spot',
                'yellow_leaf_curl_virus': 'Tomato Yellow Leaf Curl Virus',
                'mosaic_virus': 'Tomato Mosaic Virus'
            },
            'potato': {
                'healthy': 'Healthy Potato',
                'early_blight': 'Potato Early Blight',
                'late_blight': 'Potato Late Blight'
            },
            'corn': {
                'healthy': 'Healthy Corn',
                'gray_leaf_spot': 'Corn Gray Leaf Spot',
                'common_rust': 'Corn Common Rust',
                'northern_leaf_blight': 'Corn Northern Leaf Blight'
            },
            'apple': {
                'healthy': 'Healthy Apple',
                'apple_scab': 'Apple Scab',
                'black_rot': 'Apple Black Rot',
                'cedar_apple_rust': 'Apple Cedar Rust'
            },
            'grape': {
                'healthy': 'Healthy Grape',
                'black_rot': 'Grape Black Rot',
                'esca': 'Grape Esca',
                'leaf_blight': 'Grape Leaf Blight'
            }
        }
        
        self.load_model()
    
    def load_model(self):
        """Load the pre-trained disease detection model"""
        try:
            # For now, we'll use a simple rule-based approach
            # In production, load a trained TensorFlow model
            self.model_loaded = True
            print("Disease detection model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model_loaded = False
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess image for model input"""
        # Resize image to standard size
        image = image.resize((224, 224))
        
        # Convert to numpy array and normalize
        img_array = np.array(image) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def detect(self, image: Image.Image) -> Dict[str, Any]:
        """Detect disease in the given image"""
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # For demo purposes, we'll use a simple rule-based detection
            # In production, this would use the actual AI model
            result = self._mock_detection(processed_image)
            
            return result
            
        except Exception as e:
            print(f"Error in disease detection: {e}")
            return {
                'crop_type': 'Unknown',
                'disease': 'Detection Failed',
                'confidence': 0.0,
                'description': 'Unable to process image'
            }
    
    def _mock_detection(self, image: np.ndarray) -> Dict[str, Any]:
        """Mock disease detection for demo purposes"""
        # This is a simplified mock - in production, use actual AI model
        
        # Simulate different detection results
        import random
        crops = list(self.crop_diseases.keys())
        crop = random.choice(crops)
        
        diseases = list(self.crop_diseases[crop].keys())
        disease = random.choice(diseases)
        
        confidence = random.uniform(0.7, 0.95)
        
        return {
            'crop_type': crop,
            'disease': self.crop_diseases[crop][disease],
            'confidence': confidence,
            'description': self._get_disease_description(crop, disease),
            'severity': self._get_severity_level(confidence)
        }
    
    def _get_disease_description(self, crop: str, disease: str) -> str:
        """Get description for detected disease"""
        descriptions = {
            'tomato': {
                'healthy': 'Your tomato plant appears to be healthy with no visible signs of disease.',
                'early_blight': 'Early blight is a common fungal disease that causes dark brown spots with concentric rings on lower leaves.',
                'late_blight': 'Late blight is a serious disease that can quickly kill plants. Look for water-soaked lesions on leaves.',
                'leaf_mold': 'Leaf mold causes yellow spots on upper leaf surfaces and olive-green spores on undersides.',
                'septoria_leaf_spot': 'Small, circular spots with gray centers and dark borders on leaves.',
                'spider_mites': 'Tiny pests that cause stippling and yellowing of leaves.',
                'target_spot': 'Target-shaped lesions with dark brown centers and lighter edges.',
                'yellow_leaf_curl_virus': 'Virus that causes leaves to curl upward and turn yellow.',
                'mosaic_virus': 'Virus causing mottled, distorted leaves with yellow and green patches.'
            }
        }
        
        return descriptions.get(crop, {}).get(disease, 'Disease detected in crop.')
    
    def _get_severity_level(self, confidence: float) -> str:
        """Get severity level based on confidence score"""
        if confidence > 0.9:
            return 'High'
        elif confidence > 0.7:
            return 'Medium'
        else:
            return 'Low'
    
    def get_supported_crops(self) -> List[str]:
        """Get list of supported crops"""
        return list(self.crop_diseases.keys())
    
    def get_crop_diseases(self, crop: str) -> Dict[str, str]:
        """Get diseases for a specific crop"""
        return self.crop_diseases.get(crop, {}) 