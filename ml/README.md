# VisionCam ML 

Python FastAPI service for drowsiness, distraction, and phone-usage detection.

## Setup

From the **project root** (VisionCam):

```bash
# Create a virtual environment (recommended; use Python 3.10–3.12 if you have issues on 3.13)
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r ml/requirements.txt
```

## Run

From the **project root**:

```bash
uvicorn ml.ml_server:app --reload --host 0.0.0.0 --port 8000
```


Or:

```bash
python -m ml.ml_server
```

- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

## Test detection

- **POST** `/api/detect` with form field `file` (image file).

- **Windows (PowerShell):** PowerShell’s `curl` is an alias; use `curl.exe`:

  ```powershell
  curl.exe -X POST -F "file=@C:\path\to\image.jpg" http://localhost:8000/api/detect
  ```

- **Windows (PowerShell alternative):**

  ```powershell
  $uri = "http://localhost:8000/api/detect"
  $form = @{ file = Get-Item -Path "C:\path\to\image.jpg" }
  Invoke-RestMethod -Uri $uri -Method Post -Form $form
  ```

- **macOS / Linux (bash):**

  ```bash
  curl -X POST -F "file=@path/to/image.jpg" http://localhost:8000/api/detect
  ```
