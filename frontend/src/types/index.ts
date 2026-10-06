export interface Citation {
  file_path: string;
  line_number?: number;
  snippet?: string;
  reason?: string;
}

export interface MentorMessage {
  id?: string;
  sender: 'user' | 'mentor';
  message: string;
  citations: Citation[];
  created_at?: string;
  prompt_injection_blocked?: boolean;
}

export interface CodeFinding {
  id: string;
  category: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  title: string;
  file_path: string;
  line_number?: number;
  snippet?: string;
  explanation: string;
  recommendation: string;
  cwe_id?: string;
}

export interface FeatureGap {
  id: string;
  capability_name: string;
  category: string;
  status: 'Implemented' | 'Partially Implemented' | 'Missing' | 'Cannot Determine';
  evidence_summary: string;
  affected_files: string[];
  importance: 'critical' | 'high' | 'medium' | 'low';
}

export interface RoadmapItem {
  id: string;
  phase: number;
  title: string;
  category: string;
  priority: 'P0' | 'P1' | 'P2' | 'P3';
  difficulty: 'easy' | 'medium' | 'hard';
  dependencies: string[];
  affected_files: string[];
  impact: string;
  action_step: string;
  completed: boolean;
}

export interface InterviewQuestion {
  id: string;
  category: 'Basic' | 'Architecture' | 'Code' | 'Database' | 'Security' | 'Advanced';
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  question: string;
  expected_answer: string;
  relevant_file?: string;
  follow_up_question?: string;
}

export interface CategoryScoreDetail {
  score: number;
  weight: number;
  weighted_score: number;
  indicators: string[];
  strengths: string[];
  weaknesses: string[];
}

export interface CategoryScores {
  code_quality: CategoryScoreDetail;
  security: CategoryScoreDetail;
  testing: CategoryScoreDetail;
  documentation: CategoryScoreDetail;
  architecture: CategoryScoreDetail;
  feature_completeness: CategoryScoreDetail;
  maintainability: CategoryScoreDetail;
}

export interface ProjectSummary {
  overview: string;
  problem_statement: string;
  technologies: {
    languages?: string[];
    frameworks?: string[];
    databases?: string[];
    auth?: string[];
    testing?: string[];
  };
  architecture_type: string;
  architecture_explanation: string;
  main_modules: Array<{ module: string; description: string }>;
  request_workflow: string;
  strengths: string[];
  weaknesses: string[];
  project_maturity: 'Beginner' | 'Developing' | 'Intermediate' | 'Advanced';
  maturity_reasons: string[];
}

export interface ReadmeSectionScore {
  name: string;
  score: number;
  max_score: number;
  status: string;
  feedback: string;
}

export interface ReadmeAnalysis {
  overall_score: number;
  sections: ReadmeSectionScore[];
  missing_sections: string[];
  improvement_recommendations: string[];
}

export interface RepositoryDetail {
  id: string;
  github_url: string;
  owner: string;
  repo_name: string;
  default_branch: string;
  description?: string;
  stars: number;
  forks: number;
  primary_language?: string;
  file_count: number;
  last_analyzed_at?: string;
}

export interface AnalysisResponse {
  analysis_id: string;
  repository: RepositoryDetail;
  status: string;
  overall_score: number;
  category_scores: CategoryScores;
  project_summary: ProjectSummary;
  quality_metrics: Record<string, any>;
  readme_analysis: ReadmeAnalysis;
  findings: CodeFinding[];
  feature_gaps: FeatureGap[];
  roadmap_items: RoadmapItem[];
  interview_questions: InterviewQuestion[];
  execution_time_seconds: number;
  created_at: string;
}

export interface SampleRepo {
  key: string;
  name: string;
  owner: string;
  url: string;
  description: string;
  language: string;
  stars: number;
}
