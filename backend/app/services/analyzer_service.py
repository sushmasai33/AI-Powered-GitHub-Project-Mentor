import os
import re
import json
from typing import Dict, List, Any, Optional

EXT_LANGUAGE_MAP = {
    '.py': 'Python',
    '.ts': 'TypeScript',
    '.tsx': 'TypeScript (React)',
    '.js': 'JavaScript',
    '.jsx': 'JavaScript (React)',
    '.go': 'Go',
    '.java': 'Java',
    '.rs': 'Rust',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.cs': 'C#',
    '.cpp': 'C++',
    '.c': 'C',
    '.html': 'HTML',
    '.css': 'CSS',
    '.sql': 'SQL',
    '.sh': 'Shell',
    '.yml': 'YAML',
    '.yaml': 'YAML',
    '.json': 'JSON',
    '.md': 'Markdown'
}

FRAMEWORK_SIGNATURES = {
    'FastAPI': [r'fastapi', r'from fastapi import'],
    'Flask': [r'flask', r'from flask import'],
    'Django': [r'django', r'django-admin'],
    'Next.js': [r'next', r'"next":', r'next/server', r'next/navigation'],
    'React': [r'react', r'"react":', r'from [\'"]react[\'"]'],
    'Express': [r'express', r'"express":', r'require\([\'"]express[\'"]\)'],
    'NestJS': [r'@nestjs', r'"@nestjs/core"'],
    'Spring Boot': [r'spring-boot', r'org\.springframework\.boot'],
    'Gin': [r'github\.com/gin-gonic/gin']
}

DATABASE_SIGNATURES = {
    'SQLAlchemy': [r'sqlalchemy'],
    'Supabase': [r'@supabase/supabase-js', r'supabase'],
    'Prisma': [r'@prisma/client', r'prisma'],
    'Mongoose / MongoDB': [r'mongoose', r'mongodb', r'pymongo'],
    'PostgreSQL': [r'psycopg2', r'asyncpg', r'pg', r'postgres'],
    'SQLite': [r'sqlite3', r'sqlite'],
    'Redis': [r'redis', r'ioredis']
}

AUTH_SIGNATURES = {
    'JWT Authentication': [r'pyjwt', r'jsonwebtoken', r'jwt\.encode', r'jwt\.decode'],
    'Bcrypt Hashing': [r'bcrypt', r'passlib'],
    'NextAuth.js': [r'next-auth', r'@auth/core'],
    'Passport.js': [r'passport']
}

TEST_SIGNATURES = {
    'Pytest': [r'pytest'],
    'Jest': [r'jest'],
    'Vitest': [r'vitest'],
    'Cypress': [r'cypress'],
    'Playwright': [r'playwright'],
    'Unittest': [r'unittest']
}

