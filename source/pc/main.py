import time
import sys
import os

# Add project root to sys.path
sys.path.append(os.getcwd())

from source.pc.utils import load_config
from source.pc.mqtt_client import MQTTClient
from source.pc.video_receiver import VideoReceiver
from source.pc.yolo_detector import YOLODetector
from source.pc.display import Display

def main():
    print("Starting Remote PC Edge AI System...")
    
    config = load_config()
    if not config:
        return

    mqtt = MQTTClient(config)
    video = VideoReceiver(config)
    detector = YOLODetector(config)
    display = Display()

    ptz_state = {}

    def on_mqtt_message(topic, payload):
        nonlocal ptz_state
        if topic == config['mqtt']['topics']['ptz']:
            ptz_state = payload

    mqtt.set_callback(on_mqtt_message)

    try:
        mqtt.start()
        video.start()
        
        while True:
            frame = video.get_frame()
            if frame is not None:
                detections = detector.detect(frame)
                mqtt.publish_inference(detections)
                display.show(frame, ptz_state)
            
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        mqtt.stop()
        video.stop()
        display.close()

if __name__ == "__main__":
    main()
