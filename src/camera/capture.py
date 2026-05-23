#!/usr/bin/env python3
"""
Camera Module - Image Capture and Preprocessing
Optimized for 2GB Raspberry Pi
"""

import logging
import threading
import time
from pathlib import Path
from collections import deque

try:
    import cv2
    import numpy as np
    from picamera2 import Picamera2
except ImportError as e:
    logging.warning(f"Camera dependencies not fully installed: {e}")

from config import settings

logger = logging.getLogger(__name__)


class CameraManager:
    """
    Manages camera capture and frame preprocessing
    Optimized for 2GB RAM with minimal buffering
    """

    def __init__(self):
        """Initialize camera manager"""
        self.camera = None
        self.running = False
        self.frame_buffer = deque(maxlen=settings.CAMERA['buffer_size'])
        self.lock = threading.Lock()
        
        logger.info("Initializing camera...")
        self._initialize_camera()
        logger.info("Camera initialized successfully")

    def _initialize_camera(self):
        """
        Initialize the camera with configured settings
        """
        try:
            # Try libcamera first (Raspberry Pi OS bullseye+)
            if settings.CAMERA['module'] == 'libcamera':
                self.camera = Picamera2()
                
                # Configure camera
                config = self.camera.create_preview_configuration(
                    main={"format": "RGB888", "size": settings.CAMERA['resolution']},
                    raw={"size": self.camera.sensor_resolution}
                )
                
                self.camera.configure(config)
                self.camera.start()
                
                logger.info(f"Initialized libcamera with resolution {settings.CAMERA['resolution']}")
            else:
                logger.error("Legacy picamera module not supported. Use Raspberry Pi OS bullseye+")
                raise Exception("Camera initialization failed")
        
        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            raise

    def capture_frame(self):
        """
        Capture a single frame from camera
        Returns: numpy array or None if capture fails
        """
        try:
            if self.camera is None:
                return None
            
            # Capture frame
            request = self.camera.capture_request()
            array = request.make_array("main")
            request.release()
            
            # Convert RGB to BGR for OpenCV compatibility
            frame_bgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
            
            # Store in buffer
            with self.lock:
                self.frame_buffer.append(frame_bgr.copy())
            
            return frame_bgr
        
        except Exception as e:
            logger.error(f"Error capturing frame: {e}")
            return None

    def get_latest_frame(self):
        """
        Get the latest frame from buffer
        Returns: numpy array or None
        """
        with self.lock:
            if len(self.frame_buffer) > 0:
                return self.frame_buffer[-1]
            return None

    def preprocess_frame(self, frame):
        """
        Preprocess frame for AI model
        - Normalize
        - Resize if needed
        - Enhance contrast
        
        Args:
            frame: Input frame (numpy array)
        
        Returns:
            Preprocessed frame
        """
        if frame is None:
            return None
        
        try:
            # Normalize to 0-1 range
            normalized = frame.astype(np.float32) / 255.0
            
            # Enhance contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
            lab = cv2.cvtColor((normalized * 255).astype(np.uint8), cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            
            enhanced = cv2.merge([l, a, b])
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
            
            return enhanced.astype(np.float32) / 255.0
        
        except Exception as e:
            logger.error(f"Error preprocessing frame: {e}")
            return None

    def adjust_brightness(self, frame, value):
        """
        Adjust frame brightness
        Args:
            frame: Input frame
            value: Brightness adjustment (-50 to 50)
        
        Returns:
            Adjusted frame
        """
        if frame is None:
            return None
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] + value, 0, 255)
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    def get_frame_info(self, frame):
        """
        Get information about current frame
        Returns: Dict with frame metadata
        """
        if frame is None:
            return None
        
        return {
            'shape': frame.shape,
            'dtype': str(frame.dtype),
            'min': float(np.min(frame)),
            'max': float(np.max(frame)),
            'mean': float(np.mean(frame))
        }

    def save_frame(self, frame, filename=None):
        """
        Save frame to disk for debugging
        Args:
            frame: Frame to save
            filename: Output filename (optional)
        
        Returns:
            Path to saved file or None
        """
        if frame is None:
            return None
        
        try:
            if filename is None:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"frame_{timestamp}.jpg"
            
            save_path = Path(settings.APP['image_save_path']) / filename
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            cv2.imwrite(str(save_path), frame)
            logger.debug(f"Frame saved to {save_path}")
            
            return save_path
        
        except Exception as e:
            logger.error(f"Error saving frame: {e}")
            return None

    def cleanup(self):
        """
        Cleanup camera resources
        """
        try:
            if self.camera is not None:
                self.camera.stop()
                self.camera.close()
                logger.info("Camera cleanup completed")
        except Exception as e:
            logger.error(f"Error during camera cleanup: {e}")
