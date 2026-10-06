import time
from datetime import datetime
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.entities import (
    Repository,
    AnalysisRun,
    CodeFinding,
    FeatureGap,
    RoadmapItem,
    InterviewQuestion
)
from app.schemas.analysis import (
    AnalyzeRepoRequest,
    AnalysisResponse,
    RepositoryDetail,
    CodeFindingSchema,
    FeatureGapSchema,
    RoadmapItemSchema,
    InterviewQuestionSchema,
    CategoryScores,
    ProjectSummary,
    ReadmeAnalysis
)
from app.services.github_service import GitHubService, parse_github_url
from app.services.sample_repos_data import SAMPLE_REPOSITORIES
from app.services.analyzer_service import CodeAnalyzerService
from app.services.security_scanner import SecurityScannerService
from app.services.readme_analyzer import ReadmeAnalyzerService
from app.services.feature_gap_detector import FeatureGapDetectorService
from app.services.scoring_service import ScoringEngineService
from app.services.ai_service import AIService
from app.services.roadmap_service import RoadmapService
from app.services.interview_generator import InterviewGeneratorService

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.get("/sample-repos")
def get_sample_repos():
    """Returns curated repository configurations for 1-click evaluation."""
    samples = []
    for key, data in SAMPLE_REPOSITORIES.items():
        meta = data["metadata"]
        samples.append({
            "key": key,
            "name": meta["name"],
            "owner": meta["owner"]["login"],
            "url": meta["html_url"],
            "description": meta["description"],
            "language": meta["language"],
            "stars": meta["stargazers_count"]
        })
    return samples

