'use client';

import React, { useState } from 'react';
import { RoadmapItem } from '@/types';
import { toggleRoadmapItem } from '@/lib/api';
import { GitPullRequest, CheckSquare, Square, AlertCircle, ArrowRight, Zap, Shield, FileText } from 'lucide-react';

interface RoadmapTabProps {
  initialRoadmapItems: RoadmapItem[];
}

const PHASE_TITLES: Record<number, { title: string; subtitle: string; icon: any; color: string }> = {
  1: { title: 'Phase 1 — Critical Fixes', subtitle: 'Security vulnerabilities and blocking defects', icon: Shield, color: 'text-rose-400 border-rose-900/40 bg-rose-950/20' },
  2: { title: 'Phase 2 — Quality & Maintainability', subtitle: 'Refactoring, error handling, and schema validation', icon: AlertCircle, color: 'text-orange-400 border-orange-900/40 bg-orange-950/20' },
  3: { title: 'Phase 3 — Automated Testing', subtitle: 'Unit, integration, and critical workflow test suites', icon: CheckSquare, color: 'text-emerald-400 border-emerald-900/40 bg-emerald-950/20' },
  4: { title: 'Phase 4 — Missing Domain Features', subtitle: 'Implementing absent business and user capabilities', icon: GitPullRequest, color: 'text-indigo-400 border-indigo-900/40 bg-indigo-950/20' },
  5: { title: 'Phase 5 — Documentation', subtitle: 'README, architecture diagrams, and API contracts', icon: FileText, color: 'text-blue-400 border-blue-900/40 bg-blue-950/20' },
  6: { title: 'Phase 6 — Advanced Improvements', subtitle: 'Rate limiting, caching, performance, and CI/CD automation', icon: Zap, color: 'text-violet-400 border-violet-900/40 bg-violet-950/20' },
};

export default function RoadmapTab({ initialRoadmapItems }: RoadmapTabProps) {
  const [items, setItems] = useState<RoadmapItem[]>(initialRoadmapItems);
  const [togglingId, setTogglingId] = useState<string | null>(null);

  const handleToggle = async (itemId: string) => {
    setTogglingId(itemId);
    try {
      const res = await toggleRoadmapItem(itemId);
      setItems((prev) =>
        prev.map((item) => (item.id === itemId ? { ...item, completed: res.completed } : item))
      );
    } catch (err) {
      // Local optimistic toggle fallback
      setItems((prev) =>
        prev.map((item) => (item.id === itemId ? { ...item, completed: !item.completed } : item))
      );
    } finally {
      setTogglingId(null);
    }
  };

  const completedCount = items.filter((i) => i.completed).length;
  const totalCount = items.length;
  const progressPercent = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

  // Group items by phase
  const groupedItems = [1, 2, 3, 4, 5, 6].map((phase) => ({
    phase,
    meta: PHASE_TITLES[phase],
    items: items.filter((i) => i.phase === phase),
  }));

  return (
    <div className="space-y-6">
      {/* Header and Progress Card */}
      <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-zinc-100 flex items-center space-x-2">
            <GitPullRequest className="w-5 h-5 text-indigo-400" />
            <span>Personalized Project Improvement Roadmap</span>
          </h2>
          <p className="text-xs text-zinc-400 mt-0.5">
            A 6-phase prioritized action plan to evolve this project into production-ready software.
          </p>
        </div>

        <div className="w-full sm:w-48 bg-zinc-950 p-3 rounded-xl border border-zinc-800 space-y-1.5">
          <div className="flex justify-between text-xs font-medium">
            <span className="text-zinc-400">Roadmap Progress</span>
            <span className="text-indigo-400 font-mono font-bold">{progressPercent}%</span>
          </div>
          <div className="w-full bg-zinc-800 h-2 rounded-full overflow-hidden">
            <div
              className="bg-indigo-500 h-full rounded-full transition-all duration-300"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
          <div className="text-[10px] text-zinc-500 text-right">
            {completedCount} of {totalCount} completed
          </div>
        </div>
      </div>

      {/* 6 Phases Accordion / Groups */}
      <div className="space-y-6">
        {groupedItems.map(({ phase, meta, items: phaseItems }) => {
          if (phaseItems.length === 0) return null;
          const Icon = meta.icon;

          return (
            <div key={phase} className="bg-zinc-900/40 border border-zinc-800 rounded-2xl overflow-hidden">
              <div className={`p-4 border-b border-zinc-800/80 flex items-center justify-between ${meta.color}`}>
                <div className="flex items-center space-x-3">
                  <div className="p-1.5 rounded-lg bg-zinc-950/60 border border-zinc-800/60">
                    <Icon className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-zinc-100">{meta.title}</h3>
                    <p className="text-xs text-zinc-400">{meta.subtitle}</p>
                  </div>
                </div>
                <span className="text-xs font-mono text-zinc-400">
                  {phaseItems.filter((i) => i.completed).length}/{phaseItems.length}
                </span>
              </div>

              <div className="divide-y divide-zinc-800/60">
                {phaseItems.map((item) => (
                  <div
                    key={item.id}
                    onClick={() => handleToggle(item.id)}
                    className={`p-4 flex items-start space-x-3.5 hover:bg-zinc-900/40 transition-colors cursor-pointer ${
                      item.completed ? 'opacity-60 bg-zinc-950/30' : ''
                    }`}
                  >
                    <button className="mt-0.5 text-zinc-500 hover:text-indigo-400 transition-colors">
                      {item.completed ? (
                        <CheckSquare className="w-4 h-4 text-emerald-400" />
                      ) : (
                        <Square className="w-4 h-4 text-zinc-500" />
                      )}
                    </button>

                    <div className="flex-1 space-y-1.5">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <span className={`text-sm font-semibold text-zinc-200 ${item.completed ? 'line-through text-zinc-500' : ''}`}>
                          {item.title}
                        </span>

                        <div className="flex items-center space-x-2">
                          <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded border ${
                            item.priority === 'P0'
                              ? 'bg-rose-500/10 text-rose-400 border-rose-500/20'
                              : 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20'
                          }`}>
                            {item.priority}
                          </span>
                          <span className="text-[10px] uppercase px-2 py-0.5 rounded bg-zinc-800 text-zinc-400 border border-zinc-700/50">
                            {item.difficulty}
                          </span>
                        </div>
                      </div>

                      <p className="text-xs text-zinc-400 leading-relaxed">
                        <strong className="text-zinc-300">Impact:</strong> {item.impact}
                      </p>

                      <div className="p-2.5 bg-zinc-950/70 border border-zinc-800/80 rounded-lg text-xs text-indigo-300 font-mono flex items-start space-x-2">
                        <ArrowRight className="w-3.5 h-3.5 text-indigo-400 shrink-0 mt-0.5" />
                        <span>{item.action_step}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
