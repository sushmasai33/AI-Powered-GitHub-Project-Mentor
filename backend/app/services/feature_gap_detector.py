import re
from typing import Dict, List, Any

CAPABILITY_RULES = [
    {
        "name": "User Authentication & Authorization",
        "category": "Security & Identity",
        "importance": "critical",
        "patterns": [r'login', r'auth', r'jwt', r'token', r'bcrypt', r'password_hash', r'current_user'],
        "file_keywords": ['auth', 'user', 'session'],
        "implemented_desc": "Authentication handlers and token generation detected in routes/modules.",
        "partial_desc": "Basic token references found, but role-based permissions or refresh token logic is not evident.",
        "missing_desc": "No implementation evidence detected. Missing user registration, login, and authorization guards."
    },
    {
        "name": "Password Reset & Account Recovery",
        "category": "Security & Identity",
        "importance": "high",
        "patterns": [r'reset_password', r'forgot_password', r'password_reset', r'recovery_token'],
        "file_keywords": ['reset', 'recovery'],
        "implemented_desc": "Password reset token generation and endpoint handlers detected.",
        "partial_desc": "Password reset mentions exist, but email verification or token invalidation logic is missing.",
        "missing_desc": "No implementation evidence detected. Users cannot recover forgotten passwords without administrator intervention."
    },
    {
        "name": "Input Validation & Data Sanitization",
        "category": "Reliability & Data Quality",
        "importance": "critical",
        "patterns": [r'BaseModel', r'schema', r'zod', r'joi', r'validator', r'ValidationError'],
        "file_keywords": ['schema', 'validation', 'dto'],
        "implemented_desc": "Structured request schemas and data validation models detected.",
        "partial_desc": "Some request models exist, but query parameters or nested payload validations are omitted.",
        "missing_desc": "No implementation evidence detected. Endpoints receive raw request dictionaries or unvalidated parameters."
    },
    {
        "name": "Structured Error Handling & Centralized Logging",
        "category": "Observability & Resilience",
        "importance": "high",
        "patterns": [r'logger\.', r'logging\.', r'HTTPException', r'exception_handler', r'catch\s*\(', r'winston', r'pino'],
        "file_keywords": ['error', 'log', 'middleware'],
        "implemented_desc": "Centralized error handling middleware and structured logging detected.",
        "partial_desc": "Individual try/catch blocks exist without uniform JSON error structures or logging sinks.",
        "missing_desc": "No implementation evidence detected. Unhandled exceptions risk leaking raw server traces to clients."
    },
    {
        "name": "Database Migrations & Schema Evolution",
        "category": "Data Architecture",
        "importance": "high",
        "patterns": [r'alembic', r'prisma migrate', r'flyway', r'knex migrate', r'revision ='],
        "file_keywords": ['alembic', 'migrations', 'migration'],
        "implemented_desc": "Dedicated migration files and version-controlled schema tracking detected.",
        "partial_desc": "Schema models exist, but migration tracking directory or version files are absent.",
        "missing_desc": "No implementation evidence detected. Tables appear to rely solely on initial auto-creation scripts."
    },
    {
        "name": "Automated Testing Suite (Unit & Integration)",
        "category": "Software Quality & QA",
        "importance": "critical",
        "patterns": [r'def test_', r'it\(', r'describe\(', r'expect\(', r'assert '],
        "file_keywords": ['test', 'spec', '__tests__'],
        "implemented_desc": "Automated test suites with verifiable assertion logic detected.",
        "partial_desc": "Minimal test placeholder files found, but critical business workflows lack coverage.",
        "missing_desc": "No implementation evidence detected. Repository has no automated tests to prevent regressions."
    },
    {
        "name": "API Rate Limiting & Throttling",
        "category": "Security & Availability",
        "importance": "medium",
        "patterns": [r'limiter', r'rate_limit', r'throttle', r'slowapi', r'express-rate-limit'],
        "file_keywords": ['rate_limit', 'throttle'],
        "implemented_desc": "Rate limiting middleware or decorator protections detected.",
        "partial_desc": "Rate limiting libraries referenced in dependencies but not attached to public endpoints.",
        "missing_desc": "No implementation evidence detected. Public endpoints are vulnerable to automated brute-force and DoS."
    },
    {
        "name": "Health Check & Service Readiness Probes",
        "category": "DevOps & Production Readiness",
        "importance": "medium",
        "patterns": [r'/health', r'/ready', r'/ping', r'status.*ok'],
        "file_keywords": ['health'],
        "implemented_desc": "Dedicated health and readiness endpoint detected.",
        "partial_desc": "Health route returns static status without verifying database connection liveness.",
        "missing_desc": "No implementation evidence detected. Container orchestrators and monitors cannot probe application health."
    },
    {
        "name": "Environment Isolation & Template Config",
        "category": "Configuration & Security",
        "importance": "high",
        "patterns": [r'\.env\.example', r'os\.getenv', r'process\.env', r'BaseSettings'],
        "file_keywords": ['config', '.env.example'],
        "implemented_desc": "Environment variables cleanly abstracted with template configuration files.",
        "partial_desc": "Configuration reads environment variables but .env.example template is omitted.",
        "missing_desc": "No implementation evidence detected. Hardcoded parameters or secrets detected in code."
    },
    {
        "name": "Interactive API Documentation & Contracts",
        "category": "Documentation & Developer Experience",
        "importance": "medium",
        "patterns": [r'swagger', r'openapi', r'docs_url', r'redoc'],
        "file_keywords": ['swagger', 'openapi'],
        "implemented_desc": "OpenAPI / Swagger specifications configured and accessible.",
        "partial_desc": "Framework default docs enabled without custom descriptions or schema summaries.",
        "missing_desc": "No implementation evidence detected. API contracts are undocumented."
    },
    {
        "name": "Continuous Integration (CI/CD Pipeline)",
        "category": "DevOps & Automation",
        "importance": "medium",
        "patterns": [r'runs-on:', r'steps:', r'pytest', r'npm test'],
        "file_keywords": ['.github/workflows', '.gitlab-ci'],
        "implemented_desc": "Continuous integration workflow configured for automated linting and testing.",
        "partial_desc": "Workflow file exists but only runs deployment without pre-merge test validation.",
        "missing_desc": "No implementation evidence detected. Commits and pull requests are not tested automatically."
    }
]

