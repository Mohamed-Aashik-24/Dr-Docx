import React, { useRef, useEffect, useState } from 'react';
import { Trash2, Download, Minimize2, Maximize2, ChevronRight, ChevronLeft } from 'lucide-react';
import { LogEntry } from '../types';

interface ActivityLogProps {
  logs: LogEntry[];
  onClear: () => void;
}

export function ActivityLog({ logs, onClear }: ActivityLogProps) {
  const endRef = useRef<HTMLDivElement>(null);
  const [isMinimized, setIsMinimized] = useState(false);

  useEffect(() => {
    if (!isMinimized) {
      endRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs, isMinimized]);

  if (isMinimized) {
    return (
      <section className="w-16 flex-shrink-0 flex flex-col items-center bg-white dark:bg-[#0F1117] border-l border-slate-200 dark:border-white/5 h-full py-4 transition-all duration-300">
        <button 
          onClick={() => setIsMinimized(false)}
          className="p-2 hover:bg-slate-100 dark:hover:bg-white/10 rounded-lg text-slate-500 hover:text-slate-900 dark:hover:text-white transition-colors mb-4"
          title="Expand Activity Log"
        >
          <ChevronLeft className="w-5 h-5" />
        </button>
        <div className="flex-1 flex flex-col items-center py-4 text-slate-400 rotate-180" style={{ writingMode: 'vertical-rl' }}>
          <span className="text-xs font-bold uppercase tracking-widest">Activity Log</span>
        </div>
      </section>
    );
  }

  return (
    <section className="w-80 flex-shrink-0 flex flex-col bg-white dark:bg-[#0F1117] border-l border-slate-200 dark:border-white/5 h-full transition-all duration-300">
      <div className="p-6 flex items-center justify-between border-b border-slate-200 dark:border-white/5">
        <div className="flex items-center gap-3">
          <button 
            onClick={() => setIsMinimized(true)}
            className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
            title="Minimize"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
          <h2 className="font-bold text-sm uppercase tracking-wider text-slate-700 dark:text-slate-300">Activity Log</h2>
        </div>
        <button onClick={onClear} className="text-[10px] text-slate-500 font-bold hover:text-slate-800 dark:hover:text-slate-300 transition-colors">CLEAR</button>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-3 font-mono text-xs bg-slate-50 dark:bg-transparent">
        {logs.length === 0 ? (
          <div className="text-slate-500 text-center mt-10">No activity yet.</div>
        ) : (
          logs.map((log) => {
            const getTagInfo = (severity: LogEntry['severity']) => {
              switch (severity) {
                case 'info': return { color: 'text-indigo-600 dark:text-indigo-400', tag: '[INFO]' };
                case 'success': return { color: 'text-emerald-600 dark:text-emerald-400', tag: '[DONE]' };
                case 'error': return { color: 'text-rose-600 dark:text-rose-400', tag: '[ERR ]' };
                case 'warning': return { color: 'text-amber-600 dark:text-amber-400', tag: '[WARN]' };
                default: return { color: 'text-slate-600 dark:text-slate-400', tag: '[LOG ]' };
              }
            };
            const tagInfo = getTagInfo(log.severity);
            return (
              <div key={log.id} className="flex gap-2 leading-relaxed">
                <span className="text-slate-500 dark:text-slate-600 shrink-0">{log.timestamp}</span>
                <span className={`${tagInfo.color} shrink-0`}>{tagInfo.tag}</span>
                <span className="text-slate-700 dark:text-slate-400 break-words">{log.message}</span>
              </div>
            );
          })
        )}
        <div ref={endRef} />
      </div>

      <div className="p-4 border-t border-slate-200 dark:border-white/5">
        <button className="w-full py-2.5 bg-slate-100 hover:bg-slate-200 dark:bg-white/5 dark:hover:bg-white/10 text-slate-700 dark:text-slate-300 text-xs font-bold rounded-lg transition-colors border border-slate-200 dark:border-white/5">
          EXPORT FULL LOG
        </button>
      </div>
    </section>
  );
}
