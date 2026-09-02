import React, { useState } from 'react';
import { UploadCloud, File, CheckCircle2, Play, Download } from 'lucide-react';

interface FormatViewProps {
  onProcessStart: () => void;
  onProcessComplete: (stats: any) => void;
  addLog: (msg: string, severity?: 'info'|'success'|'error') => void;
  isProcessing: boolean;
}

export function FormatView({ onProcessStart, onProcessComplete, addLog, isProcessing }: FormatViewProps) {
  const [inputFile, setInputFile] = useState<File | null>(null);
  const [outputName, setOutputName] = useState('');
  const [step, setStep] = useState(0);
  const [stats, setStats] = useState<any>(null);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);

  const handleDragOver = (e: React.DragEvent) => e.preventDefault();
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setInputFile(file);
      setOutputName(file.name.replace(/\.[^/.]+$/, "") + "_formatted.docx");
      addLog(`Selected local file: ${file.name}`);
    }
  };

  const runFormat = async () => {
    if (!inputFile) return;
    onProcessStart();
    setStep(1);
    setDownloadUrl(null);
    addLog('Uploading document to backend...');
    
    try {
      const formData = new FormData();
      formData.append('file', inputFile);
      formData.append('output_name', outputName);
      
      setStep(2);
      addLog('Processing document...');
      
      const startTime = Date.now();
      const response = await fetch('/api/format', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({ error: 'Server error' }));
        throw new Error(error.error || 'Format failed');
      }
      
      setStep(3);
      addLog('Formatting complete, preparing download...');
      
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setDownloadUrl(url);
      
      // Auto-download
      const a = document.createElement('a');
      a.href = url;
      a.download = outputName || 'formatted.docx';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      
      setStep(5);
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
      const resultStats = { total: '-', elapsed: `${elapsed}s` };
      setStats(resultStats);
      addLog(`Done in ${elapsed}s → ${outputName}`, 'success');
      onProcessComplete(resultStats);
      
      setTimeout(() => setStep(0), 2000);
    } catch (err: any) {
      addLog(`Error: ${err.message}`, 'error');
      setStep(0);
      onProcessComplete(null);
    }
  };

  const steps = ['Upload', 'Process', 'Format', 'Download'];

  return (
    <div className="max-w-3xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="mb-8">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Format Publication</h1>
        <p className="text-slate-600 dark:text-slate-400">Upload and process your manuscript with ML formatting.</p>
      </header>

      <div className="space-y-6">
        <div 
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          className="bg-white shadow-sm dark:bg-white/5 dark:shadow-none border border-slate-200 dark:border-white/10 rounded-2xl p-8 border-dashed flex flex-col items-center justify-center space-y-4 hover:border-indigo-500/50 transition-colors cursor-pointer group"
        >
          {inputFile ? (
            <div className="flex flex-col items-center gap-3">
              <div className="w-14 h-14 rounded-full bg-indigo-50 dark:bg-indigo-500/10 flex items-center justify-center group-hover:scale-110 transition-transform">
                <File className="w-8 h-8 text-indigo-500 dark:text-indigo-400" />
              </div>
              <div>
                <div className="text-center text-slate-700 dark:text-slate-200 font-medium">{inputFile.name}</div>
                <div className="text-center text-sm text-slate-500 mt-1">Ready to process</div>
              </div>
              <button onClick={() => { setInputFile(null); setDownloadUrl(null); }} className="text-xs text-indigo-500 dark:text-indigo-400 hover:text-indigo-600 dark:hover:text-indigo-300 mt-2">Change file</button>
            </div>
          ) : (
            <div className="flex flex-col items-center gap-3">
              <div className="w-14 h-14 rounded-full bg-indigo-50 dark:bg-indigo-500/10 flex items-center justify-center group-hover:scale-110 transition-transform">
                <UploadCloud className="w-8 h-8 text-indigo-500 dark:text-indigo-400" />
              </div>
              <div>
                <div className="text-center text-slate-700 dark:text-slate-200 font-medium">Drop manuscript here or <span className="text-indigo-500 dark:text-indigo-400">browse</span></div>
                <div className="text-center text-sm text-slate-500 mt-1">Supports .docx</div>
              </div>
              <div className="flex gap-3 mt-4">
                <button onClick={() => {
                  const input = document.createElement('input');
                  input.type = 'file';
                  input.accept = '.docx';
                  input.onchange = (e: any) => {
                    if (e.target.files && e.target.files[0]) {
                      const file = e.target.files[0];
                      setInputFile(file);
                      setOutputName(file.name.replace(/\.[^/.]+$/, "") + "_formatted.docx");
                      addLog(`Selected local file: ${file.name}`);
                    }
                  };
                  input.click();
                }} className="px-4 py-2 rounded-lg bg-slate-100 dark:bg-white/10 hover:bg-slate-200 dark:hover:bg-white/15 text-sm font-medium text-slate-700 dark:text-slate-200 transition-colors">
                  Browse Local
                </button>
              </div>
            </div>
          )}
        </div>

        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className="text-xs font-bold text-slate-500 uppercase px-1">Input File</label>
              <div className="bg-white shadow-sm dark:bg-white/5 dark:shadow-none border border-slate-200 dark:border-white/10 px-4 py-3 rounded-xl text-sm text-slate-700 dark:text-slate-300 truncate">
                {inputFile ? inputFile.name : 'None selected'}
              </div>
            </div>
            <div className="space-y-1.5">
              <label className="text-xs font-bold text-slate-500 uppercase px-1">Output Filename</label>
              <input 
                type="text" 
                value={outputName}
                onChange={(e) => setOutputName(e.target.value)}
                placeholder="e.g. manuscript_formatted.docx"
                className="w-full bg-white shadow-sm dark:bg-white/5 dark:shadow-none border border-slate-200 dark:border-white/10 rounded-xl px-4 py-3 text-sm text-slate-700 dark:text-slate-300 focus:outline-none focus:border-indigo-500/50 transition-all italic"
              />
            </div>
          </div>
        </div>

        <button 
          onClick={runFormat}
          disabled={!inputFile || isProcessing}
          className={`w-full py-4 rounded-xl font-bold text-base flex items-center justify-center gap-3 transition-all relative overflow-hidden shadow-lg shadow-indigo-600/20
            ${!inputFile ? 'bg-slate-100 dark:bg-white/5 text-slate-400 dark:text-slate-500 cursor-not-allowed' : 
              isProcessing ? 'bg-indigo-600 text-white cursor-wait' : 'bg-indigo-600 hover:bg-indigo-500 text-white'}
          `}
        >
          {isProcessing && (
            <div className="absolute inset-0 w-full h-full">
              <div className="w-1/2 h-full bg-gradient-to-r from-transparent via-white/20 to-transparent skew-x-12 animate-[shimmer_1.5s_infinite]" />
            </div>
          )}
          {isProcessing ? (
            <>Processing...</>
          ) : (
            <>
              <Play className="w-5 h-5 fill-current" />
              Format Document
            </>
          )}
        </button>

        {/* Pipeline Visualization */}
        <div className="bg-white shadow-sm dark:bg-white/5 dark:shadow-none border border-slate-200 dark:border-white/10 rounded-2xl p-6">
          <h3 className="text-sm font-bold text-slate-500 dark:text-slate-400 uppercase mb-6">Processing Pipeline</h3>
          <div className="flex items-center justify-between px-8 relative">
            <div className="absolute top-5 left-16 right-16 h-0.5 bg-slate-200 dark:bg-white/10 -z-10">
              <div className="h-full bg-indigo-500 transition-all duration-500" style={{ width: `${Math.max(0, step - 1) * 33.33}%` }} />
            </div>
            
            {steps.map((s, i) => (
              <div key={s} className={`flex flex-col items-center gap-3 ${step > i ? '' : 'opacity-40'}`}>
                <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold transition-all duration-300
                  ${step > i ? 'bg-indigo-500 text-white shadow-lg shadow-indigo-500/30' : 
                    step === i + 1 ? 'bg-indigo-500 text-white ring-4 ring-indigo-500/20' : 
                    'bg-slate-200 text-slate-500 dark:bg-white/10 dark:text-white'}
                `}>
                  {step > i ? <CheckCircle2 className="w-5 h-5" /> : <span>{i + 1}</span>}
                </div>
                <span className="text-xs font-medium text-slate-600 dark:text-slate-300">{s}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Download button if file is ready */}
        {downloadUrl && step === 0 && (
          <a 
            href={downloadUrl} 
            download={outputName || 'formatted.docx'}
            className="w-full py-4 rounded-xl font-bold text-base flex items-center justify-center gap-3 bg-emerald-600 hover:bg-emerald-500 text-white transition-all shadow-lg shadow-emerald-600/20"
          >
            <Download className="w-5 h-5" />
            Download Formatted Document
          </a>
        )}

        {stats && step === 0 && (
          <div className="grid grid-cols-2 gap-4 animate-in fade-in slide-in-from-bottom-2">
            <div className="bg-white shadow-sm dark:bg-white/5 dark:shadow-none p-4 rounded-xl border border-slate-200 dark:border-white/5">
              <div className="text-2xl font-bold text-emerald-500 dark:text-emerald-400">✓</div>
              <div className="text-xs text-slate-500 font-medium uppercase mt-1">Status</div>
            </div>
            <div className="bg-white shadow-sm dark:bg-white/5 dark:shadow-none p-4 rounded-xl border border-slate-200 dark:border-white/5">
              <div className="text-2xl font-bold text-amber-500 dark:text-amber-400">{stats.elapsed}</div>
              <div className="text-xs text-slate-500 font-medium uppercase mt-1">Elapsed Time</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
