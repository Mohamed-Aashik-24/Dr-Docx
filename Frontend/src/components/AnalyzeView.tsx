import React, { useState } from 'react';
import { UploadCloud, Search, File } from 'lucide-react';
import { ClassifiedElement, ElementType } from '../types';

interface AnalyzeViewProps {
  onProcessStart: () => void;
  onProcessComplete: () => void;
  addLog: (msg: string, severity?: 'info'|'success'|'error') => void;
  isProcessing: boolean;
}

export function AnalyzeView({ onProcessStart, onProcessComplete, addLog, isProcessing }: AnalyzeViewProps) {
  const [inputFile, setInputFile] = useState<File | null>(null);
  const [elements, setElements] = useState<ClassifiedElement[]>([]);

  const handleDragOver = (e: React.DragEvent) => e.preventDefault();
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setInputFile(file);
      addLog(`Selected file for analysis: ${file.name}`);
    }
  };

  const getBadgeColor = (type: ElementType) => {
    switch (type) {
      case 'TITLE': return 'bg-purple-100 dark:bg-purple-500/10 text-purple-700 dark:text-purple-400 border-purple-200 dark:border-purple-500/20';
      case 'AUTHOR': return 'bg-pink-100 dark:bg-pink-500/10 text-pink-700 dark:text-pink-400 border-pink-200 dark:border-pink-500/20';
      case 'CHAPTER_HEADING': return 'bg-indigo-100 dark:bg-indigo-500/10 text-indigo-700 dark:text-indigo-400 border-indigo-200 dark:border-indigo-500/20';
      case 'SECTION_HEADING': return 'bg-blue-100 dark:bg-blue-500/10 text-blue-700 dark:text-blue-400 border-blue-200 dark:border-blue-500/20';
      case 'SUBSECTION_HEADING': return 'bg-cyan-100 dark:bg-cyan-500/10 text-cyan-700 dark:text-cyan-400 border-cyan-200 dark:border-cyan-500/20';
      case 'BODY': return 'bg-slate-100 dark:bg-slate-500/10 text-slate-700 dark:text-slate-400 border-slate-200 dark:border-slate-500/20';
      case 'FIGURE':
      case 'FIGURE_CAPTION': return 'bg-orange-100 dark:bg-orange-500/10 text-orange-700 dark:text-orange-400 border-orange-200 dark:border-orange-500/20';
      case 'TABLE':
      case 'TABLE_CAPTION': return 'bg-yellow-100 dark:bg-yellow-500/10 text-yellow-700 dark:text-yellow-400 border-yellow-200 dark:border-yellow-500/20';
      case 'REFERENCE_HEADING':
      case 'REFERENCE_ENTRY': return 'bg-teal-100 dark:bg-teal-500/10 text-teal-700 dark:text-teal-400 border-teal-200 dark:border-teal-500/20';
      case 'LIST_ITEM': return 'bg-emerald-100 dark:bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-500/20';
      case 'BLANK': return 'bg-gray-100 dark:bg-gray-500/10 text-gray-700 dark:text-gray-400 border-gray-200 dark:border-gray-500/20';
      default: return 'bg-slate-100 dark:bg-slate-500/10 text-slate-700 dark:text-slate-400 border-slate-200 dark:border-slate-500/20';
    }
  };

  const runAnalyze = async () => {
    if (!inputFile) return;
    onProcessStart();
    setElements([]);
    addLog('Uploading document for analysis...');
    
    try {
      const formData = new FormData();
      formData.append('file', inputFile);
      
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({ error: 'Server error' }));
        throw new Error(error.error || 'Analysis failed');
      }
      
      const data = await response.json();
      setElements(data.elements);
      addLog(`Analysis complete: ${data.elements.length} elements classified`, 'success');
      onProcessComplete();
    } catch (err: any) {
      addLog(`Error: ${err.message}`, 'error');
      onProcessComplete();
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500 h-full flex flex-col">
      <header className="mb-2 shrink-0">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Analyze Structure</h1>
        <p className="text-slate-600 dark:text-slate-400">Preview how the machine learning model classifies document elements.</p>
      </header>

      <div className="flex gap-4 shrink-0">
        <div 
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          className={`flex-1 border border-dashed rounded-xl p-4 flex items-center gap-4 transition-colors cursor-pointer
            ${inputFile ? 'border-indigo-500/50 bg-indigo-50 dark:bg-indigo-500/5' : 'border-slate-300 dark:border-white/10 hover:border-indigo-500/50 bg-white shadow-sm dark:bg-white/5 dark:shadow-none'}
          `}
        >
          <div className="w-10 h-10 rounded-full bg-slate-100 dark:bg-white/5 flex items-center justify-center shrink-0">
            {inputFile ? <File className="w-5 h-5 text-indigo-500 dark:text-indigo-400" /> : <UploadCloud className="w-5 h-5 text-indigo-500 dark:text-indigo-400" />}
          </div>
          <div className="flex-1">
            <div className="font-medium text-sm text-slate-700 dark:text-slate-200">{inputFile ? inputFile.name : 'Select document for analysis'}</div>
            {!inputFile && <div className="text-xs text-slate-500 mt-0.5">Drag & drop or click to browse</div>}
          </div>
          {!inputFile && (
            <button onClick={() => {
              const input = document.createElement('input');
              input.type = 'file';
              input.accept = '.docx';
              input.onchange = (e: any) => {
                if (e.target.files && e.target.files[0]) {
                  const file = e.target.files[0];
                  setInputFile(file);
                  addLog(`Selected file: ${file.name}`);
                }
              };
              input.click();
            }} className="px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-white/10 hover:bg-slate-200 dark:hover:bg-white/15 text-xs font-bold text-slate-700 dark:text-slate-200 transition-colors">
              Browse
            </button>
          )}
        </div>
        <button 
          onClick={runAnalyze}
          disabled={!inputFile || isProcessing}
          className={`px-6 rounded-xl font-bold text-sm flex items-center justify-center gap-2 transition-all relative overflow-hidden whitespace-nowrap shrink-0 shadow-lg shadow-indigo-600/20
            ${!inputFile ? 'bg-slate-200 dark:bg-white/5 text-slate-400 dark:text-slate-500 cursor-not-allowed' : 
              isProcessing ? 'bg-indigo-600 text-white cursor-wait' : 'bg-indigo-600 hover:bg-indigo-500 text-white'}
          `}
        >
          {isProcessing && (
             <div className="absolute inset-0 w-full h-full">
               <div className="w-1/2 h-full bg-gradient-to-r from-transparent via-white/20 to-transparent skew-x-12 animate-[shimmer_1.5s_infinite]" />
             </div>
          )}
          <Search className="w-4 h-4" />
          Analyze
        </button>
      </div>

      {elements.length > 0 && (
        <div className="flex-1 bg-white shadow-sm dark:bg-white/5 dark:shadow-none rounded-xl border border-slate-200 dark:border-white/10 overflow-hidden flex flex-col min-h-0 animate-in fade-in slide-in-from-bottom-2">
          <div className="overflow-x-auto flex-1">
            <table className="w-full text-left text-sm whitespace-nowrap">
              <thead className="bg-slate-50 dark:bg-white/5 text-slate-500 dark:text-slate-400 text-xs font-bold sticky top-0 border-b border-slate-200 dark:border-white/10">
                <tr>
                  <th className="px-4 py-3 w-12 text-center">#</th>
                  <th className="px-4 py-3 w-48">Type</th>
                  <th className="px-4 py-3 w-24">Source</th>
                  <th className="px-4 py-3 min-w-[200px]">Preview Text</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-white/5 text-slate-700 dark:text-slate-300">
                {elements.map((el, idx) => (
                  <tr key={el.id} className="hover:bg-slate-50 dark:hover:bg-white/[0.02] transition-colors">
                    <td className="px-4 py-3 text-center text-slate-400 dark:text-slate-500 font-mono text-xs">{idx + 1}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2.5 py-1 rounded-md text-[10px] font-bold border tracking-wide ${getBadgeColor(el.type)}`}>
                        {el.type}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span className="text-xs font-mono text-slate-500 dark:text-slate-400">{el.source}</span>
                    </td>
                    <td className="px-4 py-3 text-slate-600 dark:text-slate-400 truncate max-w-[300px]" title={el.text}>
                      {el.text}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
