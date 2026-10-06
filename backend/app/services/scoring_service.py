from typing import Dict, List, Any

class ScoringEngineService:
    @staticmethod
    def calculate_scores(
        analysis_result: Dict[str, Any],
        security_findings: List[Dict[str, Any]],
        readme_analysis: Dict[str, Any],
        feature_gaps: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculates deterministic and reproducible category and overall project scores.
        Weights:
        - Code Quality: 20%
        - Security: 20%
        - Testing: 15%
        - Documentation: 10%
        - Architecture: 15%
        - Feature Completeness: 15%
        - Maintainability: 5%
        """

        # 1. Code Quality (20%)
        cq_score = 75
        cq_indicators = ["Directory modularity", "Module separation"]
        cq_strengths = []
        cq_weaknesses = []

        if len(analysis_result.get("main_modules", [])) >= 3:
            cq_score += 15
            cq_strengths.append("Clear domain modularity with distinct subdirectories")
        else:
            cq_score -= 15
            cq_weaknesses.append("Flat folder hierarchy without domain modularity")

        if analysis_result.get("primary_language") in ["TypeScript", "Python"]:
            cq_score += 10
            cq_strengths.append(f"Strong typing or static analysis ecosystem ({analysis_result.get('primary_language')})")

        cq_score = max(20, min(100, cq_score))

        # 2. Security (20%)
        sec_score = 100
        sec_indicators = [f"{len(security_findings)} potential vulnerabilities detected"]
        sec_strengths = []
        sec_weaknesses = []

        critical_count = sum(1 for f in security_findings if f["severity"] == "critical")
        high_count = sum(1 for f in security_findings if f["severity"] == "high")
        medium_count = sum(1 for f in security_findings if f["severity"] == "medium")
        low_count = sum(1 for f in security_findings if f["severity"] == "low")

        sec_deduction = (critical_count * 30) + (high_count * 15) + (medium_count * 8) + (low_count * 3)
        sec_score = max(10, 100 - sec_deduction)

        if sec_score >= 85:
            sec_strengths.append("No critical vulnerabilities detected in scanned files")
        else:
            if critical_count > 0:
                sec_weaknesses.append(f"{critical_count} critical severity issue(s) require immediate remediation")
            if high_count > 0:
                sec_weaknesses.append(f"{high_count} high severity risk(s) identified")

        # 3. Testing (15%)
        test_score = 20
        test_indicators = []
        test_strengths = []
        test_weaknesses = []

        test_files = analysis_result.get("test_files", [])
        if len(test_files) == 0:
            test_score = 15
            test_weaknesses.append("No automated test files detected in repository")
            test_indicators.append("0 test files detected")
        elif len(test_files) <= 2:
            test_score = 50
            test_indicators.append(f"{len(test_files)} basic test file(s) found")
            test_weaknesses.append("Minimal test coverage; critical business workflows untested")
        else:
            test_score = 85
            test_indicators.append(f"{len(test_files)} dedicated test files detected")
            test_strengths.append("Automated unit and integration test suites present")

        if analysis_result.get("has_cicd"):
            test_score = min(100, test_score + 15)
            test_strengths.append("Continuous integration (CI) workflow configured")

        # 4. Documentation (10%)
        doc_score = readme_analysis.get("overall_score", 40)
        doc_indicators = [f"README score: {doc_score}/100"]
        doc_strengths = []
        doc_weaknesses = []

        if doc_score >= 70:
            doc_strengths.append("Well-structured README covering setup and usage")
        else:
            doc_weaknesses.append("README is missing essential architecture or setup sections")

        # 5. Architecture (15%)
        arch_score = 65
        arch_indicators = [f"Pattern: {analysis_result.get('architecture_type')}"]
        arch_strengths = []
        arch_weaknesses = []

        if analysis_result.get("has_docker"):
            arch_score += 15
            arch_strengths.append("Containerization configured via Docker")
        else:
            arch_weaknesses.append("No Dockerfile or container specifications found")

        if len(analysis_result.get("detected_databases", [])) > 0:
            arch_score += 10
            arch_strengths.append(f"Structured persistence layer: {', '.join(analysis_result.get('detected_databases'))}")

        arch_score = max(30, min(100, arch_score))

        # 6. Feature Completeness (15%)
        total_gaps = len(feature_gaps)
        if total_gaps > 0:
            impl_count = sum(1 for g in feature_gaps if g["status"] == "Implemented")
            partial_count = sum(1 for g in feature_gaps if g["status"] == "Partially Implemented")
            fc_score = int(((impl_count * 1.0 + partial_count * 0.5) / total_gaps) * 100)
        else:
            fc_score = 60

        fc_indicators = [f"{impl_count}/{total_gaps} expected domain capabilities implemented"]
        fc_strengths = []
        fc_weaknesses = []

        if fc_score >= 75:
            fc_strengths.append("Most expected production features are implemented")
        else:
            fc_weaknesses.append("Key features (e.g. password recovery, rate limiting, validation) missing")

        # 7. Maintainability (5%)
        maint_score = 70
        maint_indicators = ["Package manifests verified"]
        maint_strengths = []
        maint_weaknesses = []

        if analysis_result.get("has_cicd"):
            maint_score += 15
            maint_strengths.append("Automated CI pipeline supports safe refactoring")
        if analysis_result.get("has_docker"):
            maint_score += 15
            maint_strengths.append("Reproducible container runtime environment")

        maint_score = max(30, min(100, maint_score))

        # Weighted calculation
        # Weights: CQ 20%, Sec 20%, Test 15%, Doc 10%, Arch 15%, FC 15%, Maint 5%
        w_cq = cq_score * 0.20
        w_sec = sec_score * 0.20
        w_test = test_score * 0.15
        w_doc = doc_score * 0.10
        w_arch = arch_score * 0.15
        w_fc = fc_score * 0.15
        w_maint = maint_score * 0.05

        overall_score = int(round(w_cq + w_sec + w_test + w_doc + w_arch + w_fc + w_maint))
        overall_score = max(1, min(100, overall_score))

        return {
            "overall_score": overall_score,
            "category_scores": {
                "code_quality": {
                    "score": cq_score,
                    "weight": 20,
                    "weighted_score": round(w_cq, 1),
                    "indicators": cq_indicators,
                    "strengths": cq_strengths,
                    "weaknesses": cq_weaknesses
                },
                "security": {
                    "score": sec_score,
                    "weight": 20,
                    "weighted_score": round(w_sec, 1),
                    "indicators": sec_indicators,
                    "strengths": sec_strengths,
                    "weaknesses": sec_weaknesses
                },
                "testing": {
                    "score": test_score,
                    "weight": 15,
                    "weighted_score": round(w_test, 1),
                    "indicators": test_indicators,
                    "strengths": test_strengths,
                    "weaknesses": test_weaknesses
                },
                "documentation": {
                    "score": doc_score,
                    "weight": 10,
                    "weighted_score": round(w_doc, 1),
                    "indicators": doc_indicators,
                    "strengths": doc_strengths,
                    "weaknesses": doc_weaknesses
                },
                "architecture": {
                    "score": arch_score,
                    "weight": 15,
                    "weighted_score": round(w_arch, 1),
                    "indicators": arch_indicators,
                    "strengths": arch_strengths,
                    "weaknesses": arch_weaknesses
                },
                "feature_completeness": {
                    "score": fc_score,
                    "weight": 15,
                    "weighted_score": round(w_fc, 1),
                    "indicators": fc_indicators,
                    "strengths": fc_strengths,
                    "weaknesses": fc_weaknesses
                },
                "maintainability": {
                    "score": maint_score,
                    "weight": 5,
                    "weighted_score": round(w_maint, 1),
                    "indicators": maint_indicators,
                    "strengths": maint_strengths,
                    "weaknesses": maint_weaknesses
                }
            }
        }
