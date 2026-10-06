@echo off
title AI Project Mentor - Backend Server (Port 8000)
cd /d "%~dp0backend"
echo ===================================================
echo Starting FastAPI Backend Server on http://localhost:8000
echo ===================================================
python -m uvicorn app.main:app --reload --port 8000
pause
