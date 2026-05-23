# Smart First Aid Kit - Solar Powered & AI Integrated

A revolutionary medical assistant system combining Raspberry Pi, artificial intelligence, and renewable energy to provide intelligent first aid diagnosis and treatment guidance.

## 🏥 Project Overview

This project creates an autonomous smart first aid kit that serves as your personal medical assistant with the following features:

### Core Features
- **🤖 AI-Powered Diagnosis**: Wound detection and classification using computer vision
- **🎤 Voice Assistant**: Speaker system for audio guidance and instructions
- **☀️ Solar Powered**: Renewable energy source for sustainable operation
- **📱 Display Screen**: Real-time diagnosis results and first aid instructions
- **🚨 Emergency Button**: Quick access to emergency services
- **📷 Camera System**: High-resolution wound imaging and analysis
- **🏥 Medical Database**: Comprehensive first aid knowledge base

## 📁 Project Structure

```
smart-first-aid-kit/
├── README.md
├── requirements.txt
├── config/
│   ├── settings.py
│   ├── hardware_config.json
│   └── ai_models_config.json
├── src/
│   ├── main.py
│   ├── camera/
│   │   ├── __init__.py
│   │   ├── capture.py
│   │   └── preprocessing.py
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── wound_detector.py
│   │   ├── wound_classifier.py
│   │   └── diagnosis_engine.py
│   ├── audio/
│   │   ├── __init__.py
│   │   ├── text_to_speech.py
│   │   └── audio_output.py
│   ├── display/
│   │   ├── __init__.py
│   │   ├── ui_manager.py
│   │   └── display_controller.py
│   ├── emergency/
│   │   ├── __init__.py
│   │   ├── button_handler.py
│   │   └── emergency_protocol.py
│   ├── power/
│   │   ├── __init__.py
│   │   ├── solar_monitor.py
│   │   └── battery_management.py
│   └── medical/
│       ├── __init__.py
│       ├── first_aid_database.py
│       └── treatment_recommendations.py
├── models/
│   ├── README.md
│   ├── wound_detection_model.pt
│   ├── wound_classification_model.pt
│   └── model_download.py
├── data/
│   ├── training_data/
│   ├── test_data/
│   └── medical_knowledge/
│       └── first_aid_protocols.json
├── tests/
│   ├── test_camera.py
│   ├── test_ai.py
│   ├── test_audio.py
│   ├── test_display.py
│   └── test_emergency.py
├── 3d_models/
│   ├── README.md
│   ├── enclosure/
│   ├── camera_mount/
│   ├── button_assembly/
│   └── solar_panel_mount/
├── hardware/
│   ├── README.md
│   ├── wiring_diagram.txt
│   ├── components_list.md
│   └── assembly_guide.md
├── docs/
│   ├── SETUP.md
│   ├── USER_GUIDE.md
│   ├── API.md
│   ├── TROUBLESHOOTING.md
│   └── ARCHITECTURE.md
└── .gitignore
```

## 🔧 Hardware Components (Optimized for 2GB RAM)

### Main Board
- **Raspberry Pi 4 Model B** (2GB RAM - resource optimized)

### Camera & Vision
- **Raspberry Pi Camera Module v2** or **Pi Camera 3** (High quality)
- Dedicated camera ribbon cable

### Display
- **5-inch or 7-inch Touchscreen Display** (320x240 or 800x480 resolution)
- HDMI/DSI connection cable

### Audio System
- **3.5mm Audio Jack Speaker** (low power)
- Optional **Microphone module** (for voice commands)

### Power Management
- **Solar Panel** (50W, 18V output)
- **MPPT Solar Charge Controller** (20A)
- **LiFePO4 Battery** (12V, 50Ah)
- **DC-DC Converter** (stabilize Pi power)
- **UPS Module** (backup power)

### Input/Control
- **Emergency Button** (large, red, momentary switch)
- **Button housing** (protective casing)
- **Relay module** (for button triggering)

### Environmental
- **Waterproof enclosure** (IP65 rating)
- **Thermal management** (passive cooling)
- **Gaskets and seals**

## 🚀 Key Features Implementation

### 1. AI Wound Detection & Classification (2GB Optimized)
- **Lightweight YOLOv8n** model for detection
- **MobileNet-based** classification for efficiency
- Real-time processing with quantized models
- Frame rate: 5-10 FPS on 2GB Pi

### 2. Medical Assistant
- First aid protocol database
- Natural language diagnosis explanation
- Step-by-step treatment recommendations
- Vital information display

### 3. Audio Guidance
- Text-to-speech system (pyttsx3)
- Pre-recorded common instructions
- Multi-language support
- Clear audio output

