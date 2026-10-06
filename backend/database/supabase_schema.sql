-- ==============================================================================
-- AI-Powered GitHub Project Mentor: Supabase & PostgreSQL Production Schema
-- ==============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    github_username TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- 2. Repositories Table
CREATE TABLE IF NOT EXISTS repositories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    github_url TEXT NOT NULL,
    owner TEXT NOT NULL,
    repo_name TEXT NOT NULL,
    default_branch TEXT DEFAULT 'main',
    description TEXT,
    stars INTEGER DEFAULT 0,
    forks INTEGER DEFAULT 0,
    is_private BOOLEAN DEFAULT false,
    primary_language TEXT,
    file_count INTEGER DEFAULT 0,
    last_analyzed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    CONSTRAINT uq_repo_owner_name UNIQUE (owner, repo_name)
);

CREATE INDEX IF NOT EXISTS idx_repositories_owner_name ON repositories (owner, repo_name);
CREATE INDEX IF NOT EXISTS idx_repositories_user ON repositories (user_id);

-- 3. Analysis Runs Table
CREATE TABLE IF NOT EXISTS analysis_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    repository_id UUID NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'completed' CHECK (status IN ('queued', 'processing', 'completed', 'failed')),
    overall_score INTEGER CHECK (overall_score >= 0 AND overall_score <= 100),
    category_scores JSONB DEFAULT '{}'::jsonb,
    project_summary JSONB DEFAULT '{}'::jsonb,
    quality_metrics JSONB DEFAULT '{}'::jsonb,
    readme_analysis JSONB DEFAULT '{}'::jsonb,
    execution_time_seconds NUMERIC(6, 2) DEFAULT 0.0,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analysis_runs_repo ON analysis_runs (repository_id);
CREATE INDEX IF NOT EXISTS idx_analysis_runs_created_at ON analysis_runs (created_at DESC);

-- 4. Code & Security Findings Table
CREATE TABLE IF NOT EXISTS code_findings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    analysis_id UUID NOT NULL REFERENCES analysis_runs(id) ON DELETE CASCADE,
    category TEXT NOT NULL CHECK (category IN ('security', 'quality', 'style', 'architecture', 'testing')),
    severity TEXT NOT NULL CHECK (severity IN ('critical', 'high', 'medium', 'low', 'info')),
    title TEXT NOT NULL,
    file_path TEXT NOT NULL,
    line_number INTEGER,
    snippet TEXT,
    explanation TEXT NOT NULL,
    recommendation TEXT NOT NULL,
    cwe_id TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_code_findings_analysis ON code_findings (analysis_id);
CREATE INDEX IF NOT EXISTS idx_code_findings_severity ON code_findings (severity);

-- 5. Feature Gaps Matrix Table
CREATE TABLE IF NOT EXISTS feature_gaps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    analysis_id UUID NOT NULL REFERENCES analysis_runs(id) ON DELETE CASCADE,
    capability_name TEXT NOT NULL,
    category TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Implemented', 'Partially Implemented', 'Missing', 'Cannot Determine')),
    evidence_summary TEXT NOT NULL,
    affected_files TEXT[] DEFAULT '{}',
    importance TEXT NOT NULL DEFAULT 'medium' CHECK (importance IN ('critical', 'high', 'medium', 'low')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_feature_gaps_analysis ON feature_gaps (analysis_id);
CREATE INDEX IF NOT EXISTS idx_feature_gaps_status ON feature_gaps (status);

-- 6. Improvement Roadmap Items Table
CREATE TABLE IF NOT EXISTS roadmap_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    analysis_id UUID NOT NULL REFERENCES analysis_runs(id) ON DELETE CASCADE,
    phase INTEGER NOT NULL CHECK (phase BETWEEN 1 AND 6),
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    priority TEXT NOT NULL CHECK (priority IN ('P0', 'P1', 'P2', 'P3')),
    difficulty TEXT NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard')),
    dependencies TEXT[] DEFAULT '{}',
    affected_files TEXT[] DEFAULT '{}',
    impact TEXT NOT NULL,
    action_step TEXT NOT NULL,
    completed BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_roadmap_items_analysis ON roadmap_items (analysis_id, phase);

-- 7. Mentor Messages (Conversations) Table
CREATE TABLE IF NOT EXISTS mentor_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    repository_id UUID NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    sender TEXT NOT NULL CHECK (sender IN ('user', 'mentor')),
    message TEXT NOT NULL,
    citations JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_mentor_messages_repo ON mentor_messages (repository_id, created_at ASC);

-- 8. Interview / Viva Questions Table
CREATE TABLE IF NOT EXISTS interview_questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    analysis_id UUID NOT NULL REFERENCES analysis_runs(id) ON DELETE CASCADE,
    category TEXT NOT NULL CHECK (category IN ('Basic', 'Architecture', 'Code', 'Database', 'Security', 'Advanced')),
    difficulty TEXT NOT NULL CHECK (difficulty IN ('Beginner', 'Intermediate', 'Advanced')),
    question TEXT NOT NULL,
    expected_answer TEXT NOT NULL,
    relevant_file TEXT,
    follow_up_question TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_interview_questions_analysis ON interview_questions (analysis_id);

-- Row-Level Security (RLS) Configuration
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE repositories ENABLE ROW LEVEL SECURITY;
ALTER TABLE analysis_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE code_findings ENABLE ROW LEVEL SECURITY;
ALTER TABLE feature_gaps ENABLE ROW LEVEL SECURITY;
ALTER TABLE roadmap_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE mentor_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE interview_questions ENABLE ROW LEVEL SECURITY;

-- Allow public read access for demonstration repositories
CREATE POLICY "Public read repositories" ON repositories FOR SELECT USING (true);
CREATE POLICY "Public read analysis" ON analysis_runs FOR SELECT USING (true);
CREATE POLICY "Public read findings" ON code_findings FOR SELECT USING (true);
CREATE POLICY "Public read feature_gaps" ON feature_gaps FOR SELECT USING (true);
CREATE POLICY "Public read roadmap" ON roadmap_items FOR SELECT USING (true);
CREATE POLICY "Public read mentor_messages" ON mentor_messages FOR SELECT USING (true);
CREATE POLICY "Public read interview_questions" ON interview_questions FOR SELECT USING (true);
