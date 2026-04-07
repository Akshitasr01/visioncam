"""
Distraction detection via head-pose estimation (yaw, pitch, roll).
Uses solvePnP with 3D face model + MediaPipe landmarks; no training.
"""

import numpy as np
import cv2

from .config import (
    INPUT_WIDTH,
    INPUT_HEIGHT,
    YAW_LIMIT_DEG,
    PITCH_LIMIT_DEG,
    LOOK_AWAY_CONSEC_FRAMES,
)
from .utils.face_landmarks import get_face_landmarks


MODEL_3D = np.array([
    (0.0, 0.0, 0.0),
    (0.0, -63.0, -30.0),
    (-43.0, 32.0, -30.0),
    (43.0, 32.0, -30.0),
    (-28.0, -28.0, -30.0),
    (28.0, -28.0, -30.0),
], dtype=np.float64)

LANDMARK_INDICES = [4, 152, 33, 263, 61, 291]


def _rotation_matrix_to_euler_deg(R: np.ndarray):
    sy = max(np.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2), 1e-6)
    pitch = np.arctan2(-R[2, 0], sy)

    if sy > 1e-6:
        yaw = np.arctan2(R[1, 0], R[0, 0])
        roll = np.arctan2(R[2, 1], R[2, 2])
    else:
        yaw = np.arctan2(-R[1, 2], R[1, 1])
        roll = 0.0

    return (
        float(np.degrees(yaw)),
        float(np.degrees(pitch)),
        float(np.degrees(roll)),
    )


def _head_pose_from_landmarks(all_landmarks):
    pts_2d = np.array([all_landmarks[i] for i in LANDMARK_INDICES], dtype=np.float64)
    pts_3d = MODEL_3D.copy()

    cam = np.array(
        [
            [float(INPUT_WIDTH), 0, INPUT_WIDTH / 2.0],
            [0, float(INPUT_HEIGHT), INPUT_HEIGHT / 2.0],
            [0, 0, 1],
        ],
        dtype=np.float64,
    )

    dist = np.zeros((4, 1), dtype=np.float64)

    ok, rvec, _ = cv2.solvePnP(pts_3d, pts_2d, cam, dist)
    if not ok:
        return None

    R, _ = cv2.Rodrigues(rvec)
    return _rotation_matrix_to_euler_deg(R)


class DistractionModel:
    def __init__(self):
        self.consec_look_away = 0

    def process(self, frame, landmarks=None):
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

        pose = _head_pose_from_landmarks(landmarks["all_landmarks"])
        if pose is None:
            self.consec_look_away = 0
            return out

        yaw, pitch, roll = pose
        out["head_pose"]["yaw"] = round(float(yaw), 2)
        out["head_pose"]["pitch"] = round(float(pitch), 2)
        out["head_pose"]["roll"] = round(float(roll), 2)

        away = abs(yaw) > YAW_LIMIT_DEG or abs(pitch) > PITCH_LIMIT_DEG
        out["looking_away"] = bool(away)

        if away:
            self.consec_look_away += 1
        else:
            self.consec_look_away = 0

        out["distracted"] = bool(
            self.consec_look_away >= LOOK_AWAY_CONSEC_FRAMES
        )
        return out