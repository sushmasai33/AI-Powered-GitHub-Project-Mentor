from typing import Dict, Any

SAMPLE_REPOSITORIES: Dict[str, Dict[str, Any]] = {
    "student-dev/fastapi-auth-inventory": {
        "metadata": {
            "name": "fastapi-auth-inventory",
            "owner": {"login": "student-dev"},
            "html_url": "https://github.com/student-dev/fastapi-auth-inventory",
            "description": "Inventory management API built with FastAPI, SQLAlchemy, and JWT authentication.",
            "stargazers_count": 14,
            "forks_count": 3,
            "private": False,
            "language": "Python",
            "default_branch": "main"
        },
        "owner": "student-dev",
        "repo": "fastapi-auth-inventory",
        "branch": "main",
        "tree": [
            "README.md",
            "requirements.txt",
            "Dockerfile",
            "app/__init__.py",
            "app/main.py",
            "app/config.py",
            "app/database.py",
            "app/auth.py",
            "app/routes/items.py",
            "app/routes/users.py",
            "app/models/item.py",
            "app/models/user.py",
            "app/schemas/item.py",
            "tests/test_basic.py"
        ],
        "file_contents": {
            "README.md": """# FastAPI Auth & Inventory Management System

A RESTful backend for tracking warehouse inventory items with role-based access control.

## Technologies
- Python 3.11
- FastAPI
- SQLAlchemy + SQLite / PostgreSQL
- PyJWT

## Installation
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Features
- User registration and login
- JWT bearer tokens
- Create, Read, Update, Delete inventory items

## API Endpoints
- POST `/api/auth/register`
- POST `/api/auth/login`
- GET `/api/items`
- POST `/api/items`
""",
            "requirements.txt": """fastapi==0.110.0
uvicorn==0.28.0
sqlalchemy==2.0.28
pyjwt==2.8.0
passlib[bcrypt]==1.7.4
pydantic==2.6.4
pytest==8.0.2
""",
            "Dockerfile": """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
            "app/config.py": """import os

SECRET_KEY = os.getenv("SECRET_KEY", "super_insecure_hardcoded_jwt_secret_key_12345!")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./inventory.db")
DEBUG = True
""",
            "app/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import items, users
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/auth", tags=["auth"])
app.include_router(items.router, prefix="/api/items", tags=["items"])

@app.get("/health")
def health():
    return {"status": "ok"}
""",
            "app/auth.py": """from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from app.config import SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=60))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
""",
            "app/routes/items.py": """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter()

@router.get("/")
def list_items(query: str = "", db: Session = Depends(get_db)):
    # Vulnerable raw SQL search query without parameterized binding
    if query:
        raw_sql = f"SELECT * FROM items WHERE name LIKE '%{query}%'"
        result = db.execute(text(raw_sql)).fetchall()
        return [dict(r._mapping) for r in result]
    return []

@router.post("/")
def create_item(name: str, quantity: int, db: Session = Depends(get_db)):
    return {"id": 1, "name": name, "quantity": quantity}
""",
            "tests/test_basic.py": """def test_app_import():
    import app.main
    assert app.main.app is not None
"""
        }
    },
    "team-student/nextjs-campus-hub": {
        "metadata": {
            "name": "nextjs-campus-hub",
            "owner": {"login": "team-student"},
            "html_url": "https://github.com/team-student/nextjs-campus-hub",
            "description": "Fullstack student marketplace and forum built with Next.js App Router, TypeScript, and Supabase.",
            "stargazers_count": 28,
            "forks_count": 5,
            "private": False,
            "language": "TypeScript",
            "default_branch": "main"
        },
        "owner": "team-student",
        "repo": "nextjs-campus-hub",
        "branch": "main",
        "tree": [
            "README.md",
            "package.json",
            "tsconfig.json",
            "src/app/page.tsx",
            "src/app/layout.tsx",
            "src/app/api/listings/route.ts",
            "src/app/api/auth/[...nextauth]/route.ts",
            "src/components/ListingCard.tsx",
            "src/components/Navbar.tsx",
            "src/lib/supabase.ts"
        ],
        "file_contents": {
            "README.md": """# Next.js Campus Hub

A community portal for university students to exchange course notes, buy/sell textbooks, and post campus announcements.

## Tech Stack
- Next.js 14 App Router
- TypeScript
- Tailwind CSS
- Supabase (PostgreSQL + Auth)

## Getting Started
```bash
npm install
npm run dev
```
""",
            "package.json": """{
  "name": "nextjs-campus-hub",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "@supabase/supabase-js": "^2.39.0",
    "next": "^14.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "lucide-react": "^0.344.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.0.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.3.0"
  }
}
""",
            "src/lib/supabase.ts": """import { createClient } from '@supabase/supabase-js'

// High-risk: Service role key used in client-accessible utility
export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://xyzcompany.supabase.co',
  process.env.SUPABASE_SERVICE_ROLE_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummy_service_key'
)
""",
            "src/app/api/listings/route.ts": """import { NextResponse } from 'next/server'
import { supabase } from '@/lib/supabase'

export async function GET() {
  const { data, error } = await supabase.from('listings').select('*')
  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json({ listings: data })
}

export async function POST(req: Request) {
  const body = await req.json()
  // Missing authentication guard and input validation schema
  const { data, error } = await supabase.from('listings').insert(body)
  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json({ item: data })
}
"""
        }
    }
}
