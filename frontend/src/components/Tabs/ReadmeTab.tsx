'use client';

import React from 'react';
import { ReadmeAnalysis } from '@/types';
import { FileText, CheckCircle2, XCircle, AlertCircle, Sparkles } from 'lucide-react';

interface ReadmeTabProps {
  analysis: ReadmeAnalysis;
}

export default function ReadmeTab({ analysis }: ReadmeTabProps) {
  return (
    <div className="space-y-6">
      {/* README Header Card */}
      <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-zinc-100 flex items-center space-x-2">
            <FileText className="w-5 h-5 text-indigo-400" />
            <span>README Documentation Health Audit</span>
          </h2>
          <p className="text-xs text-zinc-400 mt-0.5">
            Evaluates documentation completeness against academic and industry open-source standards.
          </p>
        </div>

        <div className="flex items-center space-x-3 bg-zinc-950 px-4 py-2 rounded-xl border border-zinc-800">
          <div className="text-xs text-zinc-400">Score:</div>
          <div className="text-xl font-extrabold text-zinc-100">
            {analysis.overall_score}<span className="text-xs font-normal text-zinc-500">/100</span>
          </div>
        </div>
      </div>

      {/* Rubric Evaluation Table */}
      <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl overflow-hidden">
        <div className="px-5 py-3.5 border-b border-zinc-800 bg-zinc-950/40 text-xs font-semibold text-zinc-300">
          Standard Documentation Rubric Breakdown (10 Categories)
        </div>

        <div className="divide-y divide-zinc-800/60">
          {analysis.sections.map((section) => (
            <div key={section.name} className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:bg-zinc-900/30 transition-colors">
              <div className="flex items-start space-x-3">
                {section.status === 'Present' ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                ) : (
                  <XCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                )}
                <div>
                  <div className="text-sm font-medium text-zinc-200">{section.name}</div>
                  <div className="text-xs text-zinc-400 mt-0.5">{section.feedback}</div>
                </div>
              </div>

              <div className="flex items-center space-x-3 self-end sm:self-center">
                <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full border ${
                  section.status === 'Present'
                    ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                    : 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                }`}>
                  {section.status}
                </span>
                <span className="font-mono text-xs font-bold text-zinc-300 w-12 text-right">
                  {section.score}/{section.max_score}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Improvement Recommendations */}
      {analysis.improvement_recommendations.length > 0 && (
        <div className="bg-indigo-950/15 border border-indigo-900/30 rounded-2xl p-5 space-y-3">
          <div className="flex items-center space-x-2 text-indigo-400 font-semibold text-sm">
            <Sparkles className="w-4 h-4" />
            <span>Recommended README Enhancements</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {analysis.improvement_recommendations.map((rec, i) => (
              <div key={i} className="p-3 bg-zinc-950/40 rounded-xl border border-indigo-900/20 text-xs text-zinc-300 flex items-start space-x-2">
                <span className="text-indigo-400 font-bold shrink-0">{i + 1}.</span>
                <span>{rec}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
