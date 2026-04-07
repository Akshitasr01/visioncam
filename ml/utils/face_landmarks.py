"""
Shared face detection and facial landmark extraction.
Uses MediaPipe Tasks FaceLandmarker with automatic model download.
Provides landmarks for drowsiness (EAR/MAR) and distraction (head pose).
"""

import cv2
import numpy as np
import mediapipe as mp
import os
import urllib.request

from mediapipe.tasks.python.vision import face_landmarker as fl
from mediapipe.tasks.python.core import base_options as bo
from mediapipe.tasks.python.vision.core import vision_task_running_mode as running_mode

from ..config import INPUT_WIDTH, INPUT_HEIGHT


############################################
# Aspect Ratio Helpers
############################################

def mouth_aspect_ratio(mouth_pts):
    """
    Robust MAR using 6 mouth landmarks (distance-independent)
    Indices assumed: [61, 291, 14, 17, 78, 308]
    """

    if mouth_pts is None or len(mouth_pts) < 6:
        return 0.0

    # Points
    left = np.array(mouth_pts[0])    # 61
    right = np.array(mouth_pts[1])   # 291
    top = np.array(mouth_pts[2])     # 14 (upper inner lip)
    bottom = np.array(mouth_pts[3])  # 17 (lower inner lip)
    top_outer = np.array(mouth_pts[4])    # 78
    bottom_outer = np.array(mouth_pts[5]) # 308

    # Vertical mouth opening (average inner + outer)
    vertical_inner = np.linalg.norm(top - bottom)
    vertical_outer = np.linalg.norm(top_outer - bottom_outer)
    vertical = (vertical_inner + vertical_outer) / 2.0

    # Horizontal mouth width
    horizontal = np.linalg.norm(left - right)

    if horizontal == 0:
        return 0.0

    return vertical / horizontal



############################################3


# ✅ MODEL SETUP (AUTO DOWNLOAD)
############################################

MODEL_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "models"
)

MODEL_PATH = os.path.join(MODEL_DIR, "face_landmarker.task")


def download_model():
    """Download MediaPipe face model if missing."""
    if os.path.exists(MODEL_PATH):
        return

    os.makedirs(MODEL_DIR, exist_ok=True)

    print("Downloading MediaPipe face_landmarker model...")

    url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"

    urllib.request.urlretrieve(url, MODEL_PATH)

    print("Model downloaded successfully!")


download_model()


############################################
# ✅ CREATE FACE LANDMARKER (ONCE)
############################################

_landmarker = None


def get_landmarker():
    global _landmarker

    if _landmarker is not None:
        return _landmarker

    options = fl.FaceLandmarkerOptions(
        base_options=bo.BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=running_mode.VisionTaskRunningMode.IMAGE,
        num_faces=1,
    )

    _landmarker = fl.FaceLandmarker.create_from_options(options)

    print("MediaPipe FaceLandmarker Loaded")

    return _landmarker


############################################
# Landmark indices
############################################

LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
MOUTH_INDICES = [61, 291, 13, 14, 78, 308]


############################################
# MAIN DETECTION FUNCTION
############################################

def get_face_landmarks(frame: np.ndarray):
    """
    Run face detection + landmark extraction on a BGR frame.

    Returns:
        dict with:
          - face_detected
          - left_eye
          - right_eye
          - mouth
          - all_landmarks
    """

    resized = cv2.resize(frame, (INPUT_WIDTH, INPUT_HEIGHT))
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

    landmarker = get_landmarker()

    # Use mp.Image / mp.ImageFormat (compatible with MediaPipe 0.10.9+)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    result = landmarker.detect(mp_img)

    output = {
        "face_detected": False,
        "left_eye": None,
        "right_eye": None,
        "mouth": None,
        "all_landmarks": None,
    }

    if not result.face_landmarks:
        return output

    face = result.face_landmarks[0]

    all_pts = []

    for lm in face:
        x = lm.x * INPUT_WIDTH
        y = lm.y * INPUT_HEIGHT
        all_pts.append((float(x), float(y)))

    def pick(indices):
        return [all_pts[i] for i in indices]

    output["face_detected"] = True
    output["all_landmarks"] = all_pts
    output["left_eye"] = pick(LEFT_EYE_INDICES)
    output["right_eye"] = pick(RIGHT_EYE_INDICES)
    output["mouth"] = pick(MOUTH_INDICES)

    return output