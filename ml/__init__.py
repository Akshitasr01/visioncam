# VisionCam ML backend package
# ml/__init__.py

# This class will store all state variables related to ML processing
class MLState:
    def __init__(self):
        self.yawn_start_frame = None
        self.blink_count = 0
        self.drowsiness_alerted = False
        # Add any other state variables your ML modules need

# Create a single instance of MLState to use across the ml package
ml_state = MLState()