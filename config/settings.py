"""
Global settings and configuration for Smart First Aid Kit (2GB RAM Optimized)
"""

import os
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / 'src'
MODELS_DIR = BASE_DIR / 'models'
DATA_DIR = BASE_DIR / 'data'
LOGS_DIR = BASE_DIR / 'logs'
CONFIG_DIR = BASE_DIR / 'config'

# Create logs directory if it doesn't exist
LOGS_DIR.mkdir(exist_ok=True)

# ============================================================================
# RASPBERRY PI CONFIGURATION (2GB OPTIMIZED)
# ============================================================================
RPI_GPIO_MODE = 'BCM'  # BCM or BOARD
RPI_MEMORY_GB = 2  # RAM available
RPI_CPU_CORES = 4  # Number of cores
RPI_CPU_GOVERNOR = 'powersave'  # CPU frequency scaling

# ============================================================================
# CAMERA CONFIGURATION (Optimized for 2GB)
# ============================================================================
CAMERA = {
    'enabled': True,
    'module': 'libcamera',  # 'legacy_picamera' or 'libcamera'
    'resolution': (1280, 720),  # Lower resolution for 2GB RAM
    'framerate': 10,  # Reduced FPS to save processing
    'rotation': 0,  # degrees: 0, 90, 180, 270
    'hflip': False,
    'vflip': False,
    'brightness': 50,
    'contrast': 0,
    'saturation': 0,
    'buffer_size': 2,  # Minimal buffering
}

# ============================================================================
# AI MODEL CONFIGURATION (Lightweight for 2GB)
# ============================================================================
AI_MODELS = {
    'wound_detection': {
        'model_name': 'yolov8n',  # NANO model - ~3MB
        'model_path': str(MODELS_DIR / 'wound_detection_model.pt'),
        'confidence_threshold': 0.5,
        'device': 'cpu',  # CPU only for 2GB RAM
        'quantized': True,  # Use quantized model
        'half_precision': False,  # Disable for 2GB
    },
    'wound_classification': {
        'model_name': 'mobilenet_v2',  # Lightweight model
        'model_path': str(MODELS_DIR / 'wound_classification_model.pt'),
        'confidence_threshold': 0.6,
        'device': 'cpu',
        'quantized': True,
    }
}

WOUND_CLASSES = [
    'minor_cut',
    'deep_wound',
    'burn_first_degree',
    'burn_second_degree',
    'bruise',
    'abrasion',
    'laceration',
    'infection',
]

# ============================================================================
# DISPLAY CONFIGURATION (Lower Resolution for 2GB)
# ============================================================================
DISPLAY = {
    'enabled': True,
    'type': 'touchscreen',  # 'touchscreen' or 'hdmi'
    'resolution': (800, 480),  # 5-inch or 7-inch display
    'rotation': 0,
    'refresh_rate': 30,  # Reduced refresh for memory savings
    'brightness': 80,
    'timeout_seconds': 0,  # 0 = no timeout
}

# ============================================================================
# AUDIO CONFIGURATION
# ============================================================================
AUDIO = {
    'enabled': True,
    'speaker': {
        'device_index': 0,
        'volume': 0.8,  # 0.0 - 1.0
        'sample_rate': 44100,
    },
    'microphone': {
        'enabled': False,  # Disable to save resources
        'device_index': 0,
        'sample_rate': 44100,
    },
    'text_to_speech': {
        'engine': 'pyttsx3',  # Lightweight TTS
        'language': 'en',
        'rate': 150,  # words per minute
        'voice_id': 0,  # 0=male, 1=female
    }
}

# ============================================================================
# EMERGENCY BUTTON CONFIGURATION
# ============================================================================
EMERGENCY_BUTTON = {
    'enabled': True,
    'gpio_pin': 17,  # BCM pin
    'active_high': True,
    'debounce_ms': 50,
    'long_press_duration_seconds': 3,
}

# ============================================================================
# POWER MANAGEMENT CONFIGURATION
# ============================================================================
POWER = {
    'solar_panel': {
        'enabled': True,
        'voltage_input': 18,  # Volts
        'current_max': 5,  # Amps (smaller panel for 2GB)
        'power_max': 90,  # Watts
    },
    'battery': {
        'type': 'lifepo4',  # 'lifepo4' or 'lead-acid'
        'voltage': 12,  # Volts
        'capacity': 50,  # Amp-hours (smaller battery)
        'low_threshold': 25,  # % of capacity
        'critical_threshold': 10,  # % of capacity
    },
    'monitoring': {
        'enabled': True,
        'check_interval_seconds': 120,  # Less frequent checks
        'log_data': True,
    },
    'optimization': {
        'low_power_mode': True,
        'low_power_threshold': 40,  # % battery - more aggressive
        'cpu_governor': 'powersave',  # Always powersave for 2GB
    }
}

# ============================================================================
# MEDICAL DATABASE CONFIGURATION
# ============================================================================
MEDICAL_DB = {
    'database_path': str(DATA_DIR / 'medical_knowledge' / 'first_aid_protocols.json'),
    'update_check_interval_days': 7,
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOGGING = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': str(LOGS_DIR / 'smart_first_aid_kit.log'),
    'max_bytes': 5242880,  # 5MB (smaller for 2GB)
    'backup_count': 3,  # Fewer backups
}

# ============================================================================
# NETWORK CONFIGURATION
# ============================================================================
NETWORK = {
    'wifi': {
        'enabled': True,
        'ssid': None,  # Set in local_settings.py
        'password': None,  # Set in local_settings.py
    },
    'emergency_contact': {
        'enabled': True,
        'method': 'sms',  # 'sms', 'call', 'email'
        'phone_number': None,  # Set in local_settings.py
        'email': None,  # Set in local_settings.py
    },
    'gps': {
        'enabled': True,  # For location sharing
        'module': 'internal',  # 'internal' or 'gps_hat'
    }
}

# ============================================================================
# APPLICATION BEHAVIOR (2GB Optimized)
# ============================================================================
APP = {
    'name': 'Smart First Aid Kit',
    'version': '1.0.0',
    'debug': False,
    'auto_start': True,
    'startup_delay_seconds': 3,
    'max_processing_time_seconds': 15,  # Longer processing time for 2GB
    'image_save': True,
    'image_save_path': str(DATA_DIR / 'captured_images'),
    'memory_limit_mb': 512,  # Max memory for AI processing
}

# ============================================================================
# MEMORY OPTIMIZATION FLAGS
# ============================================================================
MEMORY_OPTIMIZATION = {
    'enable_garbage_collection': True,
    'gc_interval_frames': 30,  # Run GC every N frames
    'cache_models': True,  # Keep models in memory
    'limit_image_buffer': True,
    'max_buffer_size_mb': 100,
}

# ============================================================================
# Load local settings if available
# ============================================================================
try:
    from .local_settings import *
except ImportError:
    pass
