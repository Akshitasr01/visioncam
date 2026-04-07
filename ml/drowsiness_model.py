"""
Drowsiness detection via:
- Eye Aspect Ratio (EAR)
- Blink counting
- Yawn detection using MediaPipe FaceMesh (CORRECT landmarks)

NO ML training required.
"""

import numpy as np

from .config import (
    EAR_CLOSE_THRESH,
    EAR_OPEN_THRESH,
    MIN_BLINK_FRAMES,
    DROWSY_BLINK_WINDOW_SEC,
    DROWSY_BLINK_COUNT,
    MAR_YAWN_THRESHOLD,
    YAWN_MIN_DURATION_SEC,
    YAWN_COOLDOWN_SEC,
    ASSUMED_FPS,
)

from .utils.face_landmarks import get_face_landmarks


# ==================== HELPERS ====================

def _dist(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))


def _ear_6pts(pts):
    """
    EAR using 6 eye landmarks
    """
    v1 = _dist(pts[1], pts[5])
    v2 = _dist(pts[2], pts[4])
    h = _dist(pts[0], pts[3])
    if h < 1e-6:
        return 0.0
    return (v1 + v2) / (2.0 * h)


def compute_mar_from_facemesh(all_landmarks):
    """
    CORRECT MAR using MediaPipe FaceMesh indices
    """
    LEFT_CORNER = 61
    RIGHT_CORNER = 291
    TOP_LIP = 13
    BOTTOM_LIP = 14

    left = np.array(all_landmarks[LEFT_CORNER])
    right = np.array(all_landmarks[RIGHT_CORNER])
    top = np.array(all_landmarks[TOP_LIP])
    bottom = np.array(all_landmarks[BOTTOM_LIP])

    horizontal = np.linalg.norm(left - right)
    vertical = np.linalg.norm(top - bottom)

    if horizontal < 1e-6:
        return 0.0

    return vertical / horizontal


# ==================== MODEL ====================

class DrowsinessModel:
    def __init__(self):
        self.frame_index = 0

        # Eye / blink state
        self.eye_state = "open"
        self.closed_frames = 0
        self.blink_count = 0
        self.blink_frames = []

        self.window_frames = int(DROWSY_BLINK_WINDOW_SEC * ASSUMED_FPS)

        # Yawn state
        self.yawn_start_frame = None
        self.last_yawn_frame = -1e9

    def process(self, frame, landmarks=None):
        self.frame_index += 1

        out = {
            "drowsy": False,
            "eye_status": "open",
            "blink_count": int(self.blink_count),
            "yawn_detected": False,
            "ear": 0.0,
            "mar": 0.0,
        }

        if landmarks is None:
            landmarks = get_face_landmarks(frame)

        if (
            not landmarks["face_detected"]
            or not landmarks["left_eye"]
            or not landmarks["right_eye"]
            or not landmarks["all_landmarks"]
        ):
            self.eye_state = "open"
            self.closed_frames = 0
            self.yawn_start_frame = None
            return out

        # ==================== EAR ====================

        left_eye = landmarks["left_eye"]
        right_eye = landmarks["right_eye"]

        ear = (_ear_6pts(left_eye) + _ear_6pts(right_eye)) / 2.0
        out["ear"] = ear

        # ==================== BLINK ====================

        if self.eye_state == "open":
            if ear < EAR_CLOSE_THRESH:
                self.eye_state = "closed"
                self.closed_frames = 1
        else:
            self.closed_frames += 1
            if ear > EAR_OPEN_THRESH:
                if self.closed_frames >= MIN_BLINK_FRAMES:
                    self.blink_count += 1
                    self.blink_frames.append(self.frame_index)
                self.eye_state = "open"
                self.closed_frames = 0

        cutoff = self.frame_index - self.window_frames
        self.blink_frames = [f for f in self.blink_frames if f > cutoff]

        out["eye_status"] = "closed" if self.eye_state == "closed" else "open"
        out["blink_count"] = int(self.blink_count)

        # ==================== YAWN ====================

        mar = compute_mar_from_facemesh(landmarks["all_landmarks"])
        out["mar"] = mar

        yawn_detected = False
        cooldown_frames = int(YAWN_COOLDOWN_SEC * ASSUMED_FPS)

        if mar > MAR_YAWN_THRESHOLD:
            if self.yawn_start_frame is None:
                self.yawn_start_frame = self.frame_index
        else:
            self.yawn_start_frame = None

        if self.yawn_start_frame is not None:
            duration = (self.frame_index - self.yawn_start_frame) / ASSUMED_FPS
            if (
                duration >= YAWN_MIN_DURATION_SEC
                and (self.frame_index - self.last_yawn_frame) > cooldown_frames
            ):
                yawn_detected = True
                self.last_yawn_frame = self.frame_index
                self.yawn_start_frame = None

        out["yawn_detected"] = yawn_detected

        # ==================== DROWSY ====================

        out["drowsy"] = bool(
            len(self.blink_frames) >= DROWSY_BLINK_COUNT or yawn_detected
        )

        return out