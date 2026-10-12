import React from 'react';

export default function MetricsCard({ title, value, subtitle, icon: Icon, trend, color = 'cyan' }) {
  const colorStyles = {
    cyan: 'text-cyan-400 border-cyan-500/20 bg-cyan-950/20 shadow-[0_0_15px_rgba(6,182,212,0.1)]',
    emerald: 'text-emerald-400 border-emerald-500/20 bg-emerald-950/20 shadow-[0_0_15px_rgba(16,185,129,0.1)]',
    red: 'text-red-400 border-red-500/20 bg-red-950/20 shadow-[0_0_15px_rgba(239,68,68,0.1)]',
    amber: 'text-amber-400 border-amber-500/20 bg-amber-950/20 shadow-[0_0_15px_rgba(245,158,11,0.1)]',
    purple: 'text-violet-400 border-violet-500/20 bg-violet-950/20 shadow-[0_0_15px_rgba(139,92,246,0.1)]',
  }[color] || 'text-cyan-400 border-cyan-500/20 bg-cyan-950/20';

  return (
    <div className="soc-card p-5 bg-surface/70 border border-slate-800 relative overflow-hidden group">
      <div className="flex items-start justify-between">
        <div>
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wider block mb-1">
            {title}
          </span>
          <div className="text-2xl font-extrabold text-white font-mono tracking-tight group-hover:text-cyan-300 transition-colors">
            {value}
          </div>
        </div>

        <div className={`p-2.5 rounded-xl border ${colorStyles}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
        <span className="text-slate-400">{subtitle}</span>
        {trend && (
          <span className="font-mono text-[11px] text-cyan-400 bg-cyan-950/50 px-2 py-0.5 rounded border border-cyan-800/50">
            {trend}
          </span>
        )}
      </div>
    </div>
  );
}
