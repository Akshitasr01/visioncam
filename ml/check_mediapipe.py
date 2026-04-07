import mediapipe as mp
import importlib.util

print('version:', getattr(mp, '__version__', 'unknown'))
print('has mp.solutions.face_mesh:', getattr(mp, 'solutions', None) is not None and hasattr(mp.solutions, 'face_mesh'))
mods = ['mediapipe.solutions.face_mesh', 'mediapipe.python.solutions.face_mesh', 'mediapipe.tasks.vision.face_mesh', 'mediapipe.tasks']
for m in mods:
    spec = importlib.util.find_spec(m)
    print(('found module:' if spec else 'no module:'), m, '->', 'spec' if spec else 'None')
