from sense_hat import SenseHat

class SenseHatInterface:
    def __init__(self, config):
        self.config = config
        self.resolution = config['video']['resolution']
        if SenseHat:
            self.sense = SenseHat()
            self.sense.clear()
        else:
            self.sense = None
            print("Sense HAT not detected, running in mock mode.")

    def update_display(self, detections, active_target_id):
        """
        Map detections to 8x8 LED matrix.
        Red pixel = Active Target, White pixels = Other targets, Black pixels = Background.
        """
        if not self.sense:
            return

        self.sense.clear()
        
        W, H = self.resolution

        for d in detections:
            x1, y1, x2, y2 = d['box']
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            
            # Map to 0-7
            ix = int((cx / W) * 8)
            iy = int((cy / H) * 8)
            
            # Clamp to matrix boundaries
            ix = max(0, min(ix, 7))
            iy = max(0, min(iy, 7))
            
            if d.get('id') == active_target_id:
                color = (255, 0, 0) # Red
            else:
                color = (255, 255, 255) # White
            
            self.sense.set_pixel(ix, iy, color)

    def get_joystick_event(self):
        """
        Check for joystick input.
        """
        if not self.sense:
            return None
        
        # get_events returns a list of events since last call
        events = self.sense.stick.get_events()
        if events:
            # For simplicity, just return the first one
            return events[0]
        return None
