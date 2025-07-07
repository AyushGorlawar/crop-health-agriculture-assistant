import cv2
import numpy as np
from PIL import Image
import io
import base64
from typing import Tuple, Optional

class ImageProcessor:
    def __init__(self):
        self.target_size = (224, 224)
        self.mean = [0.485, 0.456, 0.406]  # ImageNet mean
        self.std = [0.229, 0.224, 0.225]   # ImageNet std
    
    def preprocess_image(self, image: Image.Image) -> Optional[np.ndarray]:
        """Preprocess image for AI model input"""
        try:
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image
            image = image.resize(self.target_size)
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Normalize pixel values
            img_array = img_array.astype(np.float32) / 255.0
            
            # Apply ImageNet normalization
            img_array = (img_array - self.mean) / self.std
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def enhance_image(self, image: Image.Image) -> Image.Image:
        """Enhance image quality for better detection"""
        try:
            # Convert to numpy array
            img_array = np.array(image)
            
            # Apply histogram equalization for better contrast
            if len(img_array.shape) == 3:
                # Convert to LAB color space
                lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
                l, a, b = cv2.split(lab)
                
                # Apply CLAHE to L channel
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                l = clahe.apply(l)
                
                # Merge channels
                lab = cv2.merge([l, a, b])
                enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
            else:
                # Grayscale image
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                enhanced = clahe.apply(img_array)
            
            # Convert back to PIL Image
            enhanced_image = Image.fromarray(enhanced)
            
            return enhanced_image
            
        except Exception as e:
            print(f"Error enhancing image: {e}")
            return image
    
    def detect_plant_region(self, image: Image.Image) -> Tuple[Image.Image, Optional[Tuple[int, int, int, int]]]:
        """Detect and crop plant region from image"""
        try:
            # Convert to numpy array
            img_array = np.array(image)
            
            # Convert to HSV color space for plant detection
            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            
            # Define green color range for plants
            lower_green = np.array([35, 50, 50])
            upper_green = np.array([85, 255, 255])
            
            # Create mask for green regions
            mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Find the largest contour (assumed to be the main plant)
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Add some padding
                padding = 20
                x = max(0, x - padding)
                y = max(0, y - padding)
                w = min(img_array.shape[1] - x, w + 2 * padding)
                h = min(img_array.shape[0] - y, h + 2 * padding)
                
                # Crop the image
                cropped = img_array[y:y+h, x:x+w]
                cropped_image = Image.fromarray(cropped)
                
                return cropped_image, (x, y, w, h)
            
            # If no plant region detected, return original image
            return image, None
            
        except Exception as e:
            print(f"Error detecting plant region: {e}")
            return image, None
    
    def validate_image(self, image: Image.Image) -> Tuple[bool, str]:
        """Validate if image is suitable for disease detection"""
        try:
            # Check image size
            width, height = image.size
            if width < 100 or height < 100:
                return False, "Image too small. Please upload a larger image."
            
            # Check if image is too large
            if width > 4000 or height > 4000:
                return False, "Image too large. Please upload a smaller image."
            
            # Check if image has content (not blank)
            img_array = np.array(image)
            if img_array.std() < 10:
                return False, "Image appears to be blank or too uniform."
            
            # Check if image is too dark or too bright
            mean_brightness = img_array.mean()
            if mean_brightness < 30 or mean_brightness > 220:
                return False, "Image too dark or too bright. Please adjust lighting."
            
            return True, "Image is valid for analysis."
            
        except Exception as e:
            print(f"Error validating image: {e}")
            return False, "Error processing image."
    
    def image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string"""
        try:
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', quality=85)
            img_str = base64.b64encode(buffer.getvalue()).decode()
            return img_str
        except Exception as e:
            print(f"Error converting image to base64: {e}")
            return ""
    
    def base64_to_image(self, base64_str: str) -> Optional[Image.Image]:
        """Convert base64 string to PIL Image"""
        try:
            img_data = base64.b64decode(base64_str)
            image = Image.open(io.BytesIO(img_data))
            return image
        except Exception as e:
            print(f"Error converting base64 to image: {e}")
            return None
    
    def resize_image(self, image: Image.Image, max_size: Tuple[int, int] = (800, 800)) -> Image.Image:
        """Resize image while maintaining aspect ratio"""
        try:
            # Calculate new size maintaining aspect ratio
            width, height = image.size
            max_width, max_height = max_size
            
            if width <= max_width and height <= max_height:
                return image
            
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            return resized_image
            
        except Exception as e:
            print(f"Error resizing image: {e}")
            return image 