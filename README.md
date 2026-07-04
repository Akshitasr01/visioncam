# VisionCam

Driver monitoring prototype that uses a webcam to detect drowsiness, distraction, and phone usage. The app combines a React frontend, a Node/Express auth API, and a Python FastAPI ML service.

## Architecture

| Service | Stack | Port | Purpose |
|---------|-------|------|---------|
| Frontend | React, Vite, Tailwind | 5173 | UI — login, signup, live monitor, dashboard |
| Backend | Node, Express, TypeScript, MongoDB | 3000 | User auth and profiles |
| ML server | Python, FastAPI, OpenCV, MediaPipe | 8000 | Webcam frame analysis |

## Prerequisites

- **Node.js** v18+
- **Python** 3.10–3.12 (3.13 may have issues with some ML dependencies)
- **MongoDB** — local instance or [MongoDB Atlas](https://www.mongodb.com/atlas)

## Setup & Run

Run all three services in separate terminals.

### 1. Frontend

From the project root:

```bash
npm install
npm run dev
```

Open **http://localhost:5173**

### 2. Backend

```bash
cd backend
npm install
```

Create `backend/.env` (copy from `backend/.env.example`):

```env
JWT_SECRET=your-secret-key-here
DATABASE_URL=mongodb://localhost:27017/visioncam
```

Start the API:

```bash
npm run dev
```

Runs on **http://localhost:3000**

**Endpoints:**
- `POST /api/v1/signup` — register
- `POST /api/v1/signin` — login (returns JWT)
- `GET /api/v1/profile` — user profile (requires `Authorization: Bearer <token>`)

### 3. ML server

From the **project root**:

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

pip install -r ml/requirements.txt
```

Start the server:

```bash
uvicorn ml.ml_server:app --reload --host 0.0.0.0 --port 8000
```

Or:

```bash
python run_ml.py
```

- API: **http://localhost:8000**
- Docs: **http://localhost:8000/docs**
- Health: **http://localhost:8000/health**

See [ml/README.md](ml/README.md) for more ML details and API testing examples.

## Quick start (three terminals)

| # | Directory | Command |
|---|-----------|---------|
| 1 | `VisionCam/` | `npm run dev` |
| 2 | `VisionCam/backend/` | `npm run dev` |
| 3 | `VisionCam/` (venv active) | `uvicorn ml.ml_server:app --reload --port 8000` |

## Environment variables

### Backend (`backend/.env`)

| Variable | Description |
|----------|-------------|
| `JWT_SECRET` | Secret for signing JWT tokens |
| `DATABASE_URL` | MongoDB connection string |

### Frontend (optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_BASE` | `http://localhost:8000` | ML API URL used by the Monitor page |

## App routes

| Route | Page |
|-------|------|
| `/` | Home |
| `/user-type` | Choose login or signup |
| `/login` | Sign in |
| `/signup` | Register |
| `/monitor` | Live camera monitoring (requires ML server) |
| `/dashboard` | User profile and emergency contact |
| `/alerts` | Alert history |
| `/settings` | Settings |

## Health checks

- Frontend: http://localhost:5173
- Backend: sign up or log in via the app
- ML: http://localhost:8000/health

## Project structure

```
VisionCam/
├── src/              # React frontend
├── backend/          # Express + TypeScript API
├── ml/               # Python FastAPI ML service
├── run_ml.py         # Alternative ML server entry point
└── package.json      # Frontend dependencies
```

## Build for production

```bash
# Frontend
npm run build
npm run preview

# Backend
cd backend && npm run dev   # compiles TypeScript then runs dist/index.js
```

## Troubleshooting

- **Monitor page shows ML errors** — ensure the ML server is running on port 8000.
- **Login/signup fails** — ensure MongoDB is running and `backend/.env` is configured.
- **MediaPipe / OpenCV install issues on Python 3.13** — use Python 3.10–3.12 in a virtual environment.
- **PowerShell `curl` issues** — use `curl.exe` or `Invoke-RestMethod` when testing the ML API (see `ml/README.md`).
