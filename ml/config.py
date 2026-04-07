# ---------- DROWSINESS (EYES + BLINKS) ----------
EAR_CLOSE_THRESH = 0.22
EAR_OPEN_THRESH = 0.27
MIN_BLINK_FRAMES = 2
EAR_CLOSED_THRESHOLD = 0.25       # Eye Aspect Ratio below this = eye closed
BLINK_CONSEC_FRAMES = 3           # Min consecutive frames "closed" to count as blink
DROWSY_BLINK_WINDOW_SEC = 20
DROWSY_BLINK_COUNT = 3

# ---------- YAWNING ----------
# Threshold applies to the chosen MAR measure (raw vertical/horizontal by default)
MAR_YAWN_THRESHOLD = 0.48
# Minimum duration (seconds) that MAR must stay above threshold to count as a yawn
YAWN_MIN_DURATION_SEC = 1.0
YAWN_COOLDOWN_SEC = 3.0
# Optional behaviors
MAR_USE_NORMALIZED = False  # If True, MAR will be divided by face height (may produce very small values)
YAWN_DEBUG = True  # Print per-frame MAR/debug info to ML logs
# Auto-tuning of the yawn threshold using running baseline statistics
AUTO_TUNE_YAWN_THRESHOLD = True
MAR_BASELINE_WINDOW = 50  # frames to keep for baseline MAR statistics
# If mouth vertical / face_height < MOUTH_CLOSED_NORM we consider mouth closed and suppress yawns
MOUTH_CLOSED_NORM = 0.12

# ---------- DISTRACTION / HEAD POSE ----------
YAW_LIMIT_DEG = 20        # max yaw rotation in degrees
PITCH_LIMIT_DEG = 15      # max pitch rotation in degrees
ROLL_LIMIT_DEG = 10       # max roll rotation in degrees
LOOK_AWAY_CONSEC_FRAMES = 10  # consecutive frames to consider looking away

# ---------- GENERAL ----------
INPUT_WIDTH = 640
INPUT_HEIGHT = 480
ASSUMED_FPS = 30   # 🔥 MUST match frontend