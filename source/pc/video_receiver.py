import socket
import threading
import cv2
import numpy as np

class VideoReceiver:
    def __init__(self, config):
        self.host = config['video']['host']
        self.port = config['video']['port']
        self.running = False
        self.thread = None
        self.frame = None
        self.lock = threading.Lock()

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._receive_loop)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def get_frame(self):
        with self.lock:
            if self.frame is not None:
                return self.frame.copy()
            return None

    def _receive_loop(self):
        # Mock implementation
        # Real implementation would connect to TCP socket and decode H.264 stream
        # For now, we'll just generate a dummy image or try to connect
        print(f"Connecting to video stream at {self.host}:{self.port}")
        
        while self.running:
            # Placeholder: Generate a blank frame
            dummy_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
            cv2.putText(dummy_frame, "Waiting for Video Stream...", (50, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            with self.lock:
                self.frame = dummy_frame
            
            # Simulate framerate
            import time
            time.sleep(1/30)
