# Smart First Aid Kit - Setup Guide (2GB Optimized)

## Hardware Assembly

See [hardware/assembly_guide.md](../hardware/assembly_guide.md) for detailed hardware assembly instructions.

## Software Installation for 2GB RAM

### Prerequisites

- Raspberry Pi 4 Model B (2GB RAM)
- Raspberry Pi OS Lite (bullseye or later) - recommended for 2GB
- Python 3.8 or higher
- pip package manager
- Git

### Step 1: Update System

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### Step 2: Install Python and Development Tools

```bash
sudo apt-get install -y python3-dev python3-pip python3-venv
sudo apt-get install -y build-essential cmake git
```

### Step 3: Enable Required Interfaces

Enable Camera and Display interfaces:

```bash
sudo raspi-config
```

- Interface Options → Camera → Enable
- Interface Options → I2C → Enable
- Interface Options → SPI → Enable
- Interface Options → Serial → Enable

### Step 4: Reduce Memory Usage (Important for 2GB)

```bash
# Disable GPU memory if not needed
sudo nano /boot/config.txt
# Add or modify:
# gpu_mem=64
# arm_freq=1600
# core_freq=400
```

### Step 5: Clone Repository

```bash
git clone https://github.com/elnemry844-lab/smart-first-aid-kit.git
cd smart-first-aid-kit
```

### Step 6: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 7: Install Dependencies (Lightweight)

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**Note**: Installation may take 10-15 minutes on 2GB RAM. Be patient.

### Step 8: Download Optimized AI Models

```bash
python models/model_download.py
```

Models will be quantized and lightweight:
- Wound Detection: ~3MB (YOLOv8n)
- Wound Classification: ~10MB (MobileNetV2)

### Step 9: Configuration

Create `config/local_settings.py` with your specific settings:

```python
# WiFi Configuration
NETWORK = {
    'wifi': {
        'enabled': True,
        'ssid': 'YOUR_SSID',
        'password': 'YOUR_PASSWORD',
    },
    'emergency_contact': {
        'phone_number': '+1234567890',
        'email': 'emergency@example.com',
    }
}

# Memory optimization for 2GB
APP = {
    'memory_limit_mb': 400,  # Conservative limit
}
```

## Running the Application

### Test Individual Components

```bash
# Test camera
python -m pytest tests/test_camera.py -v

# Test AI models (lightweight)
python -m pytest tests/test_ai.py -v

# Test audio system
python -m pytest tests/test_audio.py -v
```

### Start Full Application

```bash
python src/main.py
```

### Monitor Memory Usage

In another terminal:

```bash
watch -n 1 free -h
```

### Run in Background

```bash
nohup python src/main.py > logs/app.log 2>&1 &
```

## Auto-start on Boot

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/first-aid-kit.service
```

Add the following content:

```ini
[Unit]
Description=Smart First Aid Kit (2GB Optimized)
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/smart-first-aid-kit
ExecStart=/home/pi/smart-first-aid-kit/venv/bin/python src/main.py
Restart=on-failure
RestartSec=10
MemoryLimit=512M

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable first-aid-kit.service
sudo systemctl start first-aid-kit.service
```

Check status:

```bash
sudo systemctl status first-aid-kit.service
journalctl -u first-aid-kit.service -f
```

## Performance Optimization Tips for 2GB

1. **Use Raspberry Pi OS Lite** instead of full desktop
2. **Disable unnecessary services**:
   ```bash
   sudo systemctl disable bluetooth
   sudo systemctl disable avahi-daemon
   ```

3. **Swap optimization**:
   ```bash
   sudo nano /etc/dphys-swapfile
   # Change CONF_SWAPSIZE=100 (default) to CONF_SWAPSIZE=512
   sudo /etc/init.d/dphys-swapfile restart
   ```

4. **Monitor resources**:
   ```bash
   top
   ```

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

### Memory Issues

If you see "MemoryError" or "OOM Killer" messages:

1. Reduce frame resolution in `config/settings.py`
2. Decrease framerate
3. Enable more aggressive garbage collection
4. Reduce display refresh rate
