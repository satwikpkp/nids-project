import React from 'react';
import { Shield, AlertTriangle, AlertOctagon, HelpCircle } from 'lucide-react';

export default function DetectionFeedTable({ alerts = [] }) {
  const getBadge = (attackType, isAnomaly, severity) => {
    if (isAnomaly || attackType.includes('UNKNOWN')) {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-mono bg-pink-950/70 text-pink-400 border border-pink-500/50 shadow-[0_0_10px_rgba(236,72,153,0.3)]">
          <HelpCircle className="w-3 h-3" />
          UNKNOWN / ZERO-DAY
        </span>
      );
    }

    if (attackType === 'Normal') {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-mono bg-emerald-950/40 text-emerald-400 border border-emerald-500/30">
          <Shield className="w-3 h-3" />
          NORMAL
        </span>
      );
    }

    if (severity === 'critical' || attackType === 'DoS') {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-mono bg-red-950/70 text-red-400 border border-red-500/50 shadow-[0_0_10px_rgba(239,68,68,0.3)]">
          <AlertOctagon className="w-3 h-3" />
          {attackType.toUpperCase()}
        </span>
      );
    }

    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-mono bg-amber-950/50 text-amber-400 border border-amber-500/40">
        <AlertTriangle className="w-3 h-3" />
        {attackType.toUpperCase()}
      </span>
    );
  };

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-xs font-mono">
        <thead className="bg-slate-900/80 text-slate-400 border-b border-slate-800 text-[11px] uppercase tracking-wider">
          <tr>
            <th className="py-3 px-4">Timestamp</th>
            <th className="py-3 px-4">Source Socket</th>
            <th className="py-3 px-4">Destination Socket</th>
            <th className="py-3 px-4">Protocol</th>
            <th className="py-3 px-4">Classification</th>
            <th className="py-3 px-4 text-right">Confidence</th>
            <th className="py-3 px-4 text-right">Latency</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800/60">
          {alerts.length === 0 ? (
            <tr>
              <td colSpan={7} className="py-8 text-center text-slate-500">
                Awaiting incoming network flow events...
              </td>
            </tr>
          ) : (
            alerts.map((alert) => (
              <tr
                key={alert.id}
                className="hover:bg-slate-900/50 transition-colors group"
              >
                <td className="py-3 px-4 text-slate-400 whitespace-nowrap">
                  {new Date(alert.timestamp).toLocaleTimeString()}
                </td>
                <td className="py-3 px-4 text-cyan-300 whitespace-nowrap">
                  {alert.src_ip}
                  <span className="text-slate-500">:{alert.src_port}</span>
                </td>
                <td className="py-3 px-4 text-slate-300 whitespace-nowrap">
                  {alert.dst_ip}
                  <span className="text-slate-500">:{alert.dst_port}</span>
                </td>
                <td className="py-3 px-4">
                  <span className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] font-semibold">
                    {alert.protocol}
                  </span>
                </td>
                <td className="py-3 px-4">
                  {getBadge(alert.attack_type, alert.is_anomaly, alert.severity)}
                </td>
                <td className="py-3 px-4 text-right">
                  <div className="inline-flex items-center gap-1.5 justify-end">
                    <span className="text-white font-bold">
                      {(alert.confidence * 100).toFixed(1)}%
                    </span>
                    <div className="w-12 h-1.5 bg-slate-800 rounded-full overflow-hidden hidden sm:block">
                      <div
                        className={`h-full ${
                          alert.attack_type === 'Normal' ? 'bg-emerald-500' : 'bg-red-500'
                        }`}
                        style={{ width: `${alert.confidence * 100}%` }}
                      />
                    </div>
                  </div>
                </td>
                <td className="py-3 px-4 text-right text-slate-400 whitespace-nowrap">
                  {alert.inference_time_ms} ms
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
