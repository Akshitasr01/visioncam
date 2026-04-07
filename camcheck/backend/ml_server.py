"""
FastAPI inference API for VisionCam ML backend.
POST /api/detect with image → drowsiness, distraction, phone_usage.
"""

import time
from datetime import datetime, timezone

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.config import INPUT_HEIGHT, INPUT_WIDTH
from backend.distraction_model import DistractionModel
from backend.drowsiness_model import DrowsinessModel
from backend.phone_usage_detection import PhoneUsageDetector
from backend.utils.face_landmarks import get_face_landmarks

app = FastAPI(title="VisionCam ML API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared stateful models (one face-landmark run per request, then drowsiness + distraction).
_drowsiness = DrowsinessModel()
_distraction = DistractionModel()
_phone = PhoneUsageDetector()


def _decode_image(raw: bytes) -> np.ndarray:
    buf = np.frombuffer(raw, dtype=np.uint8)
    img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid or unsupported image")
    return img


def _resize_if_needed(img: np.ndarray) -> np.ndarray:
    h, w = img.shape[:2]
    if (w, h) != (INPUT_WIDTH, INPUT_HEIGHT):
        return cv2.resize(img, (INPUT_WIDTH, INPUT_HEIGHT))
    return img


@app.get("/")
def root():
    return {"service": "VisionCam ML API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/detect")
async def detect(file: UploadFile = File(...)):
    """
    Run drowsiness, distraction, and phone-usage detection on one image.
    Upload as multipart form with key "file" (image file).
    """
    t0 = time.perf_counter()
    raw = await file.read()
    frame = _decode_image(raw)
    frame = _resize_if_needed(frame)

    landmarks = get_face_landmarks(frame)
    drowsiness = _drowsiness.process(frame, landmarks=landmarks)
    if drowsiness["yawn_detected"]:
        try:
            drowsiness["yawn_detected"] = confirm_yawn_with_openai(frame)
        except Exception:
            drowsiness["yawn_detected"] = False
    distraction = _distraction.process(frame, landmarks=landmarks)
    phone = _phone.process(frame)

    duration_ms = (time.perf_counter() - t0) * 1000
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    return {
        "drowsiness": {
            "drowsy": drowsiness["drowsy"],
            "eye_status": drowsiness["eye_status"],
            "blink_count": drowsiness["blink_count"],
            "yawn_detected": drowsiness["yawn_detected"],
            "ear": drowsiness["ear"],
            "mar": drowsiness["mar"],
        },
        "distraction": {
            "distracted": distraction["distracted"],
            "looking_away": distraction["looking_away"],
            "head_pose": distraction["head_pose"],
        },
        "phone_usage": {
            "phone_detected": phone["phone_detected"],
            "phone_usage": phone["phone_usage"],
            "confidence": phone["confidence"],
        },
        "duration_ms": round(duration_ms, 2),
        "timestamp": ts,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.ml_server:app", host="0.0.0.0", port=8000, reload=True)
