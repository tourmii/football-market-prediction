# Football Market Prediction

Player analytics dashboard with market value predictions and performance statistics.

## Quick Start

```bash
docker compose up --build
```

**Access:**
- Frontend: http://localhost:3000
- API: http://localhost:8000

## Local Development

```bash
# Backend
uv run uvicorn backend.main:app --reload --port 8000

# Frontend (serve static files)
cd frontend && python -m http.server 3000
```

## Project Structure

```
├── backend/          # FastAPI server
├── frontend/         # Static HTML/JS/CSS
├── data/             # Player CSV data
└── eda/              # Exploratory analysis
```
