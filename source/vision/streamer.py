"""
Raspberry Pi TCP Video Streamer

Picamera2 streamer that sends H.264 over TCP to a connected client.
Based on https://github.com/raspberrypi/picamera2/blob/main/examples/capture_stream.py
"""

import time
import socket

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput

class Streamer:
    def __init__(
        self,
        host="0.0.0.0",
        port=10001,
        width=1280,
        height=720,
        bitrate=1000000,
    ):
        self.host = host
        self.port = port
        self.width = width
        self.height = height
        self.bitrate = bitrate

        self.picam2 = None
        self.encoder = None
        self.sock = None
        self.stream = None
        self.conn = None

    def start(self):
        if self.picam2 is not None:
            return

        self.picam2 = Picamera2()
        video_config = self.picam2.create_video_configuration(
            {"size": (self.width, self.height)}
        )
        self.picam2.configure(video_config)
        self.encoder = H264Encoder(self.bitrate)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.picam2.encoders = self.encoder
        self.conn, _ = self.sock.accept()
        self.stream = self.conn.makefile("wb")
        self.encoder.output = FileOutput(self.stream)

        self.picam2.start_encoder(self.encoder)
        self.picam2.start()
        time.sleep(20)

    def stop(self):
        if self.picam2 is not None:
            try:
                self.picam2.stop()
                self.picam2.stop_encoder()
            finally:
                self.picam2.close()
            self.picam2 = None

        if self.conn is not None:
            try:
                self.conn.close()
            finally:
                self.conn = None

        if self.stream is not None:
            try:
                self.stream.close()
            finally:
                self.stream = None

        if self.sock is not None:
            try:
                self.sock.close()
            finally:
                self.sock = None