"""Small runner to start the ML FastAPI app directly.
This avoids uvicorn's module import path issues by passing the app object.
"""
from ml.ml_server import app
import uvicorn


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

# # 🔹 NEW: convert NumPy → Python
# def _py(x):
#     if isinstance(x, np.generic):
#         return x.item()
#     return x