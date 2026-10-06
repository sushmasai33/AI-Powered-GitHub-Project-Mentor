import pytest
from app.services.feature_gap_detector import FeatureGapDetectorService

def test_feature_gap_detection_logic():
    tree = [
        "README.md",
        "app/main.py",
        "app/auth.py",
        "app/routes/users.py",
        "app/schemas/user.py"
    ]
    file_contents = {
        "app/auth.py": "import jwt\n\ndef login():\n    token = jwt.encode({'sub': 1}, 'sec')\n    return token",
        "app/schemas/user.py": "from pydantic import BaseModel\n\nclass UserSchema(BaseModel):\n    username: str"
    }

    gaps = FeatureGapDetectorService.detect_feature_gaps(tree, file_contents)
    assert len(gaps) > 0

    gap_dict = {g["capability_name"]: g for g in gaps}
    
    # Auth should be Implemented
    assert gap_dict["User Authentication & Authorization"]["status"] in ["Implemented", "Partially Implemented"]

    # Input Validation should be Implemented
    assert gap_dict["Input Validation & Data Sanitization"]["status"] in ["Implemented", "Partially Implemented"]

    # Password Reset should be Missing (no evidence)
    assert gap_dict["Password Reset & Account Recovery"]["status"] == "Missing"
    assert "No implementation evidence detected" in gap_dict["Password Reset & Account Recovery"]["evidence_summary"]
