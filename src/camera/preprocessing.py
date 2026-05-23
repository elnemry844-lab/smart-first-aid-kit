#!/usr/bin/env python3
"""
Camera Preprocessing Module
Image enhancement and normalization for AI model input
"""

import logging
import numpy as np

try:
    import cv2
except ImportError:
    logging.warning("OpenCV not installed")

logger = logging.getLogger(__name__)


class ImagePreprocessor:
    """
    Image preprocessing for wound detection and classification
    """

    @staticmethod
    def normalize(image, target_dtype=np.float32):
        """
        Normalize image to 0-1 range
        """
        if image is None:
            return None
        return image.astype(target_dtype) / 255.0

    @staticmethod
    def denormalize(image):
        """
        Denormalize image from 0-1 to 0-255
        """
        if image is None:
            return None
        return (np.clip(image, 0, 1) * 255).astype(np.uint8)

    @staticmethod
    def resize(image, size):
        """
        Resize image to target size
        Args:
            image: Input image
            size: Target size (width, height)
        
        Returns:
            Resized image
        """
        if image is None:
            return None
        return cv2.resize(image, size, interpolation=cv2.INTER_LINEAR)

    @staticmethod
    def apply_clahe(image, clip_limit=2.0, tile_size=8):
        """
        Apply Contrast Limited Adaptive Histogram Equalization
        """
        if image is None:
            return None
        
        # Convert to LAB color space
        image_uint8 = (np.clip(image, 0, 1) * 255).astype(np.uint8)
        lab = cv2.cvtColor(image_uint8, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size, tile_size))
        l = clahe.apply(l)
        
        # Merge and convert back
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        return enhanced.astype(np.float32) / 255.0

    @staticmethod
    def apply_gaussian_blur(image, kernel_size=5):
        """
        Apply Gaussian blur for noise reduction
        """
        if image is None:
            return None
        
        image_uint8 = (np.clip(image, 0, 1) * 255).astype(np.uint8)
        blurred = cv2.GaussianBlur(image_uint8, (kernel_size, kernel_size), 0)
        
        return blurred.astype(np.float32) / 255.0

    @staticmethod
    def apply_bilateral_filter(image, d=9, sigma_color=75, sigma_space=75):
        """
        Apply bilateral filter for edge-preserving smoothing
        """
        if image is None:
            return None
        
        image_uint8 = (np.clip(image, 0, 1) * 255).astype(np.uint8)
        filtered = cv2.bilateralFilter(image_uint8, d, sigma_color, sigma_space)
        
        return filtered.astype(np.float32) / 255.0

    @staticmethod
    def preprocess_for_detection(image, target_size=(416, 416)):
        """
        Preprocess image for object detection (YOLO)
        Args:
            image: Input image (0-1 range, float32)
            target_size: Target size for model
        
        Returns:
            Preprocessed image
        """
        if image is None:
            return None
        
        # Resize
        resized = ImagePreprocessor.resize(image, target_size)
        
        # Apply CLAHE
        enhanced = ImagePreprocessor.apply_clahe(resized, clip_limit=2.0)
        
        # Normalize for model
        normalized = enhanced.astype(np.float32)
        
        return normalized

    @staticmethod
    def preprocess_for_classification(image, target_size=(224, 224)):
        """
        Preprocess image for classification (MobileNet)
        Args:
            image: Input image (0-1 range, float32)
            target_size: Target size for model
        
        Returns:
            Preprocessed image
        """
        if image is None:
            return None
        
        # Resize
        resized = ImagePreprocessor.resize(image, target_size)
        
        # Bilateral filter for smoothing
        smoothed = ImagePreprocessor.apply_bilateral_filter(resized)
        
        # Normalize
        normalized = smoothed.astype(np.float32)
        
        return normalized

    @staticmethod
    def extract_roi(image, bbox):
        """
        Extract Region of Interest from image
        Args:
            image: Input image
            bbox: Bounding box (x1, y1, x2, y2)
        
        Returns:
            ROI image
        """
        if image is None or bbox is None:
            return None
        
        x1, y1, x2, y2 = bbox
        return image[y1:y2, x1:x2]

    @staticmethod
    def pad_image(image, target_size, color=(128, 128, 128)):
        """
        Pad image to target size while maintaining aspect ratio
        """
        if image is None:
            return None
        
        h, w = image.shape[:2]
        target_h, target_w = target_size
        
        # Calculate scaling factor
        scale = min(target_w / w, target_h / h)
        new_h, new_w = int(h * scale), int(w * scale)
        
        # Resize
        resized = cv2.resize(image, (new_w, new_h))
        
        # Create padded image
        padded = np.full((target_h, target_w, 3), color, dtype=image.dtype)
        
        # Calculate padding
        pad_h = (target_h - new_h) // 2
        pad_w = (target_w - new_w) // 2
        
        # Place resized image in center
        padded[pad_h:pad_h+new_h, pad_w:pad_w+new_w] = resized
        
        return padded
