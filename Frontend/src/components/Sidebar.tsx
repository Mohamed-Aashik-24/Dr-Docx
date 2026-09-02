import React from 'react';
import { FileText, Search, Activity, Settings as SettingsIcon, Sun, Moon } from 'lucide-react';
import { NavItem } from '../types';

interface SidebarProps {
  activeNav: NavItem;
  setActiveNav: (nav: NavItem) => void;
  isProcessing: boolean;
  theme: 'dark' | 'light';
  toggleTheme: () => void;
}

export function Sidebar({ activeNav, setActiveNav, isProcessing, theme, toggleTheme }: SidebarProps) {
  const navItems = [
    { name: 'Format' as NavItem, icon: FileText },
    { name: 'Analyze' as NavItem, icon: Search },
    { name: 'Train Model' as NavItem, icon: Activity },
    { name: 'Settings' as NavItem, icon: SettingsIcon },
  ];

  return (
    <aside className="w-60 flex-shrink-0 border-r border-slate-200 dark:border-white/5 flex flex-col h-full bg-white/80 dark:bg-[#0F1117]/80 backdrop-blur-md">
      <div className="p-6 mb-4 flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-indigo-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
          <FileText className="w-5 h-5 text-white" />
        </div>
        <span className="font-bold text-lg tracking-tight">Dr Docx</span>
      </div>

      <nav className="flex-1 px-3 space-y-1">
        {navItems.map((item) => (
          <button
            key={item.name}
            onClick={() => setActiveNav(item.name)}
            disabled={isProcessing}
            className={`w-full flex items-center gap-3 px-4 py-3 transition-colors cursor-pointer text-sm rounded-lg
              ${
                activeNav === item.name
                  ? 'bg-indigo-50 dark:bg-indigo-500/10 border-l-2 border-indigo-500 text-indigo-600 dark:text-indigo-400'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-50 dark:hover:bg-white/5'
              }
              ${isProcessing ? 'opacity-50 cursor-not-allowed' : ''}
            `}
          >
            <item.icon className={`w-5 h-5 ${activeNav === item.name ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-500'}`} />
            <span className="font-medium">{item.name}</span>
          </button>
        ))}
      </nav>

      <div className="p-4 border-t border-slate-200 dark:border-white/5 space-y-4">
        <button
          onClick={toggleTheme}
          className="flex items-center gap-3 w-full px-4 py-2 text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 transition-colors"
        >
          {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          <span className="font-medium">{theme === 'dark' ? 'Light Mode' : 'Dark Mode'}</span>
        </button>
        <div className="px-4 text-[10px] uppercase tracking-widest text-slate-500 font-bold">Version 1.0.0</div>
      </div>
    </aside>
  );
}
