#!/usr/bin/env python3
"""
Diagnosis Engine - Wound Analysis and Recommendation Generation
"""

import logging
import json
from pathlib import Path

from config import settings
from .wound_detector import WoundDetector
from .wound_classifier import WoundClassifier
from src.medical.first_aid_database import FirstAidDatabase

logger = logging.getLogger(__name__)


class DiagnosisEngine:
    """
    Complete wound analysis engine combining detection, classification,
    and recommendation generation
    """

    def __init__(self):
        """Initialize diagnosis engine"""
        logger.info("Initializing Diagnosis Engine...")
        
        self.detector = WoundDetector()
        self.classifier = WoundClassifier()
        self.medical_db = FirstAidDatabase()
        
        logger.info("Diagnosis Engine initialized successfully")

    def analyze_wound(self, image):
        """
        Complete wound analysis pipeline
        Args:
            image: Input image (numpy array)
        
        Returns:
            Comprehensive diagnosis result
        """
        diagnosis = {
            'status': 'processing',
            'timestamp': None,
            'wound_detected': False,
            'classification': None,
            'severity': None,
            'recommendations': [],
            'warnings': [],
            'seek_medical_help': False
        }
        
        try:
            import time
            diagnosis['timestamp'] = time.time()
            
            # Step 1: Detect wound
            logger.info("Step 1: Detecting wounds...")
            detection_result = self.detector.detect(image)
            
            if not detection_result['detected']:
                diagnosis['status'] = 'no_wound_detected'
                logger.info("No wound detected")
                return diagnosis
            
            diagnosis['wound_detected'] = True
            logger.info(f"Wound detected: {detection_result['count']} detection(s)")
            
            # Step 2: Extract and classify largest wound
            logger.info("Step 2: Extracting wound ROI...")
            largest_detection = self.detector.get_largest_detection(
                detection_result['detections']
            )
            
            if largest_detection is None:
                diagnosis['status'] = 'detection_error'
                return diagnosis
            
            # Extract ROI
            x1, y1, x2, y2 = largest_detection['bbox']
            wound_roi = image[y1:y2, x1:x2]
            
            # Step 3: Classify wound
            logger.info("Step 3: Classifying wound...")
            classification_result = self.classifier.classify(wound_roi)
            
            if classification_result is None:
                diagnosis['status'] = 'classification_error'
                return diagnosis
            
            diagnosis['classification'] = classification_result
            diagnosis['severity'] = classification_result['severity']
            
            logger.info(f"Wound classified as: {classification_result['primary_class']}")
            logger.info(f"Confidence: {classification_result['primary_confidence']:.2%}")
            
            # Step 4: Get medical recommendations
            logger.info("Step 4: Retrieving medical recommendations...")
            wound_type = classification_result['primary_class']
            severity = classification_result['severity']
            
            recommendations = self.medical_db.get_recommendations(
                wound_type=wound_type,
                severity=severity
            )
            
            diagnosis['recommendations'] = recommendations.get('steps', [])
            diagnosis['warnings'] = recommendations.get('warnings', [])
            diagnosis['seek_medical_help'] = recommendations.get('seek_medical_help', False)
            
            diagnosis['status'] = 'success'
            
            logger.info("Diagnosis complete")
            return diagnosis
        
        except Exception as e:
            logger.error(f"Error in diagnosis pipeline: {e}")
            diagnosis['status'] = 'error'
            diagnosis['error'] = str(e)
            return diagnosis

    def batch_analyze(self, images):
        """
        Analyze multiple images
        """
        results = []
        for i, image in enumerate(images):
            logger.info(f"Analyzing image {i+1}/{len(images)}")
            result = self.analyze_wound(image)
            results.append(result)
        
        return results

    def get_audio_guidance(self, diagnosis):
        """
        Generate audio guidance text from diagnosis
        """
        if diagnosis['status'] != 'success':
            return "Unable to analyze wound. Please try again."
        
        text = f"Wound detected. Type: {diagnosis['classification']['primary_class']}. "
        text += f"Severity: {diagnosis['severity']}. "
        
        text += "Recommended steps: "
        for i, step in enumerate(diagnosis['recommendations'][:3], 1):
            text += f"{i}. {step}. "
        
        if diagnosis['warnings']:
            text += "Warnings: "
            for warning in diagnosis['warnings']:
                text += f"{warning}. "
        
        if diagnosis['seek_medical_help']:
            text += "Please seek medical attention."
        
        return text

    def cleanup(self):
        """
        Cleanup resources
        """
        try:
            self.detector.cleanup()
            self.classifier.cleanup()
            logger.info("Diagnosis Engine cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
