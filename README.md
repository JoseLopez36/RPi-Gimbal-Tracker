# RPi-Virtual-PTZ

**A Distributed Virtual Tracking System with Visual Radar Feedback.**

This project implements a smart surveillance system using a Raspberry Pi 4 and a remote PC. The RPi streams video from the Camera Module v2, which is consumed by a remote PC running YOLO for human detection (edge AI). The PC sends inference results to the RPi via MQTT, where PTZ calculations are performed. The RPi sends PTZ results back to the PC, which displays both the original video stream and the cropped PTZ view. The Sense HAT on the RPi serves as a "visual radar" to map targets and provides a physical interface to toggle focus between multiple subjects.

---

## 📋 Features

* **Distributed Edge AI:** YOLO inference runs on a remote PC, offloading computation from the Raspberry Pi.
* **Virtual PTZ:** Simulates mechanical camera movement by digitally cropping and zooming into the Region of Interest (ROI) of the active target.
* **MQTT Communication:** Real-time bidirectional communication between RPi and PC for inference results and PTZ commands.
* **Dual Video Display:** PC displays both the original 720p video stream and the cropped PTZ view simultaneously.
* **Visual Radar (Sense HAT):** Maps the relative position of detected targets onto the 8x8 LED Matrix (Red pixel = Active Target, White pixels = Other targets).
* **Hardware Control:** Use the Sense HAT Joystick to cycle through detected people to change the PTZ focus target.
* **Low-Latency Streaming:** RPi streams 720p video over TCP (H.264) to the remote PC.

## 🛠️ Hardware & Requirements

### Raspberry Pi 4
* **Platform:** Raspberry Pi 4 Model B.
  * [Product Page](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
  * [Specifications](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/)
  * [Getting Started Guide](https://www.raspberrypi.com/documentation/computers/getting-started.html)
* **Sensor:** Raspberry Pi Camera Module v2.
  * [Product Page](https://www.raspberrypi.com/products/camera-module-v2/)
  * [Documentation](https://www.raspberrypi.com/documentation/accessories/camera.html)
  * [Examples](https://github.com/raspberrypi/picamera2/tree/main/examples)
* **I/O:** Raspberry Pi Sense HAT.
  * [Product Page](https://www.raspberrypi.com/products/sense-hat/)
  * [Documentation](https://www.raspberrypi.com/documentation/accessories/sense-hat.html)

### Remote PC (Edge AI)
* **Platform:** PC or laptop capable of running YOLO inference in real-time.
* **Network:** Both RPi and PC must be on the same network for MQTT communication and video streaming.

### Software Stack
* **Raspberry Pi:**
  * Python 3.11.2
  * picamera2
  * paho-mqtt
  * mosquitto (for broker host)
* **Remote PC:**
  * Python 3.12+
  * Ultralytics (YOLO)
  * paho-mqtt
  * OpenCV (for video display)

## 🚀 Installation

### Raspberry Pi Setup

**1. Clone the repository:**
```bash
git clone https://github.com/JoseLopez36/RPi-Virtual-PTZ.git
cd RPi-Virtual-PTZ
```

**2. Install system dependencies:**
```bash
sudo apt update
sudo apt install python3-picamera2 mosquitto mosquitto-clients
```

**3. Configure Mosquitto broker:**

Enable Mosquitto:
```bash
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```
Open the configuration file:
```bash
sudo nano /etc/mosquitto/conf.d/default.conf
```
Paste the following lines:
```text
listener 1883
allow_anonymous true
```
Restart Mosquitto to apply changes:
```bash
sudo systemctl restart mosquitto
```

**4. Install Python requirements:**
```bash
pip install -r source/rpi/requirements.txt
```

### Remote PC Setup

**1. Clone the repository:**
```bash
git clone https://github.com/JoseLopez36/RPi-Virtual-PTZ.git
cd RPi-Virtual-PTZ
```

**2. Create and activate a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install Python requirements:**
```bash
pip install -r source/pc/requirements.txt
```

## ⚙️ Configuration

The system uses `config/settings.json` for configuration. Edit this file to customize system parameters.

## 🎮 Usage

### Raspberry Pi

Run the main application on the Raspberry Pi:

```bash
python3 source/rpi/main.py
```

### Remote PC

Run the edge AI application on the remote PC:

```bash
python3 source/pc/main.py
```

### MQTT Topics

The system uses the following MQTT topics (configurable in `config/settings.json`):
- **Inference Results:** `rpi-ptz/inference` (PC → RPi)
- **PTZ Commands:** `rpi-ptz/ptz` (RPi → PC)

### Controls (Sense HAT Joystick)

| Input | Action |
| --- | --- |
| **Left / Right** | Cycle between detected targets |
| **Middle Click** | Reset digital zoom level |
| **Up / Down** | Adjust digital zoom level |