@router.post("/run", response_model=AnalysisResponse)
async def run_project_analysis(request: AnalyzeRepoRequest, db: Session = Depends(get_db)):
    """
    Executes complete end-to-end repository ingestion, security audit, code analysis,
    README evaluation, feature gap detection, scoring, roadmap, and viva prep.
    """
    start_time = time.time()
    
    try:
        owner, repo_name = parse_github_url(request.github_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Check if repository matches a sample repo
    sample_key = f"{owner}/{repo_name}"
    if sample_key in SAMPLE_REPOSITORIES:
        ingestion = SAMPLE_REPOSITORIES[sample_key]
    else:
        # Ingest from real GitHub API
        github_svc = GitHubService(token=request.github_token)
        try:
            ingestion = await github_svc.ingest_repository(owner, repo_name, request.branch)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to ingest GitHub repository: {str(e)}")

    tree = ingestion.get("tree", [])
    file_contents = ingestion.get("file_contents", {})
    metadata = ingestion.get("metadata", {})

    # 1. Structural & Framework Analysis
    analysis_result = CodeAnalyzerService.analyze_repository(ingestion)

    # 2. Security Analysis
    security_findings = SecurityScannerService.scan_repository(file_contents)

    # 3. README Analysis
    readme_text = ""
    for path, content in file_contents.items():
        if "readme" in path.lower():
            readme_text = content
            break
    readme_analysis_dict = ReadmeAnalyzerService.analyze_readme(readme_text)

    # 4. Feature Gap Detection
    feature_gaps_list = FeatureGapDetectorService.detect_feature_gaps(tree, file_contents)

    # 5. Deterministic Scoring Engine
    scoring_data = ScoringEngineService.calculate_scores(
        analysis_result=analysis_result,
        security_findings=security_findings,
        readme_analysis=readme_analysis_dict,
        feature_gaps=feature_gaps_list
    )
    overall_score = scoring_data["overall_score"]
    category_scores = scoring_data["category_scores"]

    # 6. AI Summary & Explanations
    project_summary = AIService.generate_project_summary(
        analysis_result=analysis_result,
        readme_analysis=readme_analysis_dict,
        security_findings=security_findings,
        feature_gaps=feature_gaps_list,
        overall_score=overall_score
    )

    # 7. Personalized 6-Phase Roadmap
    roadmap_items_list = RoadmapService.generate_roadmap(
        security_findings=security_findings,
        feature_gaps=feature_gaps_list,
        readme_analysis=readme_analysis_dict,
        analysis_result=analysis_result
    )

    # 8. Project-Specific Interview / Viva Generator
    interview_questions_list = InterviewGeneratorService.generate_interview_questions(
        analysis_result=analysis_result,
        security_findings=security_findings,
        file_contents=file_contents
    )

    execution_duration = round(time.time() - start_time, 2)

    # 9. Database Persistence
    repo_obj = db.query(Repository).filter(
        Repository.owner == owner,
        Repository.repo_name == repo_name
    ).first()

    if not repo_obj:
        repo_obj = Repository(
            github_url=request.github_url,
            owner=owner,
            repo_name=repo_name,
            default_branch=ingestion.get("branch", "main"),
            description=metadata.get("description", ""),
            stars=metadata.get("stargazers_count", 0),
            forks=metadata.get("forks_count", 0),
            primary_language=analysis_result.get("primary_language", "Python"),
            file_count=len(tree),
            last_analyzed_at=datetime.utcnow()
        )
        db.add(repo_obj)
        db.commit()
        db.refresh(repo_obj)
    else:
        repo_obj.last_analyzed_at = datetime.utcnow()
        repo_obj.file_count = len(tree)
        repo_obj.primary_language = analysis_result.get("primary_language", "Python")
        db.commit()

    # Save AnalysisRun
    analysis_run = AnalysisRun(
        repository_id=repo_obj.id,
        status="completed",
        overall_score=overall_score,
        category_scores=category_scores,
        project_summary=project_summary.model_dump(),
        quality_metrics=analysis_result,
        readme_analysis=readme_analysis_dict,
        execution_time_seconds=execution_duration
    )
    db.add(analysis_run)
    db.commit()
    db.refresh(analysis_run)

    # Save Code Findings
    saved_findings = []
    for f in security_findings:
        f_obj = CodeFinding(
            analysis_id=analysis_run.id,
            category=f["category"],
            severity=f["severity"],
            title=f["title"],
            file_path=f["file_path"],
            line_number=f.get("line_number"),
            snippet=f.get("snippet"),
            explanation=f["explanation"],
            recommendation=f["recommendation"],
            cwe_id=f.get("cwe_id")
        )
        db.add(f_obj)
        saved_findings.append(f_obj)

    # Save Feature Gaps
    saved_gaps = []
    for g in feature_gaps_list:
        g_obj = FeatureGap(
            analysis_id=analysis_run.id,
            capability_name=g["capability_name"],
            category=g["category"],
            status=g["status"],
            evidence_summary=g["evidence_summary"],
            affected_files=g.get("affected_files", []),
            importance=g.get("importance", "medium")
        )
        db.add(g_obj)
        saved_gaps.append(g_obj)

    # Save Roadmap Items
    saved_roadmap = []
    for r in roadmap_items_list:
        r_obj = RoadmapItem(
            analysis_id=analysis_run.id,
            phase=r["phase"],
            title=r["title"],
            category=r["category"],
            priority=r["priority"],
            difficulty=r["difficulty"],
            dependencies=r.get("dependencies", []),
            affected_files=r.get("affected_files", []),
            impact=r["impact"],
            action_step=r["action_step"],
            completed=r.get("completed", False)
        )
        db.add(r_obj)
        saved_roadmap.append(r_obj)

    # Save Interview Questions
    saved_questions = []
    for q in interview_questions_list:
        q_obj = InterviewQuestion(
            analysis_id=analysis_run.id,
            category=q["category"],
            difficulty=q["difficulty"],
            question=q["question"],
            expected_answer=q["expected_answer"],
            relevant_file=q.get("relevant_file"),
            follow_up_question=q.get("follow_up_question")
        )
        db.add(q_obj)
        saved_questions.append(q_obj)

    db.commit()

    return AnalysisResponse(
        analysis_id=analysis_run.id,
        repository=RepositoryDetail(
            id=repo_obj.id,
            github_url=repo_obj.github_url,
            owner=repo_obj.owner,
            repo_name=repo_obj.repo_name,
            default_branch=repo_obj.default_branch,
            description=repo_obj.description,
            stars=repo_obj.stars,
            forks=repo_obj.forks,
            primary_language=repo_obj.primary_language,
            file_count=repo_obj.file_count,
            last_analyzed_at=repo_obj.last_analyzed_at
        ),
        status="completed",
        overall_score=overall_score,
        category_scores=CategoryScores(**category_scores),
        project_summary=project_summary,
        quality_metrics=analysis_result,
        readme_analysis=ReadmeAnalysis(**readme_analysis_dict),
        findings=[
            CodeFindingSchema(
                id=f.id,
                category=f.category,
                severity=f.severity,
                title=f.title,
                file_path=f.file_path,
                line_number=f.line_number,
                snippet=f.snippet,
                explanation=f.explanation,
                recommendation=f.recommendation,
                cwe_id=f.cwe_id
            ) for f in saved_findings
        ],
        feature_gaps=[
            FeatureGapSchema(
                id=g.id,
                capability_name=g.capability_name,
                category=g.category,
                status=g.status,
                evidence_summary=g.evidence_summary,
                affected_files=g.affected_files or [],
                importance=g.importance
            ) for g in saved_gaps
        ],
        roadmap_items=[
            RoadmapItemSchema(
                id=r.id,
                phase=r.phase,
                title=r.title,
                category=r.category,
                priority=r.priority,
                difficulty=r.difficulty,
                dependencies=r.dependencies or [],
                affected_files=r.affected_files or [],
                impact=r.impact,
                action_step=r.action_step,
                completed=r.completed
            ) for r in saved_roadmap
        ],
        interview_questions=[
            InterviewQuestionSchema(
                id=q.id,
                category=q.category,
                difficulty=q.difficulty,
                question=q.question,
                expected_answer=q.expected_answer,
                relevant_file=q.relevant_file,
                follow_up_question=q.follow_up_question
            ) for q in saved_questions
        ],
        execution_time_seconds=execution_duration,
        created_at=analysis_run.created_at
    )

@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis_by_id(analysis_id: str, db: Session = Depends(get_db)):
    """Fetch existing analysis report by ID."""
    analysis = db.query(AnalysisRun).filter(AnalysisRun.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis report not found.")

    repo = analysis.repository
    findings = db.query(CodeFinding).filter(CodeFinding.analysis_id == analysis.id).all()
    gaps = db.query(FeatureGap).filter(FeatureGap.analysis_id == analysis.id).all()
    roadmap = db.query(RoadmapItem).filter(RoadmapItem.analysis_id == analysis.id).order_by(RoadmapItem.phase, RoadmapItem.priority).all()
    questions = db.query(InterviewQuestion).filter(InterviewQuestion.analysis_id == analysis.id).all()

    return AnalysisResponse(
        analysis_id=analysis.id,
        repository=RepositoryDetail(
            id=repo.id,
            github_url=repo.github_url,
            owner=repo.owner,
            repo_name=repo.repo_name,
            default_branch=repo.default_branch,
            description=repo.description,
            stars=repo.stars,
            forks=repo.forks,
            primary_language=repo.primary_language,
            file_count=repo.file_count,
            last_analyzed_at=repo.last_analyzed_at
        ),
        status=analysis.status,
        overall_score=analysis.overall_score,
        category_scores=CategoryScores(**analysis.category_scores),
        project_summary=ProjectSummary(**analysis.project_summary),
        quality_metrics=analysis.quality_metrics or {},
        readme_analysis=ReadmeAnalysis(**analysis.readme_analysis),
        findings=[
            CodeFindingSchema(
                id=f.id,
                category=f.category,
                severity=f.severity,
                title=f.title,
                file_path=f.file_path,
                line_number=f.line_number,
                snippet=f.snippet,
                explanation=f.explanation,
                recommendation=f.recommendation,
                cwe_id=f.cwe_id
            ) for f in findings
        ],
        feature_gaps=[
            FeatureGapSchema(
                id=g.id,
                capability_name=g.capability_name,
                category=g.category,
                status=g.status,
                evidence_summary=g.evidence_summary,
                affected_files=g.affected_files or [],
                importance=g.importance
            ) for g in gaps
        ],
        roadmap_items=[
            RoadmapItemSchema(
                id=r.id,
                phase=r.phase,
                title=r.title,
                category=r.category,
                priority=r.priority,
                difficulty=r.difficulty,
                dependencies=r.dependencies or [],
                affected_files=r.affected_files or [],
                impact=r.impact,
                action_step=r.action_step,
                completed=r.completed
            ) for r in roadmap
        ],
        interview_questions=[
            InterviewQuestionSchema(
                id=q.id,
                category=q.category,
                difficulty=q.difficulty,
                question=q.question,
                expected_answer=q.expected_answer,
                relevant_file=q.relevant_file,
                follow_up_question=q.follow_up_question
            ) for q in questions
        ],
        execution_time_seconds=analysis.execution_time_seconds,
        created_at=analysis.created_at
    )