### 4. Emergency Protocol
- One-click emergency button activation
- Automatic contact with emergency services
- Location sharing capability
- Incident logging

### 5. Solar Power Management
- Real-time battery monitoring
- Solar panel efficiency tracking
- Adaptive power consumption
- Low-power mode activation

## 📋 Getting Started

### Prerequisites
- Raspberry Pi 4 (2GB RAM)
- Python 3.8+
- pip and virtual environment
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/elnemry844-lab/smart-first-aid-kit.git
   cd smart-first-aid-kit
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies (lightweight)**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download optimized AI models**
   ```bash
   python models/model_download.py
   ```

5. **Configure hardware**
   - Edit `config/hardware_config.json` with your specific setup
   - Edit `config/settings.py` for your location and preferences

6. **Run the application**
   ```bash
   python src/main.py
   ```

## 📚 Documentation

- [Setup Guide](docs/SETUP.md) - Detailed installation and configuration
- [User Guide](docs/USER_GUIDE.md) - How to use the smart first aid kit
- [API Documentation](docs/API.md) - Module and function reference
- [Architecture](docs/ARCHITECTURE.md) - System design and data flow
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [Hardware Setup](hardware/README.md) - Wiring and assembly instructions
- [3D Models](3d_models/README.md) - STL files and printing guidelines

## 🔬 AI Model Details (2GB Optimized)

### Wound Detection
- **Model**: YOLOv8n (Nano - lightweight)
- **Size**: ~3MB quantized
- **Inference Time**: 200-300ms per frame
- **Accuracy**: 85-90% on test dataset

### Wound Classification
- **Model**: MobileNetV2 or SqueezeNet
- **Size**: ~10MB quantized
- **Categories**: Minor cuts, deep wounds, burns, bruises, infections, etc.
- **Output**: Classification with confidence score

### Recommendation Engine
- **Based on**: Wound type, severity, and medical best practices
- **Output**: Structured first aid instructions

## 🧪 Testing

Run tests with:
```bash
pytest tests/
```

Individual module tests:
```bash
python -m pytest tests/test_camera.py
python -m pytest tests/test_ai.py
python -m pytest tests/test_audio.py
```

## 💡 System Architecture

```
┌────────────────────────────────────────────────────────┐
│                SMART FIRST AID KIT                     │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │ CAMERA     │  │ DISPLAY    │  │ SPEAKER    │   │
│  │ INPUT      │  │ OUTPUT     │  │ OUTPUT     │   │
│  └────┬───────┘  └─────┬──────┘  └─────┬──────┘   │
│       │                │               │          │
│       └────────────────┼───────────────┘          │
│                        │                          │
│  ┌──────────────────────▼──────────────────────┐  │
│  │     RASPBERRY PI 4 (2GB RAM)               │  │
│  │  ┌───────────────────────────────────────┐ │  │
│  │  │  AI PROCESSING ENGINE                 │ │  │
│  │  │  ├─ Wound Detection (YOLOv8n)        │ │  │
│  │  │  ├─ Wound Classification             │ │  │
│  │  │  └─ Diagnosis Generation             │ │  │
│  │  ├───────────────────────────────────────┤ │  │
│  │  │  FIRST AID DATABASE & PROTOCOLS      │ │  │
│  │  ├───────────────────────────────────────┤ │  │
│  │  │  EMERGENCY & ALERT SYSTEM            │ │  │
│  │  └───────────────────────────────────────┘ │  │
│  └──────────────┬────────────────┬────────────┘  │
│                 │                │               │
│  ┌──────────────▼────────┐  ┌────▼──────────┐   │
│  │ POWER MANAGEMENT      │  │ COMMUNICATION │   │
│  │ ├─ Solar Monitor      │  │ ├─ WiFi/BT    │   │
│  │ ├─ Battery Mgmt       │  │ ├─ Emergency  │   │
│  │ └─ Low Power Mode     │  │ └─ Logging    │   │
│  └───────────────────────┘  └───────────────┘   │
│                                                  │
└────────────────────────────────────────────────────┘
```

## 🌍 Environmental Impact

This project promotes:
- **Sustainable energy**: 100% solar-powered operation
- **Accessibility**: Affordable AI-powered medical assistance
- **Sustainability**: Designed for long-term outdoor use
- **Renewable focus**: Zero carbon operation

## 📝 License

MIT License - Feel free to use and modify for your needs

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- Review [Architecture Documentation](docs/ARCHITECTURE.md)

## 🙏 Acknowledgments

- YOLOv8 for object detection framework
- TensorFlow/PyTorch communities
- Raspberry Pi Foundation
- Medical first aid databases and protocols

---

**Made with ❤️ for accessible healthcare and sustainable technology**
