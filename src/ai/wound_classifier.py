#!/usr/bin/env python3
"""
Wound Classification Module
MobileNetV2-based lightweight wound type classifier
"""

import logging
import numpy as np

try:
    import torch
    import torch.nn as nn
    from torchvision import models
except ImportError:
    logging.warning("PyTorch not installed")

from config import settings

logger = logging.getLogger(__name__)


class WoundClassifier:
    """
    Classify wound types using lightweight MobileNetV2 model
    Optimized for 2GB Raspberry Pi
    """

    def __init__(self):
        """Initialize wound classifier"""
        logger.info("Initializing Wound Classifier (MobileNetV2)...")
        self.model = None
        self.device = settings.AI_MODELS['wound_classification']['device']
        self.confidence_threshold = settings.AI_MODELS['wound_classification']['confidence_threshold']
        self.classes = settings.WOUND_CLASSES
        
        self._load_model()
        logger.info("Wound Classifier initialized successfully")

    def _load_model(self):
        """
        Load MobileNetV2 model for wound classification
        """
        try:
            # Load pre-trained MobileNetV2
            self.model = models.mobilenet_v2(pretrained=True)
            
            # Modify final layer for wound classes
            num_classes = len(self.classes)
            self.model.classifier[1] = nn.Linear(self.model.last_channel, num_classes)
            
            # Load fine-tuned weights if available
            model_path = settings.AI_MODELS['wound_classification']['model_path']
            try:
                state_dict = torch.load(model_path, map_location=self.device)
                self.model.load_state_dict(state_dict)
                logger.info(f"Loaded model from {model_path}")
            except:
                logger.warning(f"Using default MobileNetV2 weights (fine-tuned model not found at {model_path})")
            
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"Model loaded on device: {self.device}")
        
        except Exception as e:
            logger.error(f"Failed to load wound classification model: {e}")
            raise

    def classify(self, image, return_top_k=3):
        """
        Classify wound type in image
        Args:
            image: Input image (numpy array, 0-1 float32)
            return_top_k: Number of top predictions to return
        
        Returns:
            Dictionary with classification results
        """
        if self.model is None or image is None:
            return None
        
        try:
            # Prepare image
            if len(image.shape) == 2:  # Grayscale
                image = np.stack([image] * 3, axis=2)
            
            # Convert to tensor
            image_tensor = torch.from_numpy(image).permute(2, 0, 1).unsqueeze(0)
            image_tensor = image_tensor.to(self.device).float()
            
            # Inference
            with torch.no_grad():
                outputs = self.model(image_tensor)
            
            # Get probabilities
            probs = torch.nn.functional.softmax(outputs, dim=1)[0]
            
            # Get top predictions
            top_probs, top_indices = torch.topk(probs, k=min(return_top_k, len(self.classes)))
            
            predictions = []
            for prob, idx in zip(top_probs, top_indices):
                class_name = self.classes[idx.item()]
                confidence = prob.item()
                
                predictions.append({
                    'class': class_name,
                    'confidence': float(confidence),
                    'index': int(idx.item())
                })
            
            return {
                'primary_class': predictions[0]['class'],
                'primary_confidence': predictions[0]['confidence'],
                'predictions': predictions,
                'severity': self._assess_severity(predictions[0]['class'])
            }
        
        except Exception as e:
            logger.error(f"Error in wound classification: {e}")
            return None

    def _assess_severity(self, wound_class):
        """
        Assess severity based on wound class
        Returns: 'minor', 'moderate', 'severe'
        """
        severity_map = {
            'minor_cut': 'minor',
            'abrasion': 'minor',
            'bruise': 'minor',
            'burn_first_degree': 'minor',
            'laceration': 'moderate',
            'deep_wound': 'moderate',
            'burn_second_degree': 'moderate',
            'burn_third_degree': 'severe',
            'infection': 'severe',
        }
        
        return severity_map.get(wound_class, 'unknown')

    def batch_classify(self, images):
        """
        Classify multiple images
        Returns: List of classification results
        """
        results = []
        for image in images:
            result = self.classify(image)
            if result is not None:
                results.append(result)
        
        return results

    def cleanup(self):
        """
        Cleanup model resources
        """
        try:
            if self.model is not None:
                del self.model
                logger.info("Wound classifier cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
