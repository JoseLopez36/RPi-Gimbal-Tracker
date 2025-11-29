import paho.mqtt.client as mqtt

class MQTTPublisher:
    def __init__(self, broker_address, topic):
        self.client = mqtt.Client()
        self.broker_address = broker_address
        self.topic = topic
        
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT Broker (Publisher) with result code {rc}")

    def connect(self):
        print(f"Connecting to MQTT Broker at {self.broker_address}...")
        self.client.connect(self.broker_address, 1883, 60)
        self.client.loop_start()

    def send_command(self, command):
        print(f"Publishing command: {command} to {self.topic}")
        self.client.publish(self.topic, command)

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

