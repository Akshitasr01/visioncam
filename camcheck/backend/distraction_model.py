"""
Distraction detection via head-pose estimation (yaw, pitch, roll).
Uses solvePnP with 3D face model + MediaPipe landmarks; no training.
"""

import numpy as np
import cv2

from backend.config import (
    INPUT_WIDTH,
    INPUT_HEIGHT,
    YAW_LIMIT_DEG,
    PITCH_LIMIT_DEG,
    LOOK_AWAY_CONSEC_FRAMES,
)
from backend.utils.face_landmarks import get_face_landmarks


# 6-point 3D face model (generic) for solvePnP. Order matches MediaPipe indices below.
# Nose tip, Chin, Left eye, Right eye, Left mouth, Right mouth.
MODEL_3D = np.array([
    (0.0, 0.0, 0.0),
    (0.0, -63.0, -30.0),
    (-43.0, 32.0, -30.0),
    (43.0, 32.0, -30.0),
    (-28.0, -28.0, -30.0),
    (28.0, -28.0, -30.0),
], dtype=np.float64)

# MediaPipe Face Mesh indices for those 6 points.
LANDMARK_INDICES = [4, 152, 33, 263, 61, 291]


def _rotation_matrix_to_euler_deg(R: np.ndarray):
    """Convert 3x3 rotation matrix to yaw, pitch, roll in degrees."""
    sy = max(np.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2), 1e-6)
    pitch = np.arctan2(-R[2, 0], sy)
    if sy > 1e-6:
        yaw = np.arctan2(R[1, 0], R[0, 0])
        roll = np.arctan2(R[2, 1], R[2, 2])
    else:
        yaw = np.arctan2(-R[1, 2], R[1, 1])
        roll = 0.0
    return (
        np.degrees(float(yaw)),
        np.degrees(float(pitch)),
        np.degrees(float(roll)),
    )


def _head_pose_from_landmarks(all_landmarks):
    """
    Estimate head pose from 2D landmarks via solvePnP.
    all_landmarks: list of (x, y) in image coords (INPUT_WIDTH x INPUT_HEIGHT).
    Returns (yaw_deg, pitch_deg, roll_deg) or None if fails.
    """
    pts_2d = np.array([all_landmarks[i] for i in LANDMARK_INDICES], dtype=np.float64)
    pts_3d = MODEL_3D.copy()

    fx = float(INPUT_WIDTH)
    fy = float(INPUT_HEIGHT)
    cx = INPUT_WIDTH / 2.0
    cy = INPUT_HEIGHT / 2.0
    cam = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]], dtype=np.float64)
    dist = np.zeros((4, 1), dtype=np.float64)

    ok, rvec, tvec = cv2.solvePnP(pts_3d, pts_2d, cam, dist)
    if not ok:
        return None
    R, _ = cv2.Rodrigues(rvec)
    return _rotation_matrix_to_euler_deg(R)


class DistractionModel:
    """Stateful distraction detector: head pose, looking-away, distracted flag."""

    def __init__(self):
        self.consec_look_away = 0

    def process(self, frame, landmarks=None):
        """
        Process one BGR frame. Optional precomputed landmarks from get_face_landmarks.

        Returns:
            dict: distracted, looking_away, head_pose { yaw, pitch, roll }
        """
        out = {
            "distracted": False,
            "looking_away": False,
            "head_pose": {"yaw": 0.0, "pitch": 0.0, "roll": 0.0},
        }

        if landmarks is None:
            landmarks = get_face_landmarks(frame)

        if not landmarks["face_detected"] or not landmarks.get("all_landmarks"):
            self.consec_look_away = 0
            return out

        all_lm = landmarks["all_landmarks"]
        pose = _head_pose_from_landmarks(all_lm)
        if pose is None:
            self.consec_look_away = 0
            return out

        yaw, pitch, roll = pose
        out["head_pose"]["yaw"] = round(yaw, 2)
        out["head_pose"]["pitch"] = round(pitch, 2)
        out["head_pose"]["roll"] = round(roll, 2)

        away = abs(yaw) > YAW_LIMIT_DEG or abs(pitch) > PITCH_LIMIT_DEG
        out["looking_away"] = away

        if away:
            self.consec_look_away += 1
        else:
            self.consec_look_away = 0

        out["distracted"] = self.consec_look_away >= LOOK_AWAY_CONSEC_FRAMES
        return out
