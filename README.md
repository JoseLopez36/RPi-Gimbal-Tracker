# RPi-Virtual-PTZ

**An Embedded Virtual Tracking System with Visual Radar Feedback.**

This project implements a smart surveillance system on a Raspberry Pi 4. It uses Computer Vision to detect humans and performs **Virtual Pan-Tilt-Zoom (e-PTZ)** by dynamically cropping the high-resolution camera stream. The Sense HAT is utilized as a "Visual Radar" to map targets and provides a physical interface to toggle focus between multiple subjects.

---

## 📋 Features

* **Virtual PTZ:** Simulates mechanical camera movement by digitally cropping and zooming into the Region of Interest (ROI) of the active target.
* **Multi-Target Tracking:** Detects multiple humans simultaneously using YOLO.
* **Visual Radar (Sense HAT):** Maps the relative position of detected targets onto the 8x8 LED Matrix (Red pixel = Active Target, White pixels = Other targets, Black pixels = Background).
* **Hardware Control:** Use the Sense HAT Joystick to cycle through detected people to change the PTZ focus target.
* **Low-Latency Streaming:** Outputs the processed, stabilized video stream over TCP (H.264).

## 🛠️ Hardware & Requirements

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
* **Software Stack:**
* Python 3.12+
* Ultralytics (YOLO)
  * [YOLO on Raspberry Pi Guide](https://docs.ultralytics.com/guides/raspberry-pi/#flash-raspberry-pi-os-to-raspberry-pi)

## ⚙️ Architecture

The system operates in three concurrent stages:

1. **Acquisition:** Captures wide-angle video via `libcamerasrc`.
2. **Processing:**
* Detect bounding boxes of humans.
* Map coordinates to the LED matrix.
* Listen for Joystick events to select the `target_id`.
3. **Output:**
* `videocrop`: Adjusts the view based on the selected target's centroid.
* `textoverlay`: displaying telemetry (Temp/FPS).

## 🚀 Installation

### Raspberry Pi Setup

1. **Clone the repository:**
```bash
git clone https://github.com/JoseLopez36/RPi-Virtual-PTZ.git
cd RPi-Virtual-PTZ
```

2. **Install system dependencies:**
```bash
sudo apt update
sudo apt install python3-picamera2
```

3. **Install Python requirements:**
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

The system uses `config/settings.json` for configuration. Edit this file to customize system parameters

## 🎮 Usage

### Raspberry Pi

Run the main application on the Raspberry Pi:

```bash
python3 source/main.py
```

### Stream Client

The stream is served as raw H.264 over TCP. Connect from a client on the same
network to the Raspberry Pi on port `10001`.

Example with `ffplay`:

```bash
ffplay -f h264 -fflags nobuffer -flags low_delay -probesize 50000 -analyzeduration 500000 tcp://raspberrypi.local:10001
```

### Controls (Sense HAT Joystick)

| Input | Action |
| --- | --- |
| **Left / Right** | Cycle between detected targets. |
| **Middle Click** | Set PTZ to wide-angle view (no zoom). |
| **Up / Down** | Adjust digital zoom level. |