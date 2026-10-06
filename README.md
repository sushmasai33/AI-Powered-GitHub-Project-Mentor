# AI-Powered GitHub Project Mentor 🎓

> **An AI-powered project mentor that converts an actual GitHub repository into a complete project health assessment, evidence-based gap analysis, personalized improvement roadmap, repository-grounded mentoring experience, and project-specific interview preparation system.**

---

## 📌 Project Overview & Differentiation

Most existing tools position themselves merely as generic chatbots or line-by-line AI code reviewers. **AI-Powered GitHub Project Mentor** is built specifically for students, educators, and junior engineers preparing for project demonstrations, viva examinations, and technical interviews.

### Core Product Pipeline:
```
GitHub Repository → Ingestion & AST Analysis → Security & Secret Scan → Evidence-Based Gap Detection → Transparent Scoring → Personalized 6-Phase Roadmap → RAG Mentor Chat → Viva / Interview Preparation
```

---

## 🌟 Key Features

1. **Evidence-Based Missing Feature Detection (Core Differentiator)**:
   - Scans routes, AST nodes, database models, schemas, and tests to identify absent capabilities (e.g. password recovery, rate limiting, error logging, schema validation) rather than hallucinating features.
   - Distinct statuses: `Implemented`, `Partially Implemented`, `Missing` (using explicit *"No implementation evidence detected"*), and `Cannot Determine`.

2. **Transparent Deterministic Scoring Engine**:
   - Explicit mathematical scoring formulas (not arbitrary LLM guesses):
     - **Code Quality (20%)**: Folder modularity, domain isolation, static typing.
     - **Security (20%)**: Direct deductions based on severity (-30 critical, -15 high, -8 medium).
     - **Testing (15%)**: Automated assertions, unit & integration test coverage, CI pipeline.
     - **Documentation (10%)**: Standard 10-criterion rubric evaluation.
     - **Architecture (15%)**: Layered design, containerization (Docker), ORM persistence.
     - **Feature Completeness (15%)**: Ratio of implemented vs expected domain capabilities.
     - **Maintainability (5%)**: Package manifests, dependency pinning, reproducibility.

3. **Static Security & Secret Scanner**:
   - Detects hardcoded secrets, API tokens, JWT keys, SQL injections (f-strings / string concatenation in raw queries), command execution (`eval`, `exec`, `os.system`), XSS, insecure CORS, and debug modes in production.
   - Maps each finding to **CWE** (Common Weakness Enumeration) with beginner-friendly explanations and exact fix code snippets.

4. **README Health Audit**:
   - Evaluates documentation against 10 critical academic/open-source criteria (Description, Problem Statement, Features, Stack, Installation, Config, Usage, Architecture, API, License).

5. **Personalized 6-Phase Improvement Roadmap**:
   - Automatically prioritizes detected vulnerabilities, quality debt, missing features, documentation gaps, and scaling opportunities into actionable phases with interactive completion checkoffs.

6. **Repository-Grounded AI Mentor (RAG)**:
   - Semantic chunking with token relevance and file affinity.
   - **Prompt Injection Defense**: Isolates untrusted repository files inside strict security barriers, rejecting malicious system prompt overrides.
   - Cites exact file paths and line numbers for every repository fact.

7. **Project-Specific Viva & Technical Interview Simulator**:
   - Generates tailored viva questions across 6 categories: **Basic**, **Architecture**, **Code**, **Database**, **Security**, and **Advanced Scalability**.
   - Includes expected model answers, relevant repository files, and examiner follow-up probes.

---

## 🏗️ Architecture & Technology Baseline

- **Frontend**: Next.js 16 (App Router), TypeScript, Tailwind CSS, Lucide Icons.
- **Backend**: Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy, Uvicorn.
- **Database**: Supabase / PostgreSQL schema with indexes and RLS policies (`backend/database/supabase_schema.sql`), with automatic SQLite zero-config local fallback for instant local execution.
- **AI & RAG Engine**: Google GenAI (`google-genai` / Gemini 2.5) with built-in deterministic heuristic fallback for offline or zero-configuration operation.

---

## 🚀 Quickstart Guide

### 1. Backend Setup
```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
Backend API will be available at: `http://localhost:8000` (Swagger docs at `http://localhost:8000/docs`).

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend Dashboard will be available at: `http://localhost:3000`.

---

## 🧪 Automated Testing & Validation

### Run Backend Unit & Integration Tests (14/14 tests):
```bash
cd backend
python -m pytest tests -v
```

### Run Full End-to-End Workflow Verification:
```bash
python scripts/test_e2e_flow.py
```

### Build Frontend Production Bundle:
```bash
cd frontend
npm run build
```

---

## 📋 Requirement Evidence Matrix

| Requirement | Implementation Module | Validation Gate | Evidence | Result |
|---|---|---|---|---|
| **GitHub Connection** | `app/services/github_service.py` | API & Ingestion Tests | Public & token ingestion with branch resolution | **PASS** |
| **Repository Analysis** | `app/services/analyzer_service.py` | Architecture & AST Test | Inferred patterns, modules, frameworks | **PASS** |
| **AI Project Summary** | `app/services/ai_service.py` | AI Validation Test | Objective overview, problem, workflow, maturity | **PASS** |
| **Quality Score** | `app/services/scoring_service.py` | Deterministic Score Test | 7-category weighted formulas (0-100) | **PASS** |
| **Security Analysis** | `app/services/security_scanner.py` | Security Scanner Test | CWE-89 SQLi, CWE-798 Secrets, CWE-78 Exec | **PASS** |
| **README Analyzer** | `app/services/readme_analyzer.py` | Readme Rubric Test | 10-category scoring & recommendations | **PASS** |
| **Missing Features** | `app/services/feature_gap_detector.py` | Feature Gap Test | Evidence-based matrix with status labels | **PASS** |
| **AI Mentor (RAG)** | `app/services/rag_service.py` | RAG & Injection Test | Exact citations + injection attempt blocked | **PASS** |
| **Roadmap Engine** | `app/services/roadmap_service.py` | Roadmap Item Test | 6-phase prioritized action items + toggle | **PASS** |
| **Interview Prep** | `app/services/interview_generator.py` | Interview Category Test | 6 categories, answers, file references | **PASS** |
| **Next.js Dashboard** | `frontend/src/app/page.tsx` | Production Build Test | Turbopack static compilation 0 errors | **PASS** |

---

## 🛡️ Security Architecture & Untrusted Code Defense

1. **Repository Text Isolation**: User code, READMEs, and comments are treated as untrusted data and parsed through semantic token chunkers before reasoning.
2. **Prompt Injection Barrier**: Detects and neutralizes directives attempting to override assistant behavior or extract credentials.
3. **Protected Credentials**: Access tokens and API keys are stored only in server environment variables and never exposed to client browsers.
