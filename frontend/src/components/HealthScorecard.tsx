'use client';

import React from 'react';
import { Shield, CheckCircle2, AlertTriangle, FileText, Layers, GitPullRequest, Wrench } from 'lucide-react';
import { CategoryScores, RepositoryDetail } from '@/types';

interface HealthScorecardProps {
  overallScore: number;
  categoryScores: CategoryScores;
  repository: RepositoryDetail;
  executionTimeSeconds: number;
}

export default function HealthScorecard({
  overallScore,
  categoryScores,
  repository,
  executionTimeSeconds,
}: HealthScorecardProps) {
  // Score rating color and label
  const getScoreBadge = (score: number) => {
    if (score >= 80) return { label: 'Strong Quality', bg: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' };
    if (score >= 65) return { label: 'Solid Prototype', bg: 'bg-blue-500/10 text-blue-400 border-blue-500/30' };
    if (score >= 50) return { label: 'Needs Hardening', bg: 'bg-amber-500/10 text-amber-400 border-amber-500/30' };
    return { label: 'Critical Risks Found', bg: 'bg-rose-500/10 text-rose-400 border-rose-500/30' };
  };

  const badge = getScoreBadge(overallScore);

  const categories = [
    { key: 'code_quality', label: 'Code Quality', icon: Layers, data: categoryScores.code_quality },
    { key: 'security', label: 'Security & Safety', icon: Shield, data: categoryScores.security },
    { key: 'testing', label: 'Automated Testing', icon: CheckCircle2, data: categoryScores.testing },
    { key: 'documentation', label: 'Documentation', icon: FileText, data: categoryScores.documentation },
    { key: 'architecture', label: 'Architecture', icon: GitPullRequest, data: categoryScores.architecture },
    { key: 'feature_completeness', label: 'Feature Completeness', icon: Layers, data: categoryScores.feature_completeness },
    { key: 'maintainability', label: 'Maintainability', icon: Wrench, data: categoryScores.maintainability },
  ];

  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl p-6 shadow-xl backdrop-blur-sm space-y-6">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-zinc-800/80 pb-6">
        <div>
          <div className="flex items-center space-x-3 mb-1">
            <h1 className="text-2xl font-bold text-zinc-100">{repository.owner}/{repository.repo_name}</h1>
            <span className={`text-xs font-semibold px-2.5 py-0.5 rounded-full border ${badge.bg}`}>
              {badge.label}
            </span>
          </div>
          <p className="text-sm text-zinc-400 max-w-2xl">
            {repository.description || 'Analyzed software project codebase.'}
          </p>
          <div className="flex flex-wrap items-center gap-4 text-xs text-zinc-500 mt-2 font-mono">
            <span>Branch: <span className="text-zinc-300">{repository.default_branch}</span></span>
            <span>•</span>
            <span>Language: <span className="text-zinc-300">{repository.primary_language || 'Detected'}</span></span>
            <span>•</span>
            <span>Files: <span className="text-zinc-300">{repository.file_count}</span></span>
            <span>•</span>
            <span>Audit Duration: <span className="text-zinc-300">{executionTimeSeconds}s</span></span>
          </div>
        </div>

        {/* Overall Score Circle */}
        <div className="flex items-center space-x-4 bg-zinc-950/70 border border-zinc-800 rounded-2xl p-4 self-stretch md:self-auto justify-between md:justify-start">
          <div>
            <div className="text-xs uppercase tracking-wider text-zinc-400 font-semibold">Project Health</div>
            <div className="text-3xl font-extrabold text-zinc-100">
              {overallScore}<span className="text-sm font-normal text-zinc-500">/100</span>
            </div>
          </div>

          <div className="relative w-14 h-14 flex items-center justify-center">
            <svg className="w-14 h-14 transform -rotate-90" viewBox="0 0 36 36">
              <path
                className="text-zinc-800"
                strokeWidth="3.5"
                stroke="currentColor"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
              <path
                className={overallScore >= 80 ? 'text-emerald-500' : overallScore >= 60 ? 'text-indigo-500' : 'text-amber-500'}
                strokeDasharray={`${overallScore}, 100`}
                strokeWidth="3.5"
                strokeLinecap="round"
                stroke="currentColor"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
            </svg>
            <span className="absolute text-xs font-bold text-zinc-200">{overallScore}%</span>
          </div>
        </div>
      </div>

      {/* Category breakdown bars */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {categories.map(({ key, label, icon: Icon, data }) => (
          <div key={key} className="p-3.5 bg-zinc-950/40 border border-zinc-800/80 rounded-xl space-y-2">
            <div className="flex items-center justify-between text-xs">
              <div className="flex items-center space-x-1.5 text-zinc-300 font-medium">
                <Icon className="w-3.5 h-3.5 text-indigo-400" />
                <span>{label}</span>
              </div>
              <span className="text-zinc-400 font-mono font-bold">{data.score}/100</span>
            </div>

            {/* Progress bar */}
            <div className="w-full bg-zinc-800/80 h-1.5 rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full ${
                  data.score >= 80 ? 'bg-emerald-500' : data.score >= 50 ? 'bg-indigo-500' : 'bg-rose-500'
                }`}
                style={{ width: `${data.score}%` }}
              />
            </div>

            <div className="flex items-center justify-between text-[11px] text-zinc-500">
              <span>Weight: {data.weight}%</span>
              <span>Contrib: {data.weighted_score} pts</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
