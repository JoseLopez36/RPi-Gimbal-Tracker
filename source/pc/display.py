import cv2

class Display:
    def __init__(self):
        self.window_name = "RPi Virtual PTZ"

    def show(self, frame, ptz_data=None):
        if frame is None:
            return

        display_frame = frame.copy()
        
        # Draw PTZ info if available
        if ptz_data:
            x, y, w, h = ptz_data.get('x', 0), ptz_data.get('y', 0), ptz_data.get('w', 0), ptz_data.get('h', 0)
            cv2.rectangle(display_frame, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 0), 2)

        cv2.imshow(self.window_name, display_frame)
        cv2.waitKey(1)

    def close(self):
        cv2.destroyAllWindows()
