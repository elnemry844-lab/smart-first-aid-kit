#!/usr/bin/env python3
"""
Wound Detection Module
YOLOv8 nano model for lightweight wound detection on 2GB Raspberry Pi
"""

import logging
import numpy as np

try:
    from ultralytics import YOLO
import torch
except ImportError:
    logging.warning("Ultralytics YOLO not installed")

from config import settings

logger = logging.getLogger(__name__)


class WoundDetector:
    """
    Detect wounds in images using YOLOv8 nano model
    Optimized for 2GB Raspberry Pi
    """

    def __init__(self):
        """Initialize wound detector"""
        logger.info("Initializing Wound Detector (YOLOv8n)...")
        self.model = None
        self.device = settings.AI_MODELS['wound_detection']['device']
        self.confidence_threshold = settings.AI_MODELS['wound_detection']['confidence_threshold']
        
        self._load_model()
        logger.info("Wound Detector initialized successfully")

    def _load_model(self):
        """
        Load YOLOv8 nano model
        """
        try:
            model_path = settings.AI_MODELS['wound_detection']['model_path']
            
            # Load model
            self.model = YOLO(model_path)
            
            # Set to evaluation mode and device
            self.model.to(self.device)
            
            logger.info(f"Model loaded from {model_path}")
            logger.info(f"Using device: {self.device}")
        
        except Exception as e:
            logger.error(f"Failed to load wound detection model: {e}")
            raise

    def detect(self, image, confidence=None):
        """
        Detect wounds in image
        Args:
            image: Input image (numpy array, 0-255)
            confidence: Detection confidence threshold (optional)
        
        Returns:
            Dictionary with detection results
        """
        if self.model is None or image is None:
            return None
        
        try:
            if confidence is None:
                confidence = self.confidence_threshold
            
            # Run inference
            results = self.model(image, conf=confidence, verbose=False)
            
            # Parse results
            detections = []
            if len(results) > 0:
                result = results[0]
                
                for box in result.boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = box.conf[0].cpu().item()
                    
                    detection = {
                        'bbox': (int(x1), int(y1), int(x2), int(y2)),
                        'confidence': float(conf),
                        'area': int((x2 - x1) * (y2 - y1))
                    }
                    detections.append(detection)
            
            return {
                'detected': len(detections) > 0,
                'detections': detections,
                'count': len(detections)
            }
        
        except Exception as e:
            logger.error(f"Error in wound detection: {e}")
            return {'detected': False, 'detections': [], 'count': 0}

    def detect_and_extract(self, image):
        """
        Detect wounds and extract ROI
        Returns: List of wound ROIs
        """
        if image is None:
            return []
        
        try:
            detections = self.detect(image)
            
            if not detections['detected']:
                return []
            
            rois = []
            for det in detections['detections']:
                x1, y1, x2, y2 = det['bbox']
                roi = image[y1:y2, x1:x2]
                
                rois.append({
                    'image': roi,
                    'bbox': det['bbox'],
                    'confidence': det['confidence']
                })
            
            return rois
        
        except Exception as e:
            logger.error(f"Error extracting wound ROI: {e}")
            return []

    def filter_detections(self, detections, min_area=100, min_confidence=0.5):
        """
        Filter detections by area and confidence
        """
        filtered = []
        for det in detections:
            if det['area'] >= min_area and det['confidence'] >= min_confidence:
                filtered.append(det)
        
        return filtered

    def get_largest_detection(self, detections):
        """
        Get the largest detected wound
        """
        if not detections:
            return None
        
        return max(detections, key=lambda x: x['area'])

    def cleanup(self):
        """
        Cleanup model resources
        """
        try:
            if self.model is not None:
                del self.model
                logger.info("Wound detector cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
