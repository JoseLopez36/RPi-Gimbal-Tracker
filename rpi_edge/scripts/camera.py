import socket
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality

class VideoStreamer:
    def __init__(self):
        try:
            self.camera = Picamera2()
            # Configure for 1080p video
            self.video_config = self.camera.create_video_configuration(
                main={"size": (1920, 1080)},
                lores={"size": (640, 480)}
            )
            self.camera.configure(self.video_config)
            
            # Start the camera (but not recording/streaming yet)
            self.camera.start()
            print("Camera initialized and started")
        except Exception as e:
            print(f"Error initializing camera: {e}")
            self.camera = None

        self.socket = None
        self.connection = None

    def start_stream(self, host, port):
        """Starts streaming H.264 video to the specified host/port via TCP"""
        if not self.camera:
            print("Camera not initialized")
            return

        try:
            # Connect to the host/port
            print(f"Connecting to {host}:{port}...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.connection = self.socket.makefile('wb')
            
            # Create H264 Encoder (10Mbps)
            encoder = H264Encoder(bitrate=10000000)
            
            # Stream directly to the socket connection file object
            print("Starting recording to stream...")
            self.camera.start_recording(encoder, self.connection, quality=Quality.HIGH)
            
        except Exception as e:
            print(f"Failed to start stream: {e}")
            self.stop_stream()

    def stop_stream(self):
        """Stops the recording and closes the connection"""
        if self.camera:
            try:
                self.camera.stop_recording()
                print("Recording stopped")
            except Exception as e:
                print(f"Error stopping recording: {e}")

        if self.connection:
            try:
                self.connection.close()
                print("Connection closed")
            except Exception as e:
                print(f"Error closing connection: {e}")
            self.connection = None
            
        if self.socket:
            try:
                self.socket.close()
                print("Socket closed")
            except Exception as e:
                print(f"Error closing socket: {e}")
            self.socket = None
