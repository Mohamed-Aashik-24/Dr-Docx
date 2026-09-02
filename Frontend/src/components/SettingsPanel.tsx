import React, { useState } from 'react';
import { Save, RefreshCw } from 'lucide-react';
import { Settings } from '../types';

interface SettingsPanelProps {
  settings: Settings;
  onSave: (settings: Settings) => void;
  addLog: (msg: string, severity?: 'info'|'success'|'error') => void;
}

export function SettingsPanel({ settings: initialSettings, onSave, addLog }: SettingsPanelProps) {
  const [settings, setSettings] = useState<Settings>(initialSettings);

  const handleChange = (key: keyof Settings, value: any) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const handleSave = async () => {
    try {
      const response = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings),
      });
      if (!response.ok) {
        const error = await response.json().catch(() => ({ error: 'Server error' }));
        throw new Error(error.error || 'Failed to save settings');
      }
      onSave(settings);
      addLog('Settings saved to backend successfully', 'success');
    } catch (err: any) {
      addLog(`Error saving settings: ${err.message}`, 'error');
    }
  };

  const handleReset = () => {
    const defaultSettings: Settings = {
      font: 'Times New Roman',
      lineSpacing: 1.5,
      marginTop: 1.52,
      marginBottom: 1.52,
      marginLeft: 1.97,
      marginRight: 1.96,
    };
    setSettings(defaultSettings);
    addLog('Settings reset to defaults');
  };

  return (
    <div className="max-w-2xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="mb-8">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Settings</h1>
        <p className="text-slate-600 dark:text-slate-400">Configure document formatting preferences and model thresholds.</p>
      </header>

      <div className="space-y-6">
        <div className="bg-white shadow-sm dark:bg-white/5 dark:shadow-none rounded-xl border border-slate-200 dark:border-white/10 p-6 space-y-6">
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Typography</h3>
          <div className="grid grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 dark:text-slate-400">Default Font</label>
              <select 
                value={settings.font}
                onChange={(e) => handleChange('font', e.target.value)}
                className="w-full bg-slate-50 dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-xl px-4 py-3 text-sm text-slate-700 dark:text-slate-300 focus:outline-none focus:border-indigo-500/50 transition-colors"
              >
                <option value="Times New Roman" className="bg-white dark:bg-[#141721]">Times New Roman</option>
                <option value="Arial" className="bg-white dark:bg-[#141721]">Arial</option>
                <option value="Calibri" className="bg-white dark:bg-[#141721]">Calibri</option>
                <option value="Garamond" className="bg-white dark:bg-[#141721]">Garamond</option>
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 dark:text-slate-400">Line Spacing</label>
              <input 
                type="number" step="0.1" min="1" max="3"
                value={settings.lineSpacing}
                onChange={(e) => handleChange('lineSpacing', parseFloat(e.target.value) || 0)}
                className="w-full bg-slate-50 dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-xl px-4 py-3 text-sm text-slate-700 dark:text-slate-300 focus:outline-none focus:border-indigo-500/50 transition-colors"
              />
            </div>
          </div>
        </div>

        <div className="bg-white shadow-sm dark:bg-white/5 dark:shadow-none rounded-xl border border-slate-200 dark:border-white/10 p-6 space-y-6">
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Page Margins (cm)</h3>
          <div className="grid grid-cols-4 gap-4">
            {['marginTop', 'marginBottom', 'marginLeft', 'marginRight'].map((margin) => (
              <div key={margin} className="space-y-2">
                <label className="text-xs font-bold text-slate-500 dark:text-slate-400 capitalize">{margin.replace('margin', '')}</label>
                <input 
                  type="number" step="0.01"
                  value={settings[margin as keyof Settings]}
                  onChange={(e) => handleChange(margin as keyof Settings, parseFloat(e.target.value) || 0)}
                  className="w-full bg-slate-50 dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-xl px-4 py-3 text-sm text-slate-700 dark:text-slate-300 focus:outline-none focus:border-indigo-500/50 transition-colors"
                />
              </div>
            ))}
          </div>
        </div>

        <div className="flex justify-end gap-3 pt-4">
          <button 
            onClick={handleReset}
            className="px-6 py-3 rounded-xl text-sm font-bold text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-white/5 transition-colors flex items-center gap-2"
          >
            <RefreshCw className="w-4 h-4" />
            Reset Defaults
          </button>
          <button 
            onClick={handleSave}
            className="px-8 py-3 rounded-xl text-sm font-bold bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/20 transition-all flex items-center gap-2"
          >
            <Save className="w-4 h-4" />
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
}
