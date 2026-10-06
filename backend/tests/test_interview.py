import pytest
from app.services.interview_generator import InterviewGeneratorService

def test_interview_generator_categories():
    analysis = {
        "primary_language": "Python",
        "detected_frameworks": ["FastAPI"],
        "detected_databases": ["PostgreSQL"],
        "detected_auth": ["JWT Authentication"],
        "architecture_type": "Layered REST API",
        "main_modules": [{"module": "app", "description": "Core source"}]
    }
    findings = [{"severity": "critical", "file_path": "app/routes/items.py", "title": "SQL Injection"}]
    files = {"app/main.py": "code", "app/database.py": "code"}

    questions = InterviewGeneratorService.generate_interview_questions(analysis, findings, files)
    assert len(questions) >= 8

    categories = {q["category"] for q in questions}
    assert "Basic" in categories
    assert "Architecture" in categories
    assert "Code" in categories
    assert "Database" in categories
    assert "Security" in categories
    assert "Advanced" in categories

    for q in questions:
        assert len(q["question"]) > 15
        assert len(q["expected_answer"]) > 20
        assert q["follow_up_question"] is not None
