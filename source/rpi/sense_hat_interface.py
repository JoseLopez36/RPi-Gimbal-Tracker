# from sense_hat import SenseHat # Uncomment on actual RPi

class SenseHatInterface:
    def __init__(self):
        # self.sense = SenseHat()
        pass

    def update_display(self, detections, active_target_id):
        # Map detections to LED matrix
        pass

    def get_joystick_event(self):
        # Check for joystick input
        return None
