"""
Shared face detection and facial landmark extraction.
Uses MediaPipe Face Mesh; provides landmarks for drowsiness (EAR/MAR) and distraction (head pose).
"""

import cv2
import numpy as np
import mediapipe as mp

from backend.config import INPUT_WIDTH, INPUT_HEIGHT

mp_face_mesh = mp.solutions.face_mesh


# MediaPipe Face Mesh indices for EAR (left eye, right eye) and MAR (mouth).
# Left eye: 33, 160, 158, 133, 153, 144 | Right eye: 362, 385, 387, 263, 373, 380
LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
# Mouth: 61, 291, 0, 17, 78, 308 (top/bottom lip, corners)
MOUTH_INDICES = [61, 291, 0, 17, 78, 308]


def _get_face_mesh():
    static_image_mode = False
    max_num_faces = 1
    refine_landmarks = True
    min_detection_confidence = 0.5
    min_tracking_confidence = 0.5
    return mp_face_mesh.FaceMesh(
        static_image_mode=static_image_mode,
        max_num_faces=max_num_faces,
        refine_landmarks=refine_landmarks,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )


_face_mesh = None


def get_face_mesh():
    global _face_mesh
    if _face_mesh is None:
        _face_mesh = _get_face_mesh()
    return _face_mesh


def get_face_landmarks(frame: np.ndarray):
    """
    Run face detection + landmark extraction on a BGR frame (OpenCV format).

    - Resizes to INPUT_WIDTH x INPUT_HEIGHT for consistent inference.
    - Returns landmarks in image coordinates (resized image).

    Returns:
        dict with:
          - face_detected: bool
          - landmarks: list of (x, y) in image coords, or None
          - left_eye: list of (x, y), or None
          - right_eye: list of (x, y), or None
          - mouth: list of (x, y), or None
          - all_landmarks: list of (x, y) for all 468 points, or None (for head pose)
    """
    resized = cv2.resize(frame, (INPUT_WIDTH, INPUT_HEIGHT))
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

    mesh = get_face_mesh()
    results = mesh.process(rgb)

    out = {
        "face_detected": False,
        "landmarks": None,
        "left_eye": None,
        "right_eye": None,
        "mouth": None,
        "all_landmarks": None,
    }

    if not results.multi_face_landmarks:
        return out

    lm = results.multi_face_landmarks[0]
    all_pts = []
    for l in lm.landmark:
        x = l.x * INPUT_WIDTH
        y = l.y * INPUT_HEIGHT
        all_pts.append((float(x), float(y)))

    def pick(indices):
        return [all_pts[i] for i in indices]

    out["face_detected"] = True
    out["all_landmarks"] = all_pts
    out["landmarks"] = all_pts
    out["left_eye"] = pick(LEFT_EYE_INDICES)
    out["right_eye"] = pick(RIGHT_EYE_INDICES)
    out["mouth"] = pick(MOUTH_INDICES)

    return out
