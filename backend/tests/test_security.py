import pytest
from app.services.security_scanner import SecurityScannerService

def test_hardcoded_secret_detection():
    code = {
        "app/config.py": "SECRET_KEY = 'super_secret_jwt_key_1234567890!'\nDEBUG = True"
    }
    findings = SecurityScannerService.scan_repository(code)
    assert len(findings) >= 1
    titles = [f["title"] for f in findings]
    assert any("Hardcoded Secret" in t for t in titles)

def test_sql_injection_detection():
    code = {
        "app/routes/items.py": "query = f'SELECT * FROM users WHERE id = {user_input}'\ndb.execute(query)"
    }
    findings = SecurityScannerService.scan_repository(code)
    assert len(findings) >= 1
    severities = [f["severity"] for f in findings]
    assert "critical" in severities
    cwe_ids = [f["cwe_id"] for f in findings if f.get("cwe_id")]
    assert any("CWE-89" in c for c in cwe_ids)

def test_command_injection_detection():
    code = {
        "app/worker.py": "import os\nos.system('rm -rf ' + user_folder)"
    }
    findings = SecurityScannerService.scan_repository(code)
    assert len(findings) >= 1
    assert any("Arbitrary Command Execution" in f["title"] for f in findings)
