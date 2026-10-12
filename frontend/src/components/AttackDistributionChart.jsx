import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const ATTACK_COLORS = {
  'Normal': '#10B981',
  'DoS': '#EF4444',
  'Reconnaissance': '#F59E0B',
  'Exploits': '#8B5CF6',
  'Fuzzers': '#06B6D4',
  'UNKNOWN / ANOMALOUS': '#EC4899',
  'Generic': '#64748B'
};

export default function AttackDistributionChart({ distribution = {} }) {
  const data = Object.entries(distribution)
    .filter(([_, count]) => count > 0)
    .map(([name, value]) => ({ name, value }));

  if (data.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-xs text-slate-500 font-mono">
        NO TELEMETRY DISTRIBUTION LOGGED
      </div>
    );
  }

  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={55}
            outerRadius={80}
            paddingAngle={4}
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={ATTACK_COLORS[entry.name] || '#3B82F6'}
                stroke="#0B0F17"
                strokeWidth={2}
              />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: '#111827',
              borderColor: '#1E293B',
              borderRadius: '8px',
              color: '#F9FAFB',
              fontSize: '12px',
              fontFamily: 'JetBrains Mono',
              boxShadow: '0 4px 20px rgba(0,0,0,0.5)',
            }}
            formatter={(value, name) => [`${value} flows`, name]}
          />
          <Legend
            verticalAlign="bottom"
            height={36}
            iconType="circle"
            formatter={(value) => (
              <span className="text-[11px] text-slate-300 font-mono mr-2">{value}</span>
            )}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
