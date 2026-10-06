# AI-Powered GitHub Project Mentor PowerShell Launcher
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  AI-POWERED GITHUB PROJECT MENTOR" -ForegroundColor Green
Write-Host "  Launching Backend (Port 8000) and Frontend (Port 3000)..." -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Start Backend FastAPI Server
Write-Host "`n[1/3] Starting Backend Server (FastAPI on Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir\backend'; Write-Host 'FastAPI Backend Running on http://localhost:8000' -ForegroundColor Green; python -m uvicorn app.main:app --reload --port 8000"

Start-Sleep -Seconds 3

# 2. Start Frontend Next.js Server
Write-Host "[2/3] Starting Frontend Dashboard (Next.js on Port 3000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir\frontend'; Write-Host 'Next.js Frontend Running on http://localhost:3000' -ForegroundColor Cyan; npm run dev"

Start-Sleep -Seconds 4

# 3. Open Browser
Write-Host "[3/3] Opening browser at http://localhost:3000 ..." -ForegroundColor Green
Start-Process "http://localhost:3000"

Write-Host "`nBoth services are now running in separate persistent windows!" -ForegroundColor Green
Write-Host "Frontend Dashboard: http://localhost:3000" -ForegroundColor White
Write-Host "Backend API:        http://localhost:8000" -ForegroundColor White
Write-Host "API Swagger Docs:   http://localhost:8000/docs" -ForegroundColor White
