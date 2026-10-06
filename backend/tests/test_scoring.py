import pytest
from app.services.scoring_service import ScoringEngineService

def test_scoring_engine_calculation():
    analysis_result = {
        "primary_language": "Python",
        "main_modules": [{"module": "app"}, {"module": "tests"}, {"module": "routes"}],
        "test_files": ["tests/test_app.py", "tests/test_auth.py", "tests/test_db.py"],
        "has_tests": True,
        "has_docker": True,
        "has_cicd": True,
        "architecture_type": "Layered REST API",
        "detected_databases": ["SQLAlchemy", "PostgreSQL"]
    }
    
    security_findings = []  # Clean
    readme_analysis = {"overall_score": 85, "missing_sections": []}
    feature_gaps = [
        {"capability_name": "Auth", "status": "Implemented"},
        {"capability_name": "Validation", "status": "Implemented"},
        {"capability_name": "Tests", "status": "Implemented"},
        {"capability_name": "Health", "status": "Implemented"}
    ]

    scores = ScoringEngineService.calculate_scores(
        analysis_result=analysis_result,
        security_findings=security_findings,
        readme_analysis=readme_analysis,
        feature_gaps=feature_gaps
    )

    overall = scores["overall_score"]
    assert 0 <= overall <= 100
    assert overall >= 80  # Solid repo should score high

    cat = scores["category_scores"]
    assert cat["security"]["score"] == 100
    assert cat["code_quality"]["score"] >= 80
    assert cat["testing"]["score"] >= 80

def test_security_vulnerability_deductions():
    analysis_result = {
        "primary_language": "Python",
        "main_modules": [],
        "test_files": [],
        "has_tests": False,
        "has_docker": False,
        "has_cicd": False,
        "architecture_type": "Unknown",
        "detected_databases": []
    }
    
    # 2 critical findings
    security_findings = [
        {"severity": "critical", "title": "Hardcoded Key"},
        {"severity": "critical", "title": "SQL Injection"}
    ]
    readme_analysis = {"overall_score": 20, "missing_sections": []}
    feature_gaps = [{"capability_name": "Auth", "status": "Missing"}]

    scores = ScoringEngineService.calculate_scores(
        analysis_result=analysis_result,
        security_findings=security_findings,
        readme_analysis=readme_analysis,
        feature_gaps=feature_gaps
    )

    sec_score = scores["category_scores"]["security"]["score"]
    assert sec_score <= 40  # Massive penalty for 2 critical findings
    assert scores["overall_score"] < 50
