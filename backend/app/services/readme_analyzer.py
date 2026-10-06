import re
from typing import Dict, List, Any

README_CRITERIA = [
    {
        "name": "Project Description",
        "patterns": [r'#\s+', r'overview', r'about', r'introduction'],
        "weight": 10,
        "missing_feedback": "Add a clear high-level description explaining what the application does."
    },
    {
        "name": "Problem Statement",
        "patterns": [r'problem', r'motivation', r'why', r'background', r'purpose'],
        "weight": 10,
        "missing_feedback": "Explain why this project was created and what user problem it solves."
    },
    {
        "name": "Features List",
        "patterns": [r'feature', r'capabilities', r'what it does'],
        "weight": 10,
        "missing_feedback": "Include a bulleted list of completed and functional features."
    },
    {
        "name": "Technology Stack",
        "patterns": [r'tech stack', r'technologies', r'built with', r'requirements', r'stack'],
        "weight": 10,
        "missing_feedback": "List the core languages, frameworks, libraries, and databases utilized."
    },
    {
        "name": "Installation Guide",
        "patterns": [r'installation', r'install', r'setup', r'getting started', r'prerequisites'],
        "weight": 10,
        "missing_feedback": "Provide step-by-step instructions to clone, install dependencies, and run locally."
    },
    {
        "name": "Configuration & Environment",
        "patterns": [r'\.env', r'environment variable', r'configuration', r'config'],
        "weight": 10,
        "missing_feedback": "Document required environment variables (e.g. .env.example) and API keys."
    },
    {
        "name": "Usage & Quickstart",
        "patterns": [r'usage', r'quickstart', r'how to run', r'how to use', r'run'],
        "weight": 10,
        "missing_feedback": "Show how to launch the application and sample commands to interact with it."
    },
    {
        "name": "Architecture / Design",
        "patterns": [r'architecture', r'design', r'flowchart', r'diagram', r'structure'],
        "weight": 10,
        "missing_feedback": "Describe the architectural flow (e.g. client -> API -> database) or include a diagram."
    },
    {
        "name": "API Reference / Endpoints",
        "patterns": [r'api', r'endpoint', r'routes', r'swagger', r'postman'],
        "weight": 10,
        "missing_feedback": "List primary API endpoints with HTTP methods and request/response contracts."
    },
    {
        "name": "License & Contributing",
        "patterns": [r'license', r'contributing', r'author', r'credits'],
        "weight": 10,
        "missing_feedback": "Specify an open-source license (MIT, Apache) and contribution guidelines."
    }
]

class ReadmeAnalyzerService:
    @staticmethod
    def analyze_readme(readme_content: str) -> Dict[str, Any]:
        if not readme_content or not readme_content.strip():
            return {
                "overall_score": 0,
                "sections": [
                    {
                        "name": crit["name"],
                        "score": 0,
                        "max_score": 10,
                        "status": "Missing",
                        "feedback": "No README file detected in the repository root."
                    }
                    for crit in README_CRITERIA
                ],
                "missing_sections": [crit["name"] for crit in README_CRITERIA],
                "improvement_recommendations": [
                    "Create a README.md file in the root directory following standard markdown conventions.",
                    "Document the project's purpose, installation instructions, and core features."
                ]
            }

        sections = []
        total_points = 0
        missing_sections = []
        recommendations = []

        content_lower = readme_content.lower()

        for crit in README_CRITERIA:
            matched = False
            for pat in crit["patterns"]:
                if re.search(pat, content_lower):
                    matched = True
                    break

            if matched:
                score = 8
                # Check for substantial detail under the section
                if len(readme_content) > 1500:
                    score = 10
                elif len(readme_content) > 800:
                    score = 9
                total_points += score
                sections.append({
                    "name": crit["name"],
                    "score": score,
                    "max_score": 10,
                    "status": "Present",
                    "feedback": f"Detected well-documented {crit['name']}."
                })
            else:
                score = 0
                sections.append({
                    "name": crit["name"],
                    "score": score,
                    "max_score": 10,
                    "status": "Missing",
                    "feedback": crit["missing_feedback"]
                })
                missing_sections.append(crit["name"])
                recommendations.append(f"Add a dedicated '{crit['name']}' section: {crit['missing_feedback']}")

        overall_score = min(100, int((total_points / (len(README_CRITERIA) * 10)) * 100))

        return {
            "overall_score": overall_score,
            "sections": sections,
            "missing_sections": missing_sections,
            "improvement_recommendations": recommendations[:6]
        }
