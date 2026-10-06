'use client';

import React, { useState, useEffect, useRef } from 'react';
import { MentorMessage } from '@/types';
import { sendMentorMessage, fetchChatHistory } from '@/lib/api';
import { Send, Bot, User, ShieldCheck, Sparkles, FileCode, AlertTriangle, Loader2 } from 'lucide-react';

interface MentorTabProps {
  repositoryId: string;
}

const PRESET_QUERIES = [
  'Explain the system architecture and request workflow.',
  'What are the critical security vulnerabilities in this project?',
  'What features appear to be missing from the codebase?',
  'Why did the testing score come out so low?',
  'How should I explain this project during my viva examination?'
];

export default function MentorTab({ repositoryId }: MentorTabProps) {
  const [messages, setMessages] = useState<MentorMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchChatHistory(repositoryId).then((history) => {
      if (history.length > 0) {
        setMessages(history);
      } else {
        // Initial greeting
        setMessages([
          {
            sender: 'mentor',
            message: `Hello! I am your AI Project Mentor for this repository. I have analyzed your source files, architecture, security scan, and missing features.\n\nAsk me anything about your project's implementation, weaknesses, or how to explain it in your technical interview or viva.`,
            citations: []
          }
        ]);
      }
    });
  }, [repositoryId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (textToSend?: string) => {
    const text = textToSend || input;
    if (!text.trim() || isLoading) return;

    const userMessage: MentorMessage = {
      sender: 'user',
      message: text,
      citations: []
    };

    setMessages((prev) => [...prev, userMessage]);
    if (!textToSend) setInput('');
    setIsLoading(true);

    try {
      const response = await sendMentorMessage(repositoryId, text);
      setMessages((prev) => [...prev, response]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'mentor',
          message: `⚠️ **Error communicating with AI Mentor**: ${err.message || 'Service temporary unavailable.'}`,
          citations: []
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl flex flex-col h-[700px] overflow-hidden">
      {/* Mentor Chat Header */}
      <div className="p-4 border-b border-zinc-800/80 bg-zinc-950/60 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-xl bg-indigo-600/20 text-indigo-400 border border-indigo-500/30">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-zinc-100 flex items-center space-x-2">
              <span>Repository-Grounded AI Mentor</span>
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
            </h3>
            <p className="text-xs text-zinc-400">Answers verified against actual repository code and AST evidence</p>
          </div>
        </div>

        <div className="flex items-center space-x-1.5 text-xs text-emerald-400 bg-emerald-950/40 border border-emerald-800/40 px-3 py-1 rounded-full">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span className="font-medium text-[11px]">Prompt-Injection Shield Active</span>
        </div>
      </div>

      {/* Suggested Query Chips */}
      <div className="px-4 py-2 bg-zinc-950/40 border-b border-zinc-800/60 flex items-center space-x-2 overflow-x-auto text-xs scrollbar-none">
        <span className="text-zinc-500 font-semibold uppercase text-[10px] shrink-0">Ask:</span>
        {PRESET_QUERIES.map((q) => (
          <button
            key={q}
            onClick={() => handleSend(q)}
            disabled={isLoading}
            className="px-2.5 py-1 rounded-lg bg-zinc-800/80 text-zinc-300 hover:bg-zinc-700/80 border border-zinc-700/40 whitespace-nowrap transition-colors cursor-pointer shrink-0 disabled:opacity-50 text-[11px]"
          >
            {q}
          </button>
        ))}
      </div>

      {/* Messages Stream */}
      <div className="flex-1 p-4 overflow-y-auto space-y-4">
        {messages.map((msg, index) => {
          const isUser = msg.sender === 'user';
          return (
            <div
              key={index}
              className={`flex items-start space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}
            >
              <div
                className={`p-2 rounded-xl shrink-0 ${
                  isUser
                    ? 'bg-zinc-800 text-zinc-200'
                    : 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/30'
                }`}
              >
                {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              <div
                className={`max-w-2xl rounded-2xl p-4 text-xs space-y-2 leading-relaxed ${
                  isUser
                    ? 'bg-indigo-600 text-white rounded-tr-none'
                    : 'bg-zinc-950/90 text-zinc-200 border border-zinc-800 rounded-tl-none'
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.message}</div>

                {/* Evidence Citations */}
                {!isUser && msg.citations && msg.citations.length > 0 && (
                  <div className="mt-3 pt-2.5 border-t border-zinc-800 space-y-1.5">
                    <div className="text-[10px] uppercase font-bold text-zinc-400 flex items-center space-x-1">
                      <FileCode className="w-3 h-3 text-indigo-400" />
                      <span>Verified Repository Citations:</span>
                    </div>
                    {msg.citations.map((cite, cIdx) => (
                      <div
                        key={cIdx}
                        className="p-2 bg-zinc-900 rounded-lg border border-zinc-800/80 text-[11px] font-mono space-y-0.5"
                      >
                        <div className="text-indigo-400 font-semibold">
                          {cite.file_path} {cite.line_number ? `(Line ${cite.line_number})` : ''}
                        </div>
                        {cite.snippet && <div className="text-zinc-400 truncate">{cite.snippet}</div>}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {isLoading && (
          <div className="flex items-start space-x-3">
            <div className="p-2 rounded-xl bg-indigo-600/20 text-indigo-400 border border-indigo-500/30">
              <Bot className="w-4 h-4" />
            </div>
            <div className="p-3 bg-zinc-950 border border-zinc-800 rounded-2xl rounded-tl-none text-xs text-zinc-400 flex items-center space-x-2">
              <Loader2 className="w-3.5 h-3.5 animate-spin text-indigo-400" />
              <span>Analyzing repository context and grounding citations...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input bar */}
      <div className="p-4 border-t border-zinc-800 bg-zinc-950/80">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex space-x-2"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask mentor about code architecture, security risks, or viva questions..."
            className="flex-1 px-4 py-2.5 bg-zinc-900 border border-zinc-800 rounded-xl text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold flex items-center space-x-1.5 transition-colors disabled:opacity-50 cursor-pointer"
          >
            <Send className="w-3.5 h-3.5" />
            <span>Send</span>
          </button>
        </form>
      </div>
    </div>
  );
}
