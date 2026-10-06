from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field

class AnalyzeRepoRequest(BaseModel):
    github_url: str = Field(..., description="Full GitHub repository URL e.g. https://github.com/owner/repo")
    github_token: Optional[str] = Field(None, description="Optional GitHub Personal Access Token for private repos or higher rate limits")
    branch: Optional[str] = Field(None, description="Optional branch name, defaults to default branch")

class CitationSchema(BaseModel):
    file_path: str
    line_number: Optional[int] = None
    snippet: Optional[str] = None
    reason: Optional[str] = None

class MentorChatRequest(BaseModel):
    repository_id: str
    message: str

class MentorChatResponse(BaseModel):
    sender: str = "mentor"
    message: str
    citations: List[CitationSchema] = []
    confidence: str = "High confidence"
    prompt_injection_blocked: bool = False

class CodeFindingSchema(BaseModel):
    id: Optional[str] = None
    category: str
    severity: str
    title: str
    file_path: str
    line_number: Optional[int] = None
    snippet: Optional[str] = None
    explanation: str
    recommendation: str
    cwe_id: Optional[str] = None

class FeatureGapSchema(BaseModel):
    id: Optional[str] = None
    capability_name: str
    category: str
    status: str  # Implemented, Partially Implemented, Missing, Cannot Determine
    evidence_summary: str
    affected_files: List[str] = []
    importance: str = "medium"

class RoadmapItemSchema(BaseModel):
    id: Optional[str] = None
    phase: int
    title: str
    category: str
    priority: str
    difficulty: str
    dependencies: List[str] = []
    affected_files: List[str] = []
    impact: str
    action_step: str
    completed: bool = False

class InterviewQuestionSchema(BaseModel):
    id: Optional[str] = None
    category: str  # Basic, Architecture, Code, Database, Security, Advanced
    difficulty: str  # Beginner, Intermediate, Advanced
    question: str
    expected_answer: str
    relevant_file: Optional[str] = None
    follow_up_question: Optional[str] = None

class CategoryScoreDetail(BaseModel):
    score: int
    weight: int
    weighted_score: float
    indicators: List[str] = []
    strengths: List[str] = []
    weaknesses: List[str] = []

class CategoryScores(BaseModel):
    code_quality: CategoryScoreDetail
    security: CategoryScoreDetail
    testing: CategoryScoreDetail
    documentation: CategoryScoreDetail
    architecture: CategoryScoreDetail
    feature_completeness: CategoryScoreDetail
    maintainability: CategoryScoreDetail

class ProjectSummary(BaseModel):
    overview: str
    problem_statement: str
    technologies: Dict[str, List[str]]  # languages, frameworks, databases, tools
    architecture_type: str
    architecture_explanation: str
    main_modules: List[Dict[str, str]]
    request_workflow: str
    strengths: List[str]
    weaknesses: List[str]
    project_maturity: str
    maturity_reasons: List[str]

class ReadmeSectionScore(BaseModel):
    name: str
    score: int  # 0 to 10
    max_score: int = 10
    status: str
    feedback: str

class ReadmeAnalysis(BaseModel):
    overall_score: int
    sections: List[ReadmeSectionScore]
    missing_sections: List[str]
    improvement_recommendations: List[str]

class RepositoryDetail(BaseModel):
    id: str
    github_url: str
    owner: str
    repo_name: str
    default_branch: str
    description: Optional[str] = None
    stars: int = 0
    forks: int = 0
    primary_language: Optional[str] = None
    file_count: int = 0
    last_analyzed_at: Optional[datetime] = None

class AnalysisResponse(BaseModel):
    analysis_id: str
    repository: RepositoryDetail
    status: str
    overall_score: int
    category_scores: CategoryScores
    project_summary: ProjectSummary
    quality_metrics: Dict[str, Any]
    readme_analysis: ReadmeAnalysis
    findings: List[CodeFindingSchema]
    feature_gaps: List[FeatureGapSchema]
    roadmap_items: List[RoadmapItemSchema]
    interview_questions: List[InterviewQuestionSchema]
    execution_time_seconds: float
    created_at: datetime
