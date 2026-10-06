'use client';

import React, { useState } from 'react';
import { Search, Sparkles, Key, GitBranch, ArrowRight, Loader2, Code2, Database } from 'lucide-react';
import { SampleRepo } from '@/types';

interface RepoSelectorProps {
  onAnalyze: (url: string, token?: string, branch?: string) => void;
  isLoading: boolean;
  sampleRepos: SampleRepo[];
}

export default function RepoSelector({ onAnalyze, isLoading, sampleRepos }: RepoSelectorProps) {
  const [url, setUrl] = useState('');
  const [token, setToken] = useState('');
  const [branch, setBranch] = useState('');
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;
    onAnalyze(url.trim(), token.trim() || undefined, branch.trim() || undefined);
  };

  const handleSelectSample = (sampleUrl: string) => {
    setUrl(sampleUrl);
    onAnalyze(sampleUrl);
  };

  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl p-6 shadow-xl backdrop-blur-sm">
      <div className="mb-6">
        <h2 className="text-xl font-bold text-zinc-100 flex items-center space-x-2">
          <span>Connect GitHub Repository</span>
          <span className="text-xs font-normal text-zinc-400 bg-zinc-800/80 px-2 py-0.5 rounded-full border border-zinc-700/50">
            Public or Authenticated
          </span>
        </h2>
        <p className="text-sm text-zinc-400 mt-1">
          Provide a GitHub repository link to inspect source code, verify architecture, test quality, identify missing capabilities, and prepare for project viva.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-zinc-500">
              <Search className="w-5 h-5" />
            </div>
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://github.com/owner/repository"
              className="w-full pl-10 pr-4 py-3 bg-zinc-950 border border-zinc-800 rounded-xl text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all font-mono"
              disabled={isLoading}
            />
          </div>

          <button
            type="submit"
            disabled={isLoading || !url.trim()}
            className="px-6 py-3 bg-gradient-to-r from-indigo-500 to-violet-600 hover:from-indigo-600 hover:to-violet-700 text-white rounded-xl text-sm font-semibold flex items-center justify-center space-x-2 shadow-lg shadow-indigo-500/25 transition-all disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Auditing Project...</span>
              </>
            ) : (
              <>
                <span>Analyze Project</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>

        <div className="flex items-center justify-between text-xs text-zinc-400 pt-1">
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="hover:text-zinc-200 flex items-center space-x-1 cursor-pointer transition-colors"
          >
            <span>{showAdvanced ? 'Hide Advanced Options' : 'Show Advanced Options (Branch & Token)'}</span>
          </button>
          <span>Read-only inspection • No repository modifications</span>
        </div>

        {showAdvanced && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-3 border-t border-zinc-800/80 animate-in fade-in duration-200">
            <div>
              <label className="block text-xs font-medium text-zinc-400 mb-1 flex items-center space-x-1.5">
                <GitBranch className="w-3.5 h-3.5 text-zinc-500" />
                <span>Branch (Optional)</span>
              </label>
              <input
                type="text"
                value={branch}
                onChange={(e) => setBranch(e.target.value)}
                placeholder="main / master"
                className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-lg text-xs text-zinc-100 placeholder-zinc-600 focus:outline-none focus:ring-1 focus:ring-indigo-500 font-mono"
                disabled={isLoading}
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-zinc-400 mb-1 flex items-center space-x-1.5">
                <Key className="w-3.5 h-3.5 text-zinc-500" />
                <span>Personal Access Token (Optional)</span>
              </label>
              <input
                type="password"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                placeholder="ghp_xxxxxxxxxxxx"
                className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-lg text-xs text-zinc-100 placeholder-zinc-600 focus:outline-none focus:ring-1 focus:ring-indigo-500 font-mono"
                disabled={isLoading}
              />
            </div>
          </div>
        )}
      </form>

      {/* 1-Click Curated Sample Repositories */}
      <div className="mt-6 pt-5 border-t border-zinc-800/80">
        <div className="flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-zinc-400 mb-3">
          <Sparkles className="w-3.5 h-3.5 text-amber-400" />
          <span>Or Try 1-Click Evaluation Projects</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {sampleRepos.map((repo) => (
            <div
              key={repo.key}
              onClick={() => !isLoading && handleSelectSample(repo.url)}
              className="p-3.5 rounded-xl border border-zinc-800/90 bg-zinc-950/40 hover:bg-zinc-800/40 hover:border-zinc-700/80 cursor-pointer transition-all group"
            >
              <div className="flex items-center justify-between mb-1.5">
                <div className="font-semibold text-sm text-zinc-200 group-hover:text-indigo-400 transition-colors flex items-center space-x-1.5">
                  <Code2 className="w-4 h-4 text-zinc-500 group-hover:text-indigo-400" />
                  <span>{repo.owner}/{repo.name}</span>
                </div>
                <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-zinc-800/80 text-zinc-300 border border-zinc-700/40">
                  {repo.language}
                </span>
              </div>
              <p className="text-xs text-zinc-400 line-clamp-2">{repo.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
