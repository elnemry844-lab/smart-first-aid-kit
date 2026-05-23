#!/usr/bin/env python3
"""
Main entry point for Smart First Aid Kit application (2GB Optimized)
"""

import sys
import logging
import gc
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from src.camera.capture import CameraManager
from src.ai.diagnosis_engine import DiagnosisEngine
from src.audio.audio_output import AudioSystem
from src.display.ui_manager import UIManager
from src.emergency.button_handler import EmergencyButtonHandler
from src.power.solar_monitor import PowerManager

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOGGING['level']),
    format=settings.LOGGING['format'],
    handlers=[
        logging.FileHandler(settings.LOGGING['file']),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SmartFirstAidKit:
    """
    Main application class for Smart First Aid Kit (2GB Optimized)
    """

    def __init__(self):
        """Initialize all system components"""
        logger.info(f"Initializing {settings.APP['name']} v{settings.APP['version']}")
        logger.info(f"Running on Raspberry Pi with {settings.RPI_MEMORY_GB}GB RAM")
        
        self.running = False
        self.components = {}
        self.frame_count = 0
        
        # Enable garbage collection optimization
        if settings.MEMORY_OPTIMIZATION['enable_garbage_collection']:
            gc.enable()
        
        # Initialize components
        self._initialize_components()
        logger.info("All components initialized successfully")

    def _initialize_components(self):
        """Initialize all system components with memory optimization"""
        try:
            # Power Management
            logger.info("Initializing Power Management...")
            self.components['power'] = PowerManager()
            
            # Camera System
            if settings.CAMERA['enabled']:
                logger.info("Initializing Camera...")
                self.components['camera'] = CameraManager()
            
            # AI Engine
            logger.info("Initializing AI Diagnosis Engine (lightweight models)...")
            self.components['ai'] = DiagnosisEngine()
            
            # Audio System
            if settings.AUDIO['enabled']:
                logger.info("Initializing Audio System...")
                self.components['audio'] = AudioSystem()
            
            # Display System
            if settings.DISPLAY['enabled']:
                logger.info("Initializing Display...")
                self.components['display'] = UIManager()
            
            # Emergency Button
            if settings.EMERGENCY_BUTTON['enabled']:
                logger.info("Initializing Emergency Button...")
                self.components['emergency'] = EmergencyButtonHandler(
                    on_press=self.emergency_activated
                )
        
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            raise

    def start(self):
        """Start the application"""
        logger.info("Starting Smart First Aid Kit...")
        self.running = True
        
        try:
            # Display startup message
            if 'display' in self.components:
                self.components['display'].show_startup_screen()
            
            # Play startup sound
            if 'audio' in self.components:
                self.components['audio'].play_startup_sound()
            
            logger.info("Smart First Aid Kit is ready")
            self.main_loop()
        
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
            self.stop()
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            self.stop()

    def main_loop(self):
        """Main application loop with memory optimization for 2GB"""
        logger.info("Entering main loop")
        
        while self.running:
            try:
                # Get camera frame
                if 'camera' in self.components:
                    frame = self.components['camera'].capture_frame()
                    
                    if frame is not None:
                        # Process with AI
                        diagnosis = self.components['ai'].analyze_wound(frame)
                        
                        # Display results
                        if 'display' in self.components:
                            self.components['display'].show_diagnosis(diagnosis)
                        
                        # Provide audio guidance
                        if 'audio' in self.components:
                            self.components['audio'].provide_guidance(diagnosis)
                        
                        logger.debug(f"Diagnosis: {diagnosis}")
                
                # Check power status
                if 'power' in self.components:
                    power_status = self.components['power'].get_status()
                    logger.debug(f"Power Status: {power_status}")
                
                # Periodic garbage collection for 2GB RAM
                self.frame_count += 1
                if self.frame_count % settings.MEMORY_OPTIMIZATION['gc_interval_frames'] == 0:
                    gc.collect()
                    logger.debug("Garbage collection executed")
            
            except Exception as e:
                logger.error(f"Error in main loop iteration: {e}")

    def emergency_activated(self):
        """Handle emergency button activation"""
        logger.warning("EMERGENCY BUTTON ACTIVATED")
        
        # Trigger emergency protocol
        if 'display' in self.components:
            self.components['display'].show_emergency_screen()
        
        if 'audio' in self.components:
            self.components['audio'].play_emergency_alert()
        
        # Send emergency signal
        if 'emergency' in self.components:
            self.components['emergency'].send_emergency_alert()

    def stop(self):
        """Stop the application and cleanup"""
        logger.info("Stopping Smart First Aid Kit...")
        self.running = False
        
        # Cleanup components
        for name, component in self.components.items():
            try:
                if hasattr(component, 'cleanup'):
                    component.cleanup()
                logger.info(f"Cleaned up {name}")
            except Exception as e:
                logger.error(f"Error cleaning up {name}: {e}")
        
        # Final garbage collection
        gc.collect()
        
        logger.info("Smart First Aid Kit stopped")
        sys.exit(0)


def main():
    """
    Main entry point
    """
    logger.info("="*60)
    logger.info(f"{settings.APP['name']} v{settings.APP['version']}")
    logger.info(f"Optimized for {settings.RPI_MEMORY_GB}GB Raspberry Pi")
    logger.info("="*60)
    
    app = SmartFirstAidKit()
    app.start()


if __name__ == '__main__':
    main()
