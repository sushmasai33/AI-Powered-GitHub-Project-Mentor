'use client';

import React from 'react';
import { ProjectSummary } from '@/types';
import { Layers, Workflow, CheckCircle, AlertCircle, Award, Box, ShieldCheck, Database, Cpu } from 'lucide-react';

interface OverviewTabProps {
  summary: ProjectSummary;
}

export default function OverviewTab({ summary }: OverviewTabProps) {
  return (
    <div className="space-y-6">
      {/* Overview & Problem Statement */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5 space-y-2">
          <div className="flex items-center space-x-2 text-indigo-400 font-semibold text-sm">
            <Box className="w-4 h-4" />
            <span>Project Purpose</span>
          </div>
          <p className="text-zinc-300 text-sm leading-relaxed">{summary.overview}</p>
        </div>

        <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5 space-y-2">
          <div className="flex items-center space-x-2 text-indigo-400 font-semibold text-sm">
            <Cpu className="w-4 h-4" />
            <span>Problem Addressed</span>
          </div>
          <p className="text-zinc-300 text-sm leading-relaxed">{summary.problem_statement}</p>
        </div>
      </div>

      {/* Technologies Detected */}
      <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5 space-y-4">
        <h3 className="text-sm font-semibold text-zinc-100 flex items-center space-x-2">
          <Database className="w-4 h-4 text-indigo-400" />
          <span>Detected Technology Stack</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-3 bg-zinc-950/50 rounded-xl border border-zinc-800/80">
            <div className="text-xs text-zinc-500 font-medium mb-1.5">Languages</div>
            <div className="flex flex-wrap gap-1.5">
              {summary.technologies.languages?.map((lang) => (
                <span key={lang} className="text-xs px-2 py-0.5 rounded bg-zinc-800 text-zinc-200 font-mono">
                  {lang}
                </span>
              ))}
            </div>
          </div>

          <div className="p-3 bg-zinc-950/50 rounded-xl border border-zinc-800/80">
            <div className="text-xs text-zinc-500 font-medium mb-1.5">Frameworks & Web</div>
            <div className="flex flex-wrap gap-1.5">
              {summary.technologies.frameworks && summary.technologies.frameworks.length > 0 ? (
                summary.technologies.frameworks.map((fw) => (
                  <span key={fw} className="text-xs px-2 py-0.5 rounded bg-indigo-950/60 text-indigo-300 border border-indigo-800/40 font-mono">
                    {fw}
                  </span>
                ))
              ) : (
                <span className="text-xs text-zinc-500 italic">None detected</span>
              )}
            </div>
          </div>

          <div className="p-3 bg-zinc-950/50 rounded-xl border border-zinc-800/80">
            <div className="text-xs text-zinc-500 font-medium mb-1.5">Data & Persistence</div>
            <div className="flex flex-wrap gap-1.5">
              {summary.technologies.databases && summary.technologies.databases.length > 0 ? (
                summary.technologies.databases.map((db) => (
                  <span key={db} className="text-xs px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-800/40 font-mono">
                    {db}
                  </span>
                ))
              ) : (
                <span className="text-xs text-zinc-500 italic">None detected</span>
              )}
            </div>
          </div>

          <div className="p-3 bg-zinc-950/50 rounded-xl border border-zinc-800/80">
            <div className="text-xs text-zinc-500 font-medium mb-1.5">Auth & Security</div>
            <div className="flex flex-wrap gap-1.5">
              {summary.technologies.auth && summary.technologies.auth.length > 0 ? (
                summary.technologies.auth.map((a) => (
                  <span key={a} className="text-xs px-2 py-0.5 rounded bg-violet-950/60 text-violet-300 border border-violet-800/40 font-mono">
                    {a}
                  </span>
                ))
              ) : (
                <span className="text-xs text-zinc-500 italic">None detected</span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Architecture & Workflow */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5 space-y-3">
          <h3 className="text-sm font-semibold text-zinc-100 flex items-center space-x-2">
            <Layers className="w-4 h-4 text-indigo-400" />
            <span>Architecture: {summary.architecture_type}</span>
          </h3>
          <p className="text-xs text-zinc-300 leading-relaxed">{summary.architecture_explanation}</p>

          <div className="mt-4 pt-3 border-t border-zinc-800/60">
            <div className="text-xs font-semibold text-zinc-400 mb-2">Main Modules</div>
            <div className="space-y-1.5">
              {summary.main_modules.map((m) => (
                <div key={m.module} className="text-xs flex items-start space-x-2">
                  <span className="font-mono text-indigo-300 bg-indigo-950/40 px-1.5 py-0.5 rounded border border-indigo-900/40">
                    {m.module}/
                  </span>
                  <span className="text-zinc-400">{m.description}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5 space-y-3">
          <h3 className="text-sm font-semibold text-zinc-100 flex items-center space-x-2">
            <Workflow className="w-4 h-4 text-indigo-400" />
            <span>Request Lifecycle Workflow</span>
          </h3>
          <div className="p-3 bg-zinc-950 rounded-xl border border-zinc-800 font-mono text-xs text-zinc-300 leading-relaxed">
            {summary.request_workflow}
          </div>

          <div className="mt-4 pt-3 border-t border-zinc-800/60">
            <div className="flex items-center space-x-2 text-xs font-semibold text-zinc-200 mb-1">
              <Award className="w-4 h-4 text-amber-400" />
              <span>Project Maturity Rating: <span className="text-amber-400 font-bold">{summary.project_maturity}</span></span>
            </div>
            <ul className="text-xs text-zinc-400 space-y-1 list-disc list-inside mt-2">
              {summary.maturity_reasons.map((r, i) => (
                <li key={i}>{r}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Strengths & Weaknesses */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-emerald-950/10 border border-emerald-900/30 rounded-2xl p-5 space-y-3">
          <h3 className="text-sm font-semibold text-emerald-400 flex items-center space-x-2">
            <CheckCircle className="w-4 h-4" />
            <span>Evidence-Supported Strengths</span>
          </h3>
          <ul className="space-y-2 text-xs text-zinc-300">
            {summary.strengths.map((str, i) => (
              <li key={i} className="flex items-start space-x-2">
                <span className="text-emerald-400">•</span>
                <span>{str}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-rose-950/10 border border-rose-900/30 rounded-2xl p-5 space-y-3">
          <h3 className="text-sm font-semibold text-rose-400 flex items-center space-x-2">
            <AlertCircle className="w-4 h-4" />
            <span>Evidence-Supported Weaknesses</span>
          </h3>
          <ul className="space-y-2 text-xs text-zinc-300">
            {summary.weaknesses.map((w, i) => (
              <li key={i} className="flex items-start space-x-2">
                <span className="text-rose-400">•</span>
                <span>{w}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
