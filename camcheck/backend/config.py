"""
Central configuration for VisionCam ML backend.
Tune thresholds and behaviour here without editing model code.
"""

# ----- Drowsiness (blink + yawn) -----
EAR_CLOSED_THRESHOLD = 0.25       # Eye Aspect Ratio below this = eye closed
MAR_YAWN_THRESHOLD = 0.5          # Mouth Aspect Ratio above this = yawn
BLINK_CONSEC_FRAMES = 3           # Min consecutive frames "closed" to count as blink
YAWN_CONSEC_FRAMES = 15           # Min consecutive frames "open mouth" to count as yawn
DROWSY_BLINK_WINDOW_SEC = 20      # Window (seconds) to count blinks for drowsiness
DROWSY_BLINK_COUNT = 3            # Blinks in window above → flag drowsy

# ----- Distraction (head pose) -----
YAW_LIMIT_DEG = 30                # |yaw| > this → looking left/right
PITCH_LIMIT_DEG = 20              # |pitch| > this → looking up/down
LOOK_AWAY_CONSEC_FRAMES = 10      # Min consecutive "looking away" frames to flag

# ----- Phone usage -----
PHONE_CONFIDENCE_THRESHOLD = 0.5  # Detector confidence above this = phone
PHONE_CONSEC_FRAMES = 15          # Min consecutive frames with phone to flag

# ----- General -----
INPUT_WIDTH = 640                 # Resize frame width before inference
INPUT_HEIGHT = 480                # Resize frame height
FRAME_SKIP = 1                    # Process every Nth frame (1 = all; 2 = half)
ASSUMED_FPS = 30                  # Used for drowsiness blink-window (seconds -> frames)