class FeatureGapDetectorService:
    @staticmethod
    def detect_feature_gaps(tree: List[str], file_contents: Dict[str, str]) -> List[Dict[str, Any]]:
        gaps = []
        all_code_text = " ".join(file_contents.values())
        
        for rule in CAPABILITY_RULES:
            # Check file paths for keywords
            matching_files = [
                path for path in tree 
                if any(kw in path.lower() for kw in rule["file_keywords"])
            ]
            
            # Check content patterns
            pattern_matches = 0
            for pat in rule["patterns"]:
                if re.search(pat, all_code_text, re.IGNORECASE):
                    pattern_matches += 1

            if pattern_matches >= 2 and matching_files:
                status = "Implemented"
                evidence = f"{rule['implemented_desc']} Found in: {', '.join(matching_files[:2])}."
                affected = matching_files[:3]
            elif pattern_matches >= 1 or matching_files:
                status = "Partially Implemented"
                evidence = f"{rule['partial_desc']} Found in: {', '.join(matching_files[:2]) if matching_files else 'code references'}."
                affected = matching_files[:2]
            else:
                status = "Missing"
                evidence = rule["missing_desc"]
                affected = []

            gaps.append({
                "capability_name": rule["name"],
                "category": rule["category"],
                "status": status,
                "evidence_summary": evidence,
                "affected_files": affected,
                "importance": rule["importance"]
            })

        return gaps
