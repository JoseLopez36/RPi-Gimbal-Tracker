class VirtualPTZ:
    def __init__(self, config):
        self.config = config
        self.resolution = config['video']['resolution']  # [W, H]
        self.current_zoom = 1.0
        self.target_id = None
        self.last_detections = []
        self.max_zoom = 6.0
        self.zoom_step = 0.2
        self.manual_zoom_active = False
        self.last_auto_zoom = 1.0

    def update(self, detections):
        """Calculate PTZ based on detections and current target"""
        self.last_detections = detections
        W, H = self.resolution

        # Human-like aspect ratio (vertical)
        # target_ratio = width / height
        target_ratio = 9 / 16
        
        # Default: centered view based on current zoom
        target_center_x, target_center_y = W / 2, H / 2
        
        # Determine target to track
        target = None
        active_target_id = self.target_id

        # Automatic target acquisition (if no target manually selected)
        if self.target_id is None:
             # Find target with lowest ID
             valid_detections = [d for d in detections if 'id' in d]
             if valid_detections:
                 target = min(valid_detections, key=lambda x: x['id'])
                 active_target_id = target['id']
        elif self.target_id is not None:
             # Try to find manual target
             target = next((d for d in detections if d.get('id') == self.target_id), None)
        
        # Calculate Zoom
        calculated_zoom = 1.0
        
        if target:
            # Use target's bounding box center
            x1, y1, x2, y2 = target['box']
            target_center_x = (x1 + x2) / 2
            target_center_y = (y1 + y2) / 2
            
            # Automatic digital zoom level
            target_h = y2 - y1
            if target_h > 0:
                # Aim for target to be 80% of screen height
                wanted_crop_h = target_h * 1.25
                auto_zoom = H / wanted_crop_h
                calculated_zoom = max(1.0, min(auto_zoom, self.max_zoom))
        
        self.last_auto_zoom = calculated_zoom

        # Determine effective zoom
        if self.manual_zoom_active:
            effective_zoom = self.current_zoom
        else:
            effective_zoom = calculated_zoom

        # Calculate crop dimensions using the human-like aspect ratio
        # We base the size on the height and the current zoom
        crop_h = H / effective_zoom
        crop_w = crop_h * target_ratio

        # Ensure crop is within frame boundaries
        if crop_h > H:
            crop_h = H
            crop_w = crop_h * target_ratio

        # Calculate top-left corner
        crop_x = target_center_x - crop_w / 2
        crop_y = target_center_y - crop_h / 2

        # Clamp to frame boundaries
        crop_x = max(0, min(crop_x, W - crop_w))
        crop_y = max(0, min(crop_y, H - crop_h))

        return {
            "x": int(crop_x),
            "y": int(crop_y),
            "w": int(crop_w),
            "h": int(crop_h),
            "zoom": effective_zoom,
            "target_id": active_target_id
        }

    def set_target(self, target_id):
        self.target_id = target_id

    def handle_input(self, event):
        """Handle joystick events from Sense HAT"""
        # event is expected to have 'direction' and 'action'
        if event.action in ['pressed', 'held']:
            if event.direction == 'up':
                # Tweak manual zoom -> start with automatic zoom
                if not self.manual_zoom_active:
                    self.current_zoom = self.last_auto_zoom
                    self.manual_zoom_active = True
                self.current_zoom = min(self.max_zoom, self.current_zoom + self.zoom_step)
            elif event.direction == 'down':
                # Tweak manual zoom
                if not self.manual_zoom_active:
                    self.current_zoom = self.last_auto_zoom
                    self.manual_zoom_active = True
                self.current_zoom = max(1.0, self.current_zoom - self.zoom_step)
            elif event.direction == 'middle':
                self.current_zoom = 1.0
                self.manual_zoom_active = False
                self.target_id = None
            elif event.direction == 'left':
                self._cycle_target(reverse=True)
            elif event.direction == 'right':
                self._cycle_target(reverse=False)

    def _cycle_target(self, reverse=False):
        """Cycle through available target IDs from last detections"""
        if not self.last_detections:
            self.target_id = None
            return

        # Get all unique IDs from detections
        ids = sorted(list(set(d['id'] for d in self.last_detections if 'id' in d)))
        
        if not ids:
            self.target_id = None
            return

        if self.target_id is None:
            self.target_id = ids[0]
        else:
            try:
                current_idx = ids.index(self.target_id)
                if reverse:
                    new_idx = (current_idx - 1) % len(ids)
                else:
                    new_idx = (current_idx + 1) % len(ids)
                self.target_id = ids[new_idx]
            except ValueError:
                # Current target_id not in latest detections
                self.target_id = ids[0]
