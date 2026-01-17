"""
Virtual PTZ controller

Computes a ScalerCrop rectangle to digitally pan/tilt/zoom around a target
"""

class VirtualPTZ:
    def __init__(
        self,
        full_width: int,
        full_height: int,
        width: int,
        height: int,
        min_zoom: float,
        max_zoom: float
    ):
        self.full_width = full_width
        self.full_height = full_height
        self.width = width
        self.height = height
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
    
    def get_crop_from_yolo_result(self, result, track_id=None, zoom_factor=None):
        """
        Extract crop coordinates from a YOLO Results object.
        
        Args:
            result: YOLO Results object from tracker
            track_id: Optional specific track ID to focus on. If None, uses first detected target
            zoom_factor: Optional zoom factor. If None, auto-calculates based on target size
        
        Returns:
            tuple: (x, y, width, height) crop coordinates and size
        """
        if result is None or len(result.boxes) == 0:
            return None
        
        # Get boxes data
        boxes = result.boxes
        
        # If track_id is specified, find that specific track
        if track_id is not None:
            if hasattr(boxes, 'id') and boxes.id is not None:
                track_ids = boxes.id.cpu().numpy()
                matching_indices = [i for i, tid in enumerate(track_ids) if tid == track_id]
                if not matching_indices:
                    return None
                box_idx = matching_indices[0]
            else:
                return None
        else:
            # Use first detected target
            box_idx = 0
        
        # Get bounding box coordinates (xyxy format: [x1, y1, x2, y2])
        if hasattr(boxes, 'xyxy'):
            box_coords = boxes.xyxy[box_idx].cpu().numpy()
        elif hasattr(boxes, 'xywh'):
            # Convert xywh to xyxy if needed
            xywh = boxes.xywh[box_idx].cpu().numpy()
            x, y, w, h = xywh
            box_coords = [x - w/2, y - h/2, x + w/2, y + h/2]
        else:
            return None
        
        return self.get_crop(box_coords, zoom_factor)

    def get_crop(self, target_box, zoom_factor=None):
        """
        Calculate crop coordinates and size for a selected target
        
        Args:
            target_box: Bounding box in format [x1, y1, x2, y2] (pixel coordinates)
            zoom_factor: Optional zoom factor. If None, auto-calculates based on target size
        
        Returns:
            tuple: (x, y, width, height) crop coordinates and size in full frame coordinates
        """
        if target_box is None or len(target_box) < 4:
            return None
        
        x1, y1, x2, y2 = target_box[:4]
        
        # Validate bounding box
        if x2 <= x1 or y2 <= y1:
            return None
        
        # Calculate target center and size
        target_center_x = (x1 + x2) / 2.0
        target_center_y = (y1 + y2) / 2.0
        target_width = x2 - x1
        target_height = y2 - y1
        
        # Calculate zoom factor if not provided
        if zoom_factor is None:
            # Auto-calculate zoom to fit target with some padding
            # Use the larger dimension to determine zoom
            scale_x = self.width / target_width if target_width > 0 else 1.0
            scale_y = self.height / target_height if target_height > 0 else 1.0
            # Use a smaller scale to ensure target fits in crop
            zoom_factor = min(scale_x, scale_y) * 0.8  # 0.8 provides padding
        
        # Clamp zoom factor to valid range
        zoom_factor = max(self.min_zoom, min(self.max_zoom, zoom_factor))
        
        # Calculate crop size in full frame coordinates
        crop_width = self.width / zoom_factor
        crop_height = self.height / zoom_factor
        
        # Center crop on target
        crop_x = target_center_x - crop_width / 2.0
        crop_y = target_center_y - crop_height / 2.0
        
        # Clamp crop to stay within full frame bounds
        crop_x = max(0, min(crop_x, self.full_width - crop_width))
        crop_y = max(0, min(crop_y, self.full_height - crop_height))
        
        # Ensure crop doesn't exceed frame bounds
        if crop_x + crop_width > self.full_width:
            crop_width = self.full_width - crop_x
        if crop_y + crop_height > self.full_height:
            crop_height = self.full_height - crop_y
        
        # Return as integers (pixel coordinates)
        return (
            int(crop_x),
            int(crop_y),
            int(crop_width),
            int(crop_height)
        )