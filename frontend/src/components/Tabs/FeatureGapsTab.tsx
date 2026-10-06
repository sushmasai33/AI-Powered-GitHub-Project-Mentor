'use client';

import React, { useState } from 'react';
import { FeatureGap } from '@/types';
import { Layers, CheckCircle2, AlertTriangle, XCircle, HelpCircle, Filter } from 'lucide-react';

interface FeatureGapsTabProps {
  featureGaps: FeatureGap[];
}

export default function FeatureGapsTab({ featureGaps }: FeatureGapsTabProps) {
  const [statusFilter, setStatusFilter] = useState<'All' | 'Missing' | 'Partially Implemented' | 'Implemented'>('All');

  const filteredGaps = featureGaps.filter((g) => {
    if (statusFilter === 'All') return true;
    return g.status === statusFilter;
  });

  const missingCount = featureGaps.filter((g) => g.status === 'Missing').length;
  const partialCount = featureGaps.filter((g) => g.status === 'Partially Implemented').length;
  const implementedCount = featureGaps.filter((g) => g.status === 'Implemented').length;

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'Implemented':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'Partially Implemented':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      case 'Missing':
        return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
      default:
        return 'bg-zinc-800 text-zinc-400 border-zinc-700';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'Implemented':
        return <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />;
      case 'Partially Implemented':
        return <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />;
      case 'Missing':
        return <XCircle className="w-4 h-4 text-rose-400 shrink-0" />;
      default:
        return <HelpCircle className="w-4 h-4 text-zinc-400 shrink-0" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header and Differentiation Banner */}
      <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl p-5 space-y-3">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-base font-bold text-zinc-100 flex items-center space-x-2">
              <Layers className="w-5 h-5 text-indigo-400" />
              <span>Evidence-Based Feature Gap Matrix</span>
            </h2>
            <p className="text-xs text-zinc-400 mt-0.5">
              Audits implemented software capabilities against expected production requirements for this domain archetype.
            </p>
          </div>

          {/* Filter Pills */}
          <div className="flex flex-wrap gap-1.5">
            <button
              onClick={() => setStatusFilter('All')}
              className={`px-3 py-1 text-xs rounded-lg font-medium transition-colors cursor-pointer ${
                statusFilter === 'All' ? 'bg-indigo-600 text-white' : 'bg-zinc-800 text-zinc-400 hover:text-zinc-200'
              }`}
            >
              All ({featureGaps.length})
            </button>
            <button
              onClick={() => setStatusFilter('Missing')}
              className={`px-3 py-1 text-xs rounded-lg font-medium transition-colors cursor-pointer ${
                statusFilter === 'Missing' ? 'bg-rose-600 text-white' : 'bg-zinc-800 text-zinc-400 hover:text-rose-400'
              }`}
            >
              Missing ({missingCount})
            </button>
            <button
              onClick={() => setStatusFilter('Partially Implemented')}
              className={`px-3 py-1 text-xs rounded-lg font-medium transition-colors cursor-pointer ${
                statusFilter === 'Partially Implemented' ? 'bg-amber-600 text-white' : 'bg-zinc-800 text-zinc-400 hover:text-amber-400'
              }`}
            >
              Partial ({partialCount})
            </button>
            <button
              onClick={() => setStatusFilter('Implemented')}
              className={`px-3 py-1 text-xs rounded-lg font-medium transition-colors cursor-pointer ${
                statusFilter === 'Implemented' ? 'bg-emerald-600 text-white' : 'bg-zinc-800 text-zinc-400 hover:text-emerald-400'
              }`}
            >
              Implemented ({implementedCount})
            </button>
          </div>
        </div>

        <div className="p-3 bg-zinc-950/60 rounded-xl border border-zinc-800/80 text-xs text-zinc-400 flex items-center space-x-2">
          <span className="font-semibold text-indigo-400 uppercase tracking-wider text-[10px] shrink-0">Verification Method:</span>
          <span>Checks actual route files, schema validation, database models, and test suites. When no code is found, it explicitly marks: &quot;No implementation evidence detected&quot;.</span>
        </div>
      </div>

      {/* Feature Matrix Table */}
      <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl overflow-hidden">
        <div className="divide-y divide-zinc-800/60">
          {filteredGaps.map((gap) => (
            <div
              key={gap.capability_name}
              className="p-4 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-zinc-900/30 transition-colors"
            >
              <div className="space-y-1 max-w-xl">
                <div className="flex items-center space-x-2.5">
                  {getStatusIcon(gap.status)}
                  <span className="text-sm font-semibold text-zinc-100">{gap.capability_name}</span>
                  <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-zinc-800/80 text-zinc-400 border border-zinc-700/40">
                    {gap.category}
                  </span>
                </div>
                <p className="text-xs text-zinc-400 pl-6 leading-relaxed">
                  {gap.evidence_summary}
                </p>
                {gap.affected_files && gap.affected_files.length > 0 && (
                  <div className="pl-6 pt-1 flex flex-wrap gap-1.5">
                    {gap.affected_files.map((f) => (
                      <span key={f} className="text-[10px] font-mono bg-zinc-950 px-1.5 py-0.5 rounded border border-zinc-800 text-zinc-400">
                        {f}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              <div className="flex items-center space-x-3 self-end md:self-center shrink-0">
                <span className={`text-[11px] font-semibold px-2.5 py-1 rounded-full border ${getStatusBadge(gap.status)}`}>
                  {gap.status}
                </span>
                <span className={`text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded border ${
                  gap.importance === 'critical'
                    ? 'bg-rose-500/10 text-rose-400 border-rose-500/20'
                    : gap.importance === 'high'
                    ? 'bg-orange-500/10 text-orange-400 border-orange-500/20'
                    : 'bg-zinc-800 text-zinc-400 border-zinc-700/50'
                }`}>
                  {gap.importance}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
