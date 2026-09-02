import React, { useState } from 'react';
import { BrainCircuit, Activity, Database, Sparkles } from 'lucide-react';

interface TrainViewProps {
  onProcessStart: () => void;
  onProcessComplete: () => void;
  addLog: (msg: string, severity?: 'info'|'success'|'error') => void;
  isProcessing: boolean;
}

export function TrainView({ onProcessStart, onProcessComplete, addLog, isProcessing }: TrainViewProps) {
  const [results, setResults] = useState<{ accuracy: number, samples: number, features: number } | null>(null);

  const runTrain = async () => {
    onProcessStart();
    setResults(null);
    addLog('Training ML model...');
    
    try {
      const response = await fetch('/api/train', {
        method: 'POST',
      });
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({ error: 'Server error' }));
        throw new Error(error.error || 'Training failed');
      }
      
      const data = await response.json();
      setResults(data);
      addLog(`Training complete! Accuracy: ${(data.accuracy * 100).toFixed(2)}%, Samples: ${data.samples}`, 'success');
      onProcessComplete();
    } catch (err: any) {
      addLog(`Error: ${err.message}`, 'error');
      onProcessComplete();
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="mb-8">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Train Model</h1>
        <p className="text-slate-600 dark:text-slate-400">Retrain the Random Forest classifier using the built-in training dataset.</p>
      </header>

      <div className="bg-white shadow-sm dark:bg-white/5 dark:shadow-none rounded-2xl p-6 border border-slate-200 dark:border-white/10 space-y-6 relative overflow-hidden">
        {/* Background graphic */}
        <div className="absolute -right-12 -top-12 w-64 h-64 bg-indigo-50 dark:bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
        
        <div className="flex gap-4 relative z-10">
          <div className="w-12 h-12 rounded-full bg-indigo-100 dark:bg-indigo-500/20 flex items-center justify-center shrink-0">
            <BrainCircuit className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-800 dark:text-slate-200">Model Retraining</h3>
            <p className="text-sm text-slate-600 dark:text-slate-400 mt-1 leading-relaxed">
              This process extracts TF-IDF features from the curated dataset and retrains the 
              Random Forest ensemble. The new model will immediately be used for future format operations.
            </p>
          </div>
        </div>

        <button 
          onClick={runTrain}
          disabled={isProcessing}
          className={`w-full py-4 rounded-xl font-bold text-base flex items-center justify-center gap-3 transition-all relative overflow-hidden shadow-lg shadow-indigo-600/20
            ${isProcessing ? 'bg-indigo-600 text-white cursor-wait' : 'bg-indigo-600 hover:bg-indigo-500 text-white'}
          `}
        >
          {isProcessing && (
             <div className="absolute inset-0 w-full h-full">
               <div className="w-1/2 h-full bg-gradient-to-r from-transparent via-white/20 to-transparent skew-x-12 animate-[shimmer_1.5s_infinite]" />
             </div>
          )}
          {isProcessing ? (
            <>Processing Dataset...</>
          ) : (
            <>
              <Sparkles className="w-5 h-5 fill-current" />
              Start Training
            </>
          )}
        </button>
      </div>

      {results && (
        <div className="grid grid-cols-3 gap-4 animate-in fade-in slide-in-from-bottom-2">
          <div className="bg-white shadow-sm dark:bg-white/5 dark:shadow-none rounded-xl p-5 border border-slate-200 dark:border-white/10">
            <div className="flex items-center gap-2 text-slate-500 dark:text-slate-400 mb-2">
              <Activity className="w-4 h-4" />
              <span className="text-xs font-bold uppercase tracking-wider">Accuracy</span>
            </div>
            <div className="text-3xl font-bold text-emerald-600 dark:text-emerald-400">{(results.accuracy * 100).toFixed(2)}%</div>
          </div>
          <div className="bg-white shadow-sm dark:bg-white/5 dark:shadow-none rounded-xl p-5 border border-slate-200 dark:border-white/10">
            <div className="flex items-center gap-2 text-slate-500 dark:text-slate-400 mb-2">
              <Database className="w-4 h-4" />
              <span className="text-xs font-bold uppercase tracking-wider">Samples</span>
            </div>
            <div className="text-3xl font-bold text-slate-800 dark:text-white">{results.samples}</div>
          </div>
          <div className="bg-white shadow-sm dark:bg-white/5 dark:shadow-none rounded-xl p-5 border border-slate-200 dark:border-white/10">
            <div className="flex items-center gap-2 text-slate-500 dark:text-slate-400 mb-2">
              <BrainCircuit className="w-4 h-4" />
              <span className="text-xs font-bold uppercase tracking-wider">Features</span>
            </div>
            <div className="text-3xl font-bold text-slate-800 dark:text-white">{results.features}</div>
          </div>
        </div>
      )}
    </div>
  );
}
