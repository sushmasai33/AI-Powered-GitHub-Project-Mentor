'use client';

import React, { useState } from 'react';
import { InterviewQuestion } from '@/types';
import { GraduationCap, ChevronDown, ChevronUp, CheckCircle, FileCode, HelpCircle, Sparkles } from 'lucide-react';

interface InterviewTabProps {
  questions: InterviewQuestion[];
}

export default function InterviewTab({ questions }: InterviewTabProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [expandedIds, setExpandedIds] = useState<Record<string, boolean>>({});
  const [practicedIds, setPracticedIds] = useState<Record<string, boolean>>({});

  const categories = ['All', 'Basic', 'Architecture', 'Code', 'Database', 'Security', 'Advanced'];

  const filteredQuestions = questions.filter((q) => {
    if (selectedCategory === 'All') return true;
    return q.category === selectedCategory;
  });

  const toggleExpand = (id: string) => {
    setExpandedIds((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const togglePracticed = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setPracticedIds((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const getDifficultyBadge = (difficulty: string) => {
    switch (difficulty) {
      case 'Beginner':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'Intermediate':
        return 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30';
      case 'Advanced':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      default:
        return 'bg-zinc-800 text-zinc-400 border-zinc-700';
    }
  };

  const practicedCount = Object.values(practicedIds).filter(Boolean).length;

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-zinc-100 flex items-center space-x-2">
            <GraduationCap className="w-5 h-5 text-indigo-400" />
            <span>Project Viva & Technical Interview Simulator</span>
          </h2>
          <p className="text-xs text-zinc-400 mt-0.5">
            Real questions examiners and technical recruiters will ask based on your actual source code, design trade-offs, and weaknesses.
          </p>
        </div>

        <div className="flex items-center space-x-2 bg-zinc-950 px-3.5 py-1.5 rounded-xl border border-zinc-800 text-xs">
          <span className="text-zinc-400">Practiced:</span>
          <span className="font-mono font-bold text-indigo-400">{practicedCount}/{questions.length}</span>
        </div>
      </div>

      {/* Category Pills */}
      <div className="flex flex-wrap gap-1.5">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-3 py-1.5 text-xs rounded-xl font-medium transition-colors cursor-pointer ${
              selectedCategory === cat
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'bg-zinc-900/60 text-zinc-400 hover:text-zinc-200 border border-zinc-800'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Questions List */}
      <div className="space-y-3">
        {filteredQuestions.map((q, idx) => {
          const isExpanded = !!expandedIds[q.id || String(idx)];
          const isPracticed = !!practicedIds[q.id || String(idx)];

          return (
            <div
              key={q.id || idx}
              className={`bg-zinc-900/40 border border-zinc-800 rounded-2xl overflow-hidden transition-all ${
                isPracticed ? 'border-emerald-900/40 bg-zinc-950/40' : 'hover:border-zinc-700/80'
              }`}
            >
              <div
                onClick={() => toggleExpand(q.id || String(idx))}
                className="p-4 flex items-start justify-between gap-4 cursor-pointer select-none"
              >
                <div className="space-y-2 flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="text-xs font-mono font-bold text-indigo-400 bg-indigo-950/40 px-2 py-0.5 rounded border border-indigo-900/40">
                      {q.category}
                    </span>
                    <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${getDifficultyBadge(q.difficulty)}`}>
                      {q.difficulty}
                    </span>
                    {q.relevant_file && (
                      <span className="text-[10px] font-mono text-zinc-500 flex items-center space-x-1">
                        <FileCode className="w-3 h-3" />
                        <span>{q.relevant_file}</span>
                      </span>
                    )}
                  </div>

                  <h3 className="text-sm font-semibold text-zinc-100 leading-snug">
                    {q.question}
                  </h3>
                </div>

                <div className="flex items-center space-x-2 shrink-0">
                  <button
                    onClick={(e) => togglePracticed(q.id || String(idx), e)}
                    className={`px-2.5 py-1 text-[11px] rounded-lg font-medium border flex items-center space-x-1 transition-colors cursor-pointer ${
                      isPracticed
                        ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
                        : 'bg-zinc-800/80 text-zinc-400 hover:text-zinc-200 border-zinc-700/40'
                    }`}
                  >
                    <CheckCircle className="w-3 h-3" />
                    <span>{isPracticed ? 'Practiced' : 'Mark Done'}</span>
                  </button>

                  <button className="text-zinc-500 hover:text-zinc-300 p-1">
                    {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {isExpanded && (
                <div className="px-4 pb-4 pt-1 border-t border-zinc-800/60 bg-zinc-950/60 space-y-3 text-xs">
                  {/* Expected Model Answer */}
                  <div className="p-3.5 bg-zinc-900/80 rounded-xl border border-zinc-800 space-y-1">
                    <div className="text-emerald-400 font-semibold flex items-center space-x-1.5">
                      <Sparkles className="w-3.5 h-3.5" />
                      <span>Model Viva Answer (How to Respond)</span>
                    </div>
                    <p className="text-zinc-300 leading-relaxed pt-1">
                      {q.expected_answer}
                    </p>
                  </div>

                  {/* Follow-up question */}
                  {q.follow_up_question && (
                    <div className="p-3 bg-amber-950/15 rounded-xl border border-amber-900/30 space-y-1">
                      <div className="text-amber-400 font-semibold flex items-center space-x-1.5">
                        <HelpCircle className="w-3.5 h-3.5" />
                        <span>Examiner Follow-up Probe</span>
                      </div>
                      <p className="text-amber-200/90 leading-relaxed italic">
                        &quot;{q.follow_up_question}&quot;
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
