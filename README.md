# AI Resume Analyzer

An AI-assisted web application for uploading a PDF resume, checking ATS readiness, comparing it with a job description, and receiving clear improvement suggestions.

## Project layout

- `frontend/` — Next.js dashboard
- `backend/` — FastAPI upload, PDF extraction, and analysis API

## Run locally

Open two terminals in this folder.

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

```powershell
cd frontend
npm install
npm run dev
```

Then visit `http://localhost:3000`.

## Current milestone

This first working slice accepts a text-based PDF, extracts its text, and returns transparent rule-based scores. The next milestones add OpenAI analysis, PostgreSQL history, accounts, and downloadable reports.

## Optional AI coaching

Copy `backend/.env.example` to `backend/.env`, then add your own `OPENAI_API_KEY`. The key remains on the backend and is never sent to the browser. Without a key, the dashboard still provides local score-based guidance.