class CodeAnalyzerService:
    @staticmethod
    def analyze_repository(ingestion_result: Dict[str, Any]) -> Dict[str, Any]:
        tree: List[str] = ingestion_result.get("tree", [])
        file_contents: Dict[str, str] = ingestion_result.get("file_contents", {})
        metadata: Dict[str, Any] = ingestion_result.get("metadata", {})
        
        # 1. Language Breakdown
        language_counts: Dict[str, int] = {}
        for path in tree:
            _, ext = os.path.splitext(path.lower())
            if ext in EXT_LANGUAGE_MAP:
                lang = EXT_LANGUAGE_MAP[ext]
                language_counts[lang] = language_counts.get(lang, 0) + 1
        
        primary_lang = metadata.get("language")
        if not primary_lang and language_counts:
            primary_lang = max(language_counts.items(), key=lambda x: x[1])[0]
        if not primary_lang:
            primary_lang = "Unknown"

        # Combine all file contents for dependency / signature search
        all_text = " ".join(file_contents.values())

        # 2. Framework & Library Detection
        detected_frameworks = []
        for name, patterns in FRAMEWORK_SIGNATURES.items():
            if any(re.search(p, all_text, re.IGNORECASE) for p in patterns):
                detected_frameworks.append(name)

        detected_databases = []
        for name, patterns in DATABASE_SIGNATURES.items():
            if any(re.search(p, all_text, re.IGNORECASE) for p in patterns):
                detected_databases.append(name)

        detected_auth = []
        for name, patterns in AUTH_SIGNATURES.items():
            if any(re.search(p, all_text, re.IGNORECASE) for p in patterns):
                detected_auth.append(name)

        detected_testing = []
        for name, patterns in TEST_SIGNATURES.items():
            if any(re.search(p, all_text, re.IGNORECASE) for p in patterns):
                detected_testing.append(name)

        # 3. Detect Testing Presence
        test_files = [p for p in tree if any(part in p.lower() for part in ['test', 'spec', '__tests__'])]
        has_tests = len(test_files) > 0

        # 4. Detect CI/CD & Docker
        has_docker = any('dockerfile' in p.lower() or 'docker-compose' in p.lower() for p in tree)
        has_cicd = any('.github/workflows' in p.lower() or '.gitlab-ci' in p.lower() for p in tree)

        # 5. Architecture Inference
        architecture_type = "Modular Application"
        arch_explanation = "The repository is structured around dedicated source directories."
        if "Next.js" in detected_frameworks:
            architecture_type = "Fullstack Next.js Application (App Router / SSR)"
            arch_explanation = "Uses Next.js with React Server Components, client modules, and built-in API route handlers."
        elif "FastAPI" in detected_frameworks or "Flask" in detected_frameworks:
            architecture_type = "Layered REST API Service (Python Backend)"
            arch_explanation = "Adopts a layered backend pattern with routers, models, schemas, and database session injection."
        elif "Express" in detected_frameworks or "NestJS" in detected_frameworks:
            architecture_type = "Node.js RESTful Web Service"
            arch_explanation = "Implements an Express/Node asynchronous request pipeline with middleware routing."

        # 6. Main Modules Explanation
        main_modules = []
        seen_dirs = set()
        for path in tree:
            parts = path.split('/')
            if len(parts) > 1:
                top_dir = parts[0]
                if top_dir not in seen_dirs and top_dir not in ['node_modules', '.git']:
                    seen_dirs.add(top_dir)
                    desc = f"Contains {top_dir} implementation logic and subsystem components."
                    if top_dir.lower() in ['app', 'src']:
                        desc = "Primary application source code containing business logic and modules."
                    elif top_dir.lower() in ['tests', '__tests__']:
                        desc = "Automated test suites and verification scripts."
                    elif top_dir.lower() in ['components', 'ui']:
                        desc = "Reusable UI view components and layout templates."
                    elif top_dir.lower() in ['routes', 'api', 'controllers']:
                        desc = "API route endpoints and HTTP request handlers."
                    elif top_dir.lower() in ['models', 'entities']:
                        desc = "Data entities and database schema definitions."
                    main_modules.append({"module": top_dir, "description": desc})

        # 7. Request Workflow Inference
        if "FastAPI" in detected_frameworks:
            workflow = "HTTP Client -> FastAPI Router -> Authentication & Dependency Injection -> Service/Handler -> Database Query (ORM) -> Response Schema Serialization -> Client."
        elif "Next.js" in detected_frameworks:
            workflow = "Browser Request -> Next.js Edge/Server Middleware -> App Router (Server Component / API Route) -> Database/Supabase Client -> Rendered HTML / JSON -> Client."
        elif "Express" in detected_frameworks:
            workflow = "HTTP Request -> Express Middleware -> Route Controller -> Database Driver -> JSON Response."
        else:
            workflow = "Client Invocation -> Entry Point -> Module Handlers -> Storage Layer -> Response."

        return {
            "primary_language": primary_lang,
            "language_counts": language_counts,
            "detected_frameworks": detected_frameworks,
            "detected_databases": detected_databases,
            "detected_auth": detected_auth,
            "detected_testing": detected_testing,
            "test_files": test_files,
            "has_tests": has_tests,
            "has_docker": has_docker,
            "has_cicd": has_cicd,
            "architecture_type": architecture_type,
            "architecture_explanation": arch_explanation,
            "main_modules": main_modules[:8],
            "request_workflow": workflow,
            "file_count": len(tree)
        }
