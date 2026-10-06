import os
import json
import logging
from typing import Dict, List, Any, Optional
from app.config import settings
from app.schemas.analysis import ProjectSummary

logger = logging.getLogger(__name__)

class AIService:
    @staticmethod
    def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> Optional[str]:
        """
        Calls either NVIDIA NIM (ultra-low latency OpenAI-compatible endpoint)
        or Google Gemini API. Falls back to None if no key is configured or on error.
        """
        # 1. Try NVIDIA NIM API if configured (lowest latency)
        if settings.NVIDIA_API_KEY:
            try:
                import httpx
                headers = {
                    "Authorization": f"Bearer {settings.NVIDIA_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": settings.NVIDIA_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": temperature,
                    "max_tokens": 1024
                }
                with httpx.Client(timeout=30.0) as client:
                    resp = client.post(
                        "https://integrate.api.nvidia.com/v1/chat/completions",
                        headers=headers,
                        json=payload
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        return data["choices"][0]["message"]["content"]
                    else:
                        logger.warning(f"NVIDIA NIM API responded with HTTP {resp.status_code}: {resp.text}")
            except Exception as e:
                logger.warning(f"NVIDIA NIM API call fallback: {e}")

        # 2. Try Gemini API if configured
        if settings.GEMINI_API_KEY:
            try:
                from google import genai
                client = genai.Client(api_key=settings.GEMINI_API_KEY)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"{system_prompt}\n\n{user_prompt}"
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                logger.warning(f"Gemini API call fallback: {e}")

        return None

    @staticmethod
    def generate_project_summary(
        analysis_result: Dict[str, Any],
        readme_analysis: Dict[str, Any],
        security_findings: List[Dict[str, Any]],
        feature_gaps: List[Dict[str, Any]],
        overall_score: int
    ) -> ProjectSummary:
        """
        Generates an evidence-grounded project summary. Uses Google Gemini API if
        GEMINI_API_KEY is configured, or a robust deterministic inference engine
        with verifiable repository facts.
        """
        primary_lang = analysis_result.get("primary_language", "Python")
        frameworks = analysis_result.get("detected_frameworks", ["Custom Framework"])
        databases = analysis_result.get("detected_databases", ["Database"])
        auth_tech = analysis_result.get("detected_auth", [])
        arch_type = analysis_result.get("architecture_type", "Modular Application")
        arch_expl = analysis_result.get("architecture_explanation", "")
        workflow = analysis_result.get("request_workflow", "")
        main_modules = analysis_result.get("main_modules", [])
        has_tests = analysis_result.get("has_tests", False)
        has_docker = analysis_result.get("has_docker", False)
        has_cicd = analysis_result.get("has_cicd", False)

        # Classify maturity based on objective indicators
        maturity = "Beginner"
        maturity_reasons = []

        if overall_score >= 80 and has_tests and (has_docker or has_cicd):
            maturity = "Advanced"
            maturity_reasons.append("Automated test coverage and production containerization/CI pipeline present.")
            maturity_reasons.append("Strict architecture layer separation and documentation.")
        elif overall_score >= 60 and (has_tests or len(frameworks) >= 2):
            maturity = "Intermediate"
            maturity_reasons.append("Structured framework usage and modular directory organization.")
            if not has_tests:
                maturity_reasons.append("Lacks comprehensive automated test suites.")
            else:
                maturity_reasons.append("Testing present but missing full CI/CD deployment automation.")
        elif overall_score >= 40:
            maturity = "Developing"
            maturity_reasons.append("Core business functionality is implemented but security or testing needs work.")
            maturity_reasons.append("Documentation and error-handling mechanisms are partial.")
        else:
            maturity = "Beginner"
            maturity_reasons.append("Initial prototype stage with missing tests, documentation, and error boundaries.")
            maturity_reasons.append("Multiple critical security or architectural gaps identified.")

        # Determine evidence-based strengths
        strengths = []
        if len(frameworks) > 0:
            strengths.append(f"Adopts modern framework tooling ({', '.join(frameworks)}).")
        if len(databases) > 0:
            strengths.append(f"Integrated persistence layer using {', '.join(databases)}.")
        if auth_tech:
            strengths.append(f"User identity managed via {', '.join(auth_tech)}.")
        if has_docker:
            strengths.append("Containerized for reproducible deployments via Docker.")
        if readme_analysis.get("overall_score", 0) >= 60:
            strengths.append("Clear README documentation with setup and usage guides.")
        if not strengths:
            strengths.append("Modular folder organization providing basic separation of code.")

        # Determine evidence-based weaknesses
        weaknesses = []
        if not has_tests:
            weaknesses.append("Zero automated test files detected in repository (high regression risk).")
        if security_findings:
            crit_count = sum(1 for f in security_findings if f["severity"] in ["critical", "high"])
            if crit_count > 0:
                weaknesses.append(f"Identified {crit_count} high/critical security vulnerability risk(s).")
        missing_crucial = [g["capability_name"] for g in feature_gaps if g["status"] == "Missing"]
        if missing_crucial:
            weaknesses.append(f"Missing crucial production capabilities: {', '.join(missing_crucial[:3])}.")
        if not has_cicd:
            weaknesses.append("No automated Continuous Integration (CI) pipeline configured.")
        if not weaknesses:
            weaknesses.append("Further end-to-end load testing and benchmark analysis recommended.")

        overview = (
            f"An application developed in {primary_lang} utilizing "
            f"{', '.join(frameworks) if frameworks else 'native standard libraries'}. "
            f"The codebase is organized as a {arch_type.lower()}."
        )

        problem_stmt = (
            f"Solves the need for structured {primary_lang} web service delivery, "
            f"organizing data management with {', '.join(databases)} and providing endpoint interfaces for client integration."
        )

        # Attempt Gemini call if API key is present
        if settings.GEMINI_API_KEY:
            try:
                from google import genai
                client = genai.Client(api_key=settings.GEMINI_API_KEY)
                prompt = (
                    f"You are an academic software mentor. Provide an objective, evidence-based summary "
                    f"of this repository in JSON format with fields: overview, problem_statement.\n"
                    f"Language: {primary_lang}, Frameworks: {frameworks}, Modules: {[m['module'] for m in main_modules]}.\n"
                    f"DO NOT hallucinate features that are not listed."
                )
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                if response and response.text:
                    clean_text = response.text.strip()
                    if clean_text.startswith("```json"):
                        clean_text = clean_text[7:-3].strip()
                    gemini_json = json.loads(clean_text)
                    if "overview" in gemini_json and "problem_statement" in gemini_json:
                        overview = gemini_json["overview"]
                        problem_stmt = gemini_json["problem_statement"]
            except Exception as e:
                logger.warning(f"Gemini API invocation fallback to deterministic engine: {e}")

        return ProjectSummary(
            overview=overview,
            problem_statement=problem_stmt,
            technologies={
                "languages": [primary_lang] + [k for k in analysis_result.get("language_counts", {}).keys() if k != primary_lang][:3],
                "frameworks": frameworks,
                "databases": databases,
                "auth": auth_tech,
                "testing": analysis_result.get("detected_testing", [])
            },
            architecture_type=arch_type,
            architecture_explanation=arch_expl,
            main_modules=main_modules,
            request_workflow=workflow,
            strengths=strengths,
            weaknesses=weaknesses,
            project_maturity=maturity,
            maturity_reasons=maturity_reasons
        )
