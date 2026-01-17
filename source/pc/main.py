import cv2

from yolo_tracker import YOLOTracker
from mqtt_client import MQTTClient
from utils import load_config

def main():
    print("Starting remote PC edge AI system...")
    
    config = load_config()
    if not config:
        return

    # Initialize video capture
    source = f"tcp://raspberrypi.local:{config['video']['port']}"

    tracker = YOLOTracker(config)
    mqtt = MQTTClient(config)

    ptz_state = {}

    def on_mqtt_message(topic, payload):
        nonlocal ptz_state
        if topic == config['mqtt']['topics']['ptz']:
            ptz_state = payload

    mqtt.set_callback(on_mqtt_message)

    try:
        results = tracker.start(source)
        mqtt.start()
        
        for result in results:
            # Publish the inference results to MQTT
            mqtt.publish_inference(result)

            # Display the frame in a single window named 'YOLO Inference'
            cv2.imshow("YOLO Inference", result.plot())

            # Display Virtual PTZ View if state is available from RPi
            if ptz_state:
                try:
                    x, y, w, h = ptz_state.get('x'), ptz_state.get('y'), ptz_state.get('w'), ptz_state.get('h')
                    if all(v is not None for v in [x, y, w, h]):
                        frame = result.orig_img
                        H, W = frame.shape[:2]
                        
                        # Calculate coordinates and ensure they are within frame boundaries
                        x1, y1 = max(0, int(x)), max(0, int(y))
                        x2, y2 = min(W, int(x + w)), min(H, int(y + h))
                        
                        if x2 > x1 and y2 > y1:
                            crop = frame[y1:y2, x1:x2]
                            # Resize crop back to original resolution for display
                            cv2.imshow("Virtual PTZ View", cv2.resize(crop, (W, H)))
                except Exception as e:
                    print(f"Error displaying PTZ crop: {e}")

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        mqtt.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
