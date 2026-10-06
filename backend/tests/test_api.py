import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

init_db()
client = TestClient(app)

def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_sample_repos_endpoint():
    response = client.get("/api/analysis/sample-repos")
    assert response.status_code == 200
    samples = response.json()
    assert len(samples) >= 2
    assert "fastapi-auth-inventory" in [s["name"] for s in samples]

def test_run_analysis_sample_repo():
    payload = {
        "github_url": "https://github.com/student-dev/fastapi-auth-inventory"
    }
    response = client.post("/api/analysis/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert 0 <= data["overall_score"] <= 100
    assert len(data["findings"]) > 0
    assert len(data["feature_gaps"]) > 0
    assert len(data["roadmap_items"]) > 0
    assert len(data["interview_questions"]) > 0

    analysis_id = data["analysis_id"]
    repo_id = data["repository"]["id"]

    # Test Mentor Chat endpoint
    chat_payload = {
        "repository_id": repo_id,
        "message": "Explain the security vulnerabilities in this repository."
    }
    chat_resp = client.post("/api/mentor/chat", json=chat_payload)
    assert chat_resp.status_code == 200
    chat_data = chat_resp.json()
    assert chat_data["sender"] == "mentor"
    assert "Security Findings Summary" in chat_data["message"]
    assert chat_data["prompt_injection_blocked"] is False

    # Test Roadmap toggle
    roadmap_item_id = data["roadmap_items"][0]["id"]
    toggle_resp = client.post(f"/api/roadmap/item/{roadmap_item_id}/toggle")
    assert toggle_resp.status_code == 200
    assert toggle_resp.json()["completed"] is True
