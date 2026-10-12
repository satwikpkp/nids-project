import React from 'react';
import { ShieldCheck, AlertTriangle, Flame } from 'lucide-react';

export default function TrafficStatusBadge({ status }) {
  if (status === 'Under Attack') {
    return (
      <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-red-950/60 border border-red-500/60 text-red-400 font-mono text-xs shadow-[0_0_20px_rgba(239,68,68,0.4)]">
        <span className="relative flex h-2.5 w-2.5">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75" />
          <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-red-500" />
        </span>
        <Flame className="w-3.5 h-3.5 text-red-400 animate-pulse" />
        <span className="font-semibold uppercase tracking-wider">UNDER ATTACK</span>
      </div>
    );
  }

  if (status === 'Suspicious') {
    return (
      <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-950/50 border border-amber-500/50 text-amber-400 font-mono text-xs shadow-[0_0_15px_rgba(245,158,11,0.25)]">
        <span className="relative flex h-2.5 w-2.5">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75" />
          <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-amber-500" />
        </span>
        <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
        <span className="font-semibold uppercase tracking-wider">SUSPICIOUS TRAFFIC</span>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-950/40 border border-emerald-500/40 text-emerald-400 font-mono text-xs shadow-[0_0_15px_rgba(16,185,129,0.2)]">
      <span className="relative flex h-2.5 w-2.5">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
        <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500" />
      </span>
      <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
      <span className="font-semibold uppercase tracking-wider">NORMAL OPERATION</span>
    </div>
  );
}
