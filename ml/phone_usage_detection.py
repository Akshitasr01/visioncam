"""
Phone usage detection via object detection (stub implementation).
Uses config thresholds; plug in a real detector (e.g. YOLO COCO 'cell phone') later.
"""

from .config import PHONE_CONFIDENCE_THRESHOLD, PHONE_CONSEC_FRAMES


def _stub_detect(_frame):
    """
    Stub: no model loaded. Always returns (False, 0.0).
    Replace with real detector (e.g. YOLO COCO class 'cell phone') when ready.
    """
    return False, 0.0


class PhoneUsageDetector:
    """Stateful phone-usage detector: consecutive-frame logic, config thresholds."""

    def __init__(self):
        self.consec_phone = 0

    def process(self, frame):
        """
        Process one BGR frame. Optional: resize to INPUT_WIDTH x INPUT_HEIGHT for detector.

        Returns:
            dict: phone_detected, phone_usage, confidence
        """
        out = {
            "phone_detected": False,
            "phone_usage": False,
            "confidence": 0.0,
        }

        detected, conf = _stub_detect(frame)
        out["phone_detected"] = detected and conf >= PHONE_CONFIDENCE_THRESHOLD
        out["confidence"] = float(conf)

        if out["phone_detected"]:
            self.consec_phone += 1
        else:
            self.consec_phone = 0

        out["phone_usage"] = self.consec_phone >= PHONE_CONSEC_FRAMES
        return out
