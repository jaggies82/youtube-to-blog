from typing import Any, Dict, List
from pathlib import Path
from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
from .base_adapter import ExternalAPIAdapter
from ..utils.logger import Logger

class DetectedObject:
    def __init__(self, class_name: str, confidence: float, bbox: List[float]):
        self.class_name = class_name
        self.confidence = confidence
        self.bbox = bbox

class VisualInsights:
    def __init__(self, objects: List[DetectedObject], key_frames: List[Image.Image]):
        self.objects = objects
        self.key_frames = key_frames

class YOLOAdapter(ExternalAPIAdapter):
    """Adapter for YOLO-based object detection and video analysis."""

    def __init__(self):
        super().__init__("yolo")
        self.model = None
        self.logger = Logger()

    def authenticate(self) -> bool:
        """Initialize YOLO model."""
        try:
            model_path = self.config.get("model", "yolov8n.pt")
            self.model = YOLO(model_path)
            self._set_authenticated(True)
            return True
        except Exception as e:
            self.handle_error(e, "model initialization")
            return False

    def execute(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute YOLO analysis based on request type."""
        if not self.is_authenticated():
            if not self.authenticate():
                return {}

        operation = request_data.get("operation")
        if operation == "detect_objects":
            return self._detect_objects(request_data.get("image"))
        elif operation == "analyze_video":
            return self._analyze_video(request_data.get("video_path"))
        else:
            self.logger.error(f"Unsupported operation: {operation}")
            return {}

    def detect_objects(self, frame: Image.Image) -> List[DetectedObject]:
        """Detect objects in a single frame."""
        if not self.is_authenticated():
            if not self.authenticate():
                return []

        try:
            results = self.model(frame, conf=self.config.get("confidence_threshold", 0.5))
            detected_objects = []
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    class_id = int(box.cls[0])
                    class_name = result.names[class_id]
                    confidence = float(box.conf[0])
                    bbox = box.xyxy[0].tolist()
                    
                    detected_objects.append(
                        DetectedObject(class_name, confidence, bbox)
                    )
            
            return detected_objects
        except Exception as e:
            self.handle_error(e, "object detection")
            return []

    def analyze_video(self, video_path: str) -> VisualInsights:
        """Analyze video and extract key frames with detected objects."""
        if not self.is_authenticated():
            if not self.authenticate():
                return VisualInsights([], [])

        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError(f"Could not open video file: {video_path}")

            all_objects = []
            key_frames = []
            frame_count = 0
            sample_rate = 30  # Sample every 30th frame

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_count % sample_rate == 0:
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_pil = Image.fromarray(frame_rgb)
                    
                    # Detect objects in frame
                    objects = self.detect_objects(frame_pil)
                    if objects:
                        all_objects.extend(objects)
                        key_frames.append(frame_pil)

                frame_count += 1

            cap.release()
            return VisualInsights(all_objects, key_frames)
        except Exception as e:
            self.handle_error(e, "video analysis")
            return VisualInsights([], [])

    def _detect_objects(self, image: Image.Image) -> Dict[str, Any]:
        """Internal method to detect objects in an image."""
        objects = self.detect_objects(image)
        return {
            "objects": [
                {
                    "class": obj.class_name,
                    "confidence": obj.confidence,
                    "bbox": obj.bbox
                }
                for obj in objects
            ]
        }

    def _analyze_video(self, video_path: str) -> Dict[str, Any]:
        """Internal method to analyze a video."""
        insights = self.analyze_video(video_path)
        return {
            "objects": [
                {
                    "class": obj.class_name,
                    "confidence": obj.confidence,
                    "bbox": obj.bbox
                }
                for obj in insights.objects
            ],
            "key_frames_count": len(insights.key_frames)
        } 