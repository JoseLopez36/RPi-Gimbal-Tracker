# PC Server Code

This directory contains the code to run on the Host PC.

## Responsibilities
1. Receive GStreamer video stream.
2. Decode video.
3. (Scenario A) Run Deep Learning inference.
4. Publish control signals via MQTT.

## Setup
1. **System Dependencies (Ubuntu/Debian):**
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 libgirepository1.0-dev libcairo2-dev \
       gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
       libgstreamer1.0-dev
   ```

2. **Python Dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Deep Learning Setup (TBD):**
   - Install TensorFlow or PyTorch depending on the model format used.
   - Example: `pip install tensorflow`

