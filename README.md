# PiStream-DL-Offloading

**Subject:** Advanced Digital Systems And Applications  
**Master's Project**

## 📖 Project Overview

This project implements and analyzes a closed-loop control system using video streaming and Deep Learning (DL). The system captures 1080p video on a Raspberry Pi 4B, streams it to a high-performance PC for DL processing, and returns control signals back to the Pi via MQTT.

The core objective is to compare the performance metrics (latency, processing time) of running Deep Learning models on the embedded device (Edge) versus offloading the processing to a remote PC over Wi-Fi.


## 🛠 Hardware Components

* **Embedded Device:** Raspberry Pi 4 Model B.
    * See specifications.
* **Sensor:** Raspberry Pi Camera Module V2 (RaspiCam).
    * See documentation.
* **Processing Unit:** Laptop/PC for remote decoding and inference.


## ⚙️ Technologies

* **Video Streaming:** GStreamer (H.264 encoding at 1080p@30fps).
* **Communication:** MQTT Protocol (for control signals, e.g., topic `/control/move`).
* **Deep Learning:** Framework TBD (e.g., TensorFlow/PyTorch) for video analysis.
* **Network:** Wi-Fi.

## 🚀 Workflow Architecture

1.  **Capture & Encode:** The RaspiCam records video at 1080p@30fps. The RPi 4B uses hardware acceleration to encode the stream into H.264 using GStreamer.
2.  **Transmission:** The encoded video is streamed over Wi-Fi to the PC.
3.  **Decode & Process:** The PC receives the stream, decodes it, and applies a Deep Learning model to analyze the content.
4.  **Control Loop:** Based on the DL inference result, the PC publishes a control signal via MQTT.
5.  **Action:** The RPi receives the signal and performs a specific hardware action (e.g., activating a GPIO pin).

## 📊 Comparative Study

A major component of this project is the analysis of computational cost and network overhead. We will benchmark:

* **Scenario A (Remote):** Streaming + PC Inference + Network Latency.
* **Scenario B (Embedded):** Local Inference directly on the RPi 4B.

Metrics to be measured include Wi-Fi latencies and specific processing times on the RPi.

### Directory Structure
* **`rpi_edge/`**: Code to run on the Raspberry Pi (Video Capture, Encoding, GPIO Control).
* **`pc_server/`**: Code to run on the PC (Video Decoding, DL Inference, Control Logic).
* **`results/`**: Benchmark logs and data.
* **`models/`**: Deep Learning models.

### Prerequisites
* **Raspberry Pi:** GStreamer, Python 3, MQTT Client.
* **PC:** GStreamer, Python 3, Deep Learning Framework, MQTT Broker (e.g., Mosquitto).

### Setup

#### Raspberry Pi (Edge)
1. Navigate to `rpi_edge/`.
2. Follow the `README.md` inside for installation.

#### PC (Server)
1. Navigate to `pc_server/`.
2. Follow the `README.md` inside for installation.

## 📝 License
[Insert License Here]