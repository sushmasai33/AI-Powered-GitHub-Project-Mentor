'use client';

import React, { useState } from 'react';
import { CodeFinding } from '@/types';
import { ShieldAlert, ShieldCheck, AlertTriangle, Info, Terminal, CheckCircle2, ChevronDown, ChevronUp } from 'lucide-react';

interface SecurityTabProps {
  findings: CodeFinding[];
}

export default function SecurityTab({ findings }: SecurityTabProps) {
  const [filter, setFilter] = useState<'all' | 'critical' | 'high' | 'medium' | 'low'>('all');
  const [expandedId, setExpandedId] = useState<string | null>(findings[0]?.id || null);

  const filteredFindings = findings.filter((f) => {
    if (filter === 'all') return true;
    return f.severity === filter;
  });

  const criticalCount = findings.filter((f) => f.severity === 'critical').length;
  const highCount = findings.filter((f) => f.severity === 'high').length;
  const mediumCount = findings.filter((f) => f.severity === 'medium').length;
  const lowCount = findings.filter((f) => f.severity === 'low').length;

  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
      case 'high':
        return 'bg-orange-500/10 text-orange-400 border-orange-500/30';
      case 'medium':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      case 'low':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      default:
        return 'bg-zinc-800 text-zinc-400 border-zinc-700';
    }
  };

  return (
    <div className="space-y-6">
      {/* Security Summary Banner */}
      <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-zinc-100 flex items-center space-x-2">
            <ShieldAlert className="w-5 h-5 text-indigo-400" />
            <span>Static Security & Secret Audit</span>
          </h2>
          <p className="text-xs text-zinc-400 mt-0.5">
            Rule-based static analysis detecting hardcoded secrets, injection flaws, and unsafe configuration.
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-1.5 self-stretch sm:self-auto">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1 text-xs rounded-lg font-medium transition-colors cursor-pointer ${
              filter === 'all' ? 'bg-indigo-600 text-white' : 'bg-zinc-800 text-zinc-400 hover:text-zinc-200'
            }`}
          >
            All ({findings.length})
          </button>
          <button
            onClick={() => setFilter('critical')}
            className={`px-3 py-1 text-xs rounded-lg font-medium transition-colors cursor-pointer ${
              filter === 'critical' ? 'bg-rose-600 text-white' : 'bg-zinc-800 text-zinc-400 hover:text-rose-400'
            }`}
          >
            Critical ({criticalCount})
          </button>
          <button
            onClick={() => setFilter('high')}
            className={`px-3 py-1 text-xs rounded-lg font-medium transition-colors cursor-pointer ${
              filter === 'high' ? 'bg-orange-600 text-white' : 'bg-zinc-800 text-zinc-400 hover:text-orange-400'
            }`}
          >
            High ({highCount})
          </button>
          <button
            onClick={() => setFilter('medium')}
            className={`px-3 py-1 text-xs rounded-lg font-medium transition-colors cursor-pointer ${
              filter === 'medium' ? 'bg-amber-600 text-white' : 'bg-zinc-800 text-zinc-400 hover:text-amber-400'
            }`}
          >
            Medium ({mediumCount})
          </button>
        </div>
      </div>

      {filteredFindings.length === 0 ? (
        <div className="p-12 text-center bg-zinc-900/30 border border-zinc-800/80 rounded-2xl">
          <ShieldCheck className="w-12 h-12 text-emerald-400 mx-auto mb-3" />
          <h3 className="text-sm font-semibold text-zinc-200">No {filter !== 'all' ? filter : ''} Security Findings Detected</h3>
          <p className="text-xs text-zinc-400 mt-1 max-w-md mx-auto">
            The scanner did not detect common vulnerabilities matching this filter in repository files.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredFindings.map((finding) => {
            const isExpanded = expandedId === finding.id;
            return (
              <div
                key={finding.id}
                className="bg-zinc-900/50 border border-zinc-800 rounded-xl overflow-hidden transition-all hover:border-zinc-700/80"
              >
                <div
                  onClick={() => setExpandedId(isExpanded ? null : finding.id)}
                  className="p-4 flex items-center justify-between cursor-pointer select-none"
                >
                  <div className="flex items-center space-x-3">
                    <span className={`text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full border ${getSeverityBadge(finding.severity)}`}>
                      {finding.severity}
                    </span>
                    <div>
                      <div className="text-sm font-semibold text-zinc-100">{finding.title}</div>
                      <div className="text-xs text-zinc-500 font-mono mt-0.5">
                        {finding.file_path}{finding.line_number ? ` : Line ${finding.line_number}` : ''}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-3">
                    {finding.cwe_id && (
                      <span className="text-[11px] text-zinc-500 font-mono hidden md:inline-block">
                        {finding.cwe_id}
                      </span>
                    )}
                    <button className="text-zinc-500 hover:text-zinc-300">
                      {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {isExpanded && (
                  <div className="px-4 pb-4 pt-1 border-t border-zinc-800/60 space-y-3 text-xs bg-zinc-950/40">
                    {finding.snippet && (
                      <div>
                        <div className="text-zinc-500 font-semibold mb-1 flex items-center space-x-1.5">
                          <Terminal className="w-3.5 h-3.5 text-zinc-500" />
                          <span>Detected Source Snippet</span>
                        </div>
                        <pre className="p-3 bg-zinc-950 border border-zinc-800 rounded-lg text-rose-300 font-mono overflow-x-auto text-[11px]">
                          <code>{finding.snippet}</code>
                        </pre>
                      </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="p-3 bg-zinc-900/60 rounded-lg border border-zinc-800/80">
                        <div className="font-semibold text-zinc-300 mb-1">Beginner Explanation</div>
                        <p className="text-zinc-400 leading-relaxed">{finding.explanation}</p>
                      </div>

                      <div className="p-3 bg-rose-950/20 rounded-lg border border-rose-900/30">
                        <div className="font-semibold text-rose-300 mb-1">Security Impact</div>
                        <p className="text-rose-200/80 leading-relaxed">{finding.recommendation ? finding.explanation : 'Risk of unauthorized access.'}</p>
                      </div>
                    </div>

                    <div className="p-3 bg-emerald-950/20 rounded-lg border border-emerald-900/30">
                      <div className="font-semibold text-emerald-300 mb-1 flex items-center space-x-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>Recommended Remediation</span>
                      </div>
                      <p className="text-emerald-200/90 leading-relaxed font-mono text-[11px]">
                        {finding.recommendation}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
