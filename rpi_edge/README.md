# Raspberry Pi Edge Code

This directory contains the code to run on the Raspberry Pi 4B.

## Responsibilities
1. Capture video from Pi Camera.
2. Encode video to H.264 using GStreamer.
3. Stream video to PC.
4. Listen for MQTT control signals.
5. Execute hardware actions (GPIO).
6. (Scenario B) Run local inference.

## Setup
### 1. **System Dependencies:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 libgirepository1.0-dev libcairo2-dev python3-picamera2
   ```

### 2. Clone the Repository
   ```bash
   git clone https://github.com/josloprui6/RPi-Edge-vs-Local.git
   cd RPi-Edge-vs-Local
   ```

### 3. **Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 4. **Hardware Config:**
   - Ensure the Camera is enabled (`sudo raspi-config` -> Interface Options -> Camera).
   - Ensure GPIO access permissions are set (usually default for `pi` user).