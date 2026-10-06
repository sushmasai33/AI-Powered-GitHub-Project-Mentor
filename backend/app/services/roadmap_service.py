from typing import Dict, List, Any

class RoadmapService:
    @staticmethod
    def generate_roadmap(
        security_findings: List[Dict[str, Any]],
        feature_gaps: List[Dict[str, Any]],
        readme_analysis: Dict[str, Any],
        analysis_result: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        items = []

        # -------------------------------------------------------------
        # Phase 1: Critical (Security Vulnerabilities & Blocking Bugs)
        # -------------------------------------------------------------
        for idx, finding in enumerate(security_findings):
            if finding["severity"] in ["critical", "high"]:
                items.append({
                    "phase": 1,
                    "title": f"Fix {finding['title']}",
                    "category": "Security Remediation",
                    "priority": "P0" if finding["severity"] == "critical" else "P1",
                    "difficulty": "medium",
                    "dependencies": [],
                    "affected_files": [finding["file_path"]],
                    "impact": f"Prevents security breach: {finding['explanation']}",
                    "action_step": f"Apply fix at line {finding.get('line_number', 'N/A')}: {finding['recommendation']}",
                    "completed": False
                })

        # If no critical security finding, add environment isolation item
        if not any(item["phase"] == 1 for item in items):
            items.append({
                "phase": 1,
                "title": "Establish Environment Isolation (.env.example)",
                "category": "Security & Config",
                "priority": "P1",
                "difficulty": "easy",
                "dependencies": [],
                "affected_files": [".env.example"],
                "impact": "Eliminates risk of leaking local configuration or production secrets in version control.",
                "action_step": "Create a .env.example template defining all required variables with placeholder values.",
                "completed": False
            })

        # -------------------------------------------------------------
        # Phase 2: Quality & Maintainability
        # -------------------------------------------------------------
        items.append({
            "phase": 2,
            "title": "Implement Centralized Error Handling & Exception Middleware",
            "category": "Code Quality",
            "priority": "P1",
            "difficulty": "medium",
            "dependencies": ["Phase 1"],
            "affected_files": [m["module"] for m in analysis_result.get("main_modules", [])[:2]],
            "impact": "Ensures uniform client error responses and prevents server crashes from unhandled exceptions.",
            "action_step": "Define a global error middleware that catches domain exceptions and returns structured JSON responses.",
            "completed": False
        })
        items.append({
            "phase": 2,
            "title": "Enforce Strict Input Validation Schemas",
            "category": "Code Quality",
            "priority": "P1",
            "difficulty": "easy",
            "dependencies": ["Phase 1"],
            "affected_files": ["routes/", "schemas/"],
            "impact": "Guarantees type safety on incoming payloads and prevents malformed data entering database.",
            "action_step": "Bind Pydantic or validation schemas to all POST/PUT/PATCH endpoints.",
            "completed": False
        })

        # -------------------------------------------------------------
        # Phase 3: Testing & Verification
        # -------------------------------------------------------------
        items.append({
            "phase": 3,
            "title": "Build Automated Unit Test Suite for Business Logic",
            "category": "Automated Testing",
            "priority": "P1",
            "difficulty": "medium",
            "dependencies": ["Phase 2"],
            "affected_files": ["tests/"],
            "impact": "Guarantees core calculation and authentication logic functions as expected during refactors.",
            "action_step": "Create test files covering happy path and edge-case inputs with assertions.",
            "completed": False
        })
        items.append({
            "phase": 3,
            "title": "Add API Integration Endpoint Tests",
            "category": "Automated Testing",
            "priority": "P2",
            "difficulty": "medium",
            "dependencies": ["Unit Test Suite"],
            "affected_files": ["tests/test_api.py"],
            "impact": "Validates full request-response cycles including HTTP status codes and database changes.",
            "action_step": "Use test clients (e.g. TestClient / Supertest) to simulate real user HTTP requests.",
            "completed": False
        })

        # -------------------------------------------------------------
        # Phase 4: Missing Domain Features
        # -------------------------------------------------------------
        missing_gaps = [g for g in feature_gaps if g["status"] == "Missing"]
        for gap in missing_gaps[:3]:
            items.append({
                "phase": 4,
                "title": f"Implement {gap['capability_name']}",
                "category": gap["category"],
                "priority": "P1" if gap["importance"] == "critical" else "P2",
                "difficulty": "hard" if gap["importance"] == "critical" else "medium",
                "dependencies": ["Phase 2", "Phase 3"],
                "affected_files": gap.get("affected_files", []),
                "impact": f"Addresses critical feature gap: {gap['evidence_summary']}",
                "action_step": f"Design endpoints, data models, and logic for {gap['capability_name']}.",
                "completed": False
            })

        # -------------------------------------------------------------
        # Phase 5: Documentation & Presentation
        # -------------------------------------------------------------
        missing_readme = readme_analysis.get("missing_sections", [])
        if missing_readme:
            items.append({
                "phase": 5,
                "title": f"Enrich README with {', '.join(missing_readme[:3])}",
                "category": "Documentation",
                "priority": "P2",
                "difficulty": "easy",
                "dependencies": [],
                "affected_files": ["README.md"],
                "impact": "Significantly improves project legibility for evaluators, recruiters, and contributors.",
                "action_step": "Add missing setup steps, architectural explanation, and sample API payloads to README.md.",
                "completed": False
            })
        else:
            items.append({
                "phase": 5,
                "title": "Add Visual Architecture Diagram to Documentation",
                "category": "Documentation",
                "priority": "P2",
                "difficulty": "easy",
                "dependencies": [],
                "affected_files": ["README.md", "docs/"],
                "impact": "Helps external reviewers quickly understand system components and data flow.",
                "action_step": "Render a Mermaid flowchart or architectural diagram showing client, API, and DB tiers.",
                "completed": False
            })

        # -------------------------------------------------------------
        # Phase 6: Advanced Improvements
        # -------------------------------------------------------------
        items.append({
            "phase": 6,
            "title": "Configure Automated CI/CD Workflow",
            "category": "DevOps & Automation",
            "priority": "P2",
            "difficulty": "medium",
            "dependencies": ["Phase 3"],
            "affected_files": [".github/workflows/ci.yml"],
            "impact": "Automatically runs linting, formatting checks, and test suite on every pull request.",
            "action_step": "Create a GitHub Actions workflow running tests on Ubuntu runner with PostgreSQL/cache services.",
            "completed": False
        })
        items.append({
            "phase": 6,
            "title": "Add Rate Limiting & Response Caching",
            "category": "Performance & Scalability",
            "priority": "P3",
            "difficulty": "medium",
            "dependencies": ["Phase 4"],
            "affected_files": ["app/main.py"],
            "impact": "Hardens API against denial-of-service and decreases database query latency.",
            "action_step": "Integrate rate limiting middleware (e.g. SlowAPI) and in-memory or Redis caching for read endpoints.",
            "completed": False
        })

        return items
