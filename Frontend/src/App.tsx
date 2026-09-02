import React, { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { ActivityLog } from './components/ActivityLog';
import { FormatView } from './components/FormatView';
import { AnalyzeView } from './components/AnalyzeView';
import { TrainView } from './components/TrainView';
import { SettingsPanel } from './components/SettingsPanel';
import { NavItem, LogEntry, Settings } from './types';

export default function App() {
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  const toggleTheme = () => setTheme(prev => prev === 'dark' ? 'light' : 'dark');

  const [activeNav, setActiveNav] = useState<NavItem>('Format');
  const [isProcessing, setIsProcessing] = useState(false);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [toast, setToast] = useState<{message: string, show: boolean} | null>(null);
  
  const [settings, setSettings] = useState<Settings>({
    font: 'Times New Roman',
    lineSpacing: 1.5,
    marginTop: 1.52,
    marginBottom: 1.52,
    marginLeft: 1.97,
    marginRight: 1.96,
  });

  const addLog = (message: string, severity: LogEntry['severity'] = 'info') => {
    const newLog: LogEntry = {
      id: Math.random().toString(36).slice(2, 11),
      timestamp: new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute:'2-digit', second:'2-digit' }),
      severity,
      message,
    };
    setLogs(prev => [...prev, newLog]);
  };

  const showToast = (message: string) => {
    setToast({ message, show: true });
    setTimeout(() => setToast(prev => prev ? { ...prev, show: false } : null), 3000);
  };

  const handleProcessComplete = () => {
    setIsProcessing(false);
    showToast('Process completed successfully');
  };

  const renderContent = () => {
    switch (activeNav) {
      case 'Format':
        return <FormatView onProcessStart={() => setIsProcessing(true)} onProcessComplete={handleProcessComplete} addLog={addLog} isProcessing={isProcessing} />;
      case 'Analyze':
        return <AnalyzeView onProcessStart={() => setIsProcessing(true)} onProcessComplete={handleProcessComplete} addLog={addLog} isProcessing={isProcessing} />;
      case 'Train Model':
        return <TrainView onProcessStart={() => setIsProcessing(true)} onProcessComplete={handleProcessComplete} addLog={addLog} isProcessing={isProcessing} />;
      case 'Settings':
        return <SettingsPanel settings={settings} onSave={setSettings} addLog={addLog} />;
      default:
        return null;
    }
  };

  return (
    <div className={theme === 'dark' ? 'dark' : ''}>
      <div className="flex h-screen w-full bg-slate-50 dark:bg-[#0F1117] text-slate-900 dark:text-[#E2E8F0] overflow-hidden font-sans selection:bg-indigo-500/30">
        <Sidebar activeNav={activeNav} setActiveNav={setActiveNav} isProcessing={isProcessing} theme={theme} toggleTheme={toggleTheme} />
        
        <main className="flex-1 flex flex-col min-w-0 relative h-full bg-slate-100 dark:bg-[#141721]">
          <div className="flex-1 p-8 overflow-y-auto">
            {renderContent()}
          </div>

          {/* Toast Notification */}
          <div className={`absolute top-6 right-6 transition-all duration-300 transform z-50
            ${toast?.show ? 'translate-y-0 opacity-100' : '-translate-y-4 opacity-0 pointer-events-none'}`}>
            <div className="bg-emerald-100 dark:bg-emerald-500/10 border border-emerald-300 dark:border-emerald-500/20 text-emerald-700 dark:text-emerald-400 px-4 py-3 rounded-xl shadow-lg backdrop-blur-md flex items-center gap-3 font-medium text-sm">
              <div className="w-2 h-2 rounded-full bg-emerald-500 dark:bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.8)]" />
              {toast?.message}
            </div>
          </div>
        </main>

        <ActivityLog logs={logs} onClear={() => setLogs([])} />
      </div>
    </div>
  );
}
