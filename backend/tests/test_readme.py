import pytest
from app.services.readme_analyzer import ReadmeAnalyzerService

def test_empty_readme_score():
    res = ReadmeAnalyzerService.analyze_readme("")
    assert res["overall_score"] == 0
    assert len(res["missing_sections"]) > 5

def test_rich_readme_score():
    readme = """# E-Commerce Platform

A production-ready store API solving inventory bottlenecks.

## Problem Statement
Small businesses struggle with manual inventory reconciliation.

## Features
- User authentication
- Product catalog
- Stripe checkout

## Tech Stack
- Next.js
- FastAPI
- PostgreSQL

## Installation
```bash
git clone repo
pip install -r requirements.txt
uvicorn app.main:app
```

## Configuration
Copy `.env.example` to `.env` and set `DATABASE_URL`.

## Usage
Run `curl http://localhost:8000/api/items`.

## Architecture
Client -> FastAPI Gateway -> PostgreSQL Database.

## API Reference
- GET `/api/items`
- POST `/api/items`

## License
MIT License.
"""
    res = ReadmeAnalyzerService.analyze_readme(readme)
    assert res["overall_score"] >= 80
    assert len(res["missing_sections"]) == 0
