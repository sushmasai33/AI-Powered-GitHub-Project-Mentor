'use client';

import React, { useState, useEffect } from 'react';
import Header from '@/components/Header';
import RepoSelector from '@/components/RepoSelector';
import HealthScorecard from '@/components/HealthScorecard';
import OverviewTab from '@/components/Tabs/OverviewTab';
import SecurityTab from '@/components/Tabs/SecurityTab';
import ReadmeTab from '@/components/Tabs/ReadmeTab';
import FeatureGapsTab from '@/components/Tabs/FeatureGapsTab';
import RoadmapTab from '@/components/Tabs/RoadmapTab';
import MentorTab from '@/components/Tabs/MentorTab';
import InterviewTab from '@/components/Tabs/InterviewTab';

import { AnalysisResponse, SampleRepo } from '@/types';
import { fetchSampleRepos, runAnalysis } from '@/lib/api';
import {
  Layers,
  ShieldAlert,
  FileText,
  GitPullRequest,
  Bot,
  GraduationCap,
  Sparkles,
  AlertCircle,
  RefreshCw,
  ArrowRight
} from 'lucide-react';

export default function Home() {
  const [sampleRepos, setSampleRepos] = useState<SampleRepo[]>([]);
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<
    'overview' | 'security' | 'feature_gaps' | 'roadmap' | 'readme' | 'mentor' | 'interview'
  >('overview');

  useEffect(() => {
    fetchSampleRepos()
      .then((repos) => {
        setSampleRepos(repos);
        // Automatically analyze first sample repo for instant demonstration if none loaded
        if (repos.length > 0 && !analysis) {
          handleAnalyze(repos[0].url);
        }
      })
      .catch(() => {
        // Fallback sample repos if backend is momentarily booting
        setSampleRepos([
          {
            key: 'student-dev/fastapi-auth-inventory',
            name: 'fastapi-auth-inventory',
            owner: 'student-dev',
            url: 'https://github.com/student-dev/fastapi-auth-inventory',
            description: 'Inventory management API built with FastAPI, SQLAlchemy, and JWT authentication.',
            language: 'Python',
            stars: 14
          }
        ]);
      });
  }, []);

  const handleAnalyze = async (url: string, token?: string, branch?: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await runAnalysis(url, token, branch);
      setAnalysis(data);
      setActiveTab('overview');
    } catch (err: any) {
      setError(err.message || 'Failed to analyze repository. Verify URL and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const tabs = [
    { id: 'overview', label: 'Overview & Summary', icon: Layers },
    {
      id: 'security',
      label: 'Security Audit',
      icon: ShieldAlert,
      badge: analysis?.findings.length ? String(analysis.findings.length) : undefined,
      badgeColor: 'bg-rose-500/20 text-rose-300 border-rose-500/30'
    },
    {
      id: 'feature_gaps',
      label: 'Missing Features Matrix',
      icon: Layers,
      badge: analysis?.feature_gaps.filter((g) => g.status === 'Missing').length
        ? `${analysis?.feature_gaps.filter((g) => g.status === 'Missing').length} Missing`
        : undefined,
      badgeColor: 'bg-amber-500/20 text-amber-300 border-amber-500/30'
    },
    { id: 'roadmap', label: 'Improvement Roadmap', icon: GitPullRequest },
    { id: 'readme', label: 'README Report', icon: FileText },
    { id: 'mentor', label: 'AI Mentor Chat', icon: Bot, isSpecial: true },
    { id: 'interview', label: 'Viva & Interview Prep', icon: GraduationCap }
  ];

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col font-sans">
      <Header />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Repo Input Bar */}
        <RepoSelector
          onAnalyze={handleAnalyze}
          isLoading={isLoading}
          sampleRepos={sampleRepos}
        />

        {/* Error Alert */}
        {error && (
          <div className="p-4 bg-rose-950/30 border border-rose-900/50 rounded-2xl flex items-start space-x-3 text-rose-300 text-xs">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-rose-400" />
            <div className="space-y-1">
              <div className="font-semibold text-rose-200">Analysis Error</div>
              <div>{error}</div>
            </div>
          </div>
        )}

        {/* Analysis Results View */}
        {analysis && (
          <div className="space-y-6 animate-in fade-in duration-300">
            {/* Health Scorecard */}
            <HealthScorecard
              overallScore={analysis.overall_score}
              categoryScores={analysis.category_scores}
              repository={analysis.repository}
              executionTimeSeconds={analysis.execution_time_seconds}
            />

            {/* Quick Actions Strip */}
            <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-2">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                const isActive = activeTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={`p-3 rounded-xl border text-xs font-semibold flex flex-col items-center justify-center space-y-1.5 transition-all cursor-pointer ${
                      isActive
                        ? 'bg-indigo-600 text-white border-indigo-500 shadow-md shadow-indigo-600/25'
                        : 'bg-zinc-900/60 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-850 border-zinc-800/80'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span className="truncate max-w-full text-center">{tab.label}</span>
                    {tab.badge && (
                      <span className={`text-[10px] px-1.5 py-0.2 rounded-full border ${tab.badgeColor}`}>
                        {tab.badge}
                      </span>
                    )}
                  </button>
                );
              })}
            </div>

            {/* Tab Contents */}
            <div className="pt-2">
              {activeTab === 'overview' && <OverviewTab summary={analysis.project_summary} />}
              {activeTab === 'security' && <SecurityTab findings={analysis.findings} />}
              {activeTab === 'feature_gaps' && <FeatureGapsTab featureGaps={analysis.feature_gaps} />}
              {activeTab === 'roadmap' && <RoadmapTab initialRoadmapItems={analysis.roadmap_items} />}
              {activeTab === 'readme' && <ReadmeTab analysis={analysis.readme_analysis} />}
              {activeTab === 'mentor' && <MentorTab repositoryId={analysis.repository.id} />}
              {activeTab === 'interview' && <InterviewTab questions={analysis.interview_questions} />}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-zinc-900 py-6 mt-12 bg-zinc-950/80 text-xs text-zinc-500 text-center">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <div>AI-Powered GitHub Project Mentor • Evidence-Based Academic Intelligence</div>
          <div className="font-mono text-zinc-600">FastAPI + Supabase/PostgreSQL + Next.js 16 + RAG</div>
        </div>
      </footer>
    </div>
  );
}
