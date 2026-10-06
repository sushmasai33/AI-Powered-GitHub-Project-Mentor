@echo off
title AI Project Mentor Launcher
echo ================================================================
echo  AI-POWERED GITHUB PROJECT MENTOR
echo  Launching Backend (Port 8000) and Frontend (Port 3000)...
echo ================================================================
echo.

echo [1/3] Starting Python FastAPI Backend on port 8000...
start "AI Project Mentor - Backend" cmd /c "%~dp0run_backend.bat"

echo [2/3] Waiting for backend to initialize...
timeout /t 3 /nobreak >nul

echo [3/3] Starting Next.js Frontend Dashboard on port 3000...
start "AI Project Mentor - Frontend" cmd /c "%~dp0run_frontend.bat"

echo.
echo Waiting for services to become ready...
timeout /t 5 /nobreak >nul

echo.
echo Launching your browser at http://localhost:3000 ...
start http://localhost:3000

echo.
echo ================================================================
echo  Both services are now running in their respective windows!
echo  - Frontend Dashboard: http://localhost:3000
echo  - Backend API:        http://localhost:8000
echo  - Swagger Docs:       http://localhost:8000/docs
echo ================================================================
