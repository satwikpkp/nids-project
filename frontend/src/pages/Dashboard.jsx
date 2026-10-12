import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import TrafficStatusBadge from '../components/TrafficStatusBadge';
import MetricsCard from '../components/MetricsCard';
import AttackDistributionChart from '../components/AttackDistributionChart';
import DetectionFeedTable from '../components/DetectionFeedTable';
import {
  Shield,
  Activity,
  Zap,
  Cpu,
  Layers,
  Radio,
  RefreshCw,
  LogOut,
  Play,
  Server,
  UserCheck
} from 'lucide-react';

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [stats, setStats] = useState({
    status: 'Normal',
    total_packets_analyzed: 1420,
    malicious_packets_count: 86,
    benign_packets_count: 1334,
    attack_ratio: 0.06,
    avg_inference_latency_ms: 1.25,
    cpu_usage_pct: 12.4,
    ram_usage_mb: 245.8,
    packets_per_sec: 240,
    attack_distribution: {
      Normal: 1334,
      DoS: 38,
      Reconnaissance: 22,
      Exploits: 14,
      Fuzzers: 8,
      'UNKNOWN / ANOMALOUS': 4,
    },
  });

  const [alerts, setAlerts] = useState([]);
  const [isSimulating, setIsSimulating] = useState(false);
  const [wsConnected, setWsConnected] = useState(false);

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
  const WS_BASE_URL = import.meta.env.VITE_WS_URL || (
    API_BASE_URL.startsWith('https://') 
      ? API_BASE_URL.replace('https://', 'wss://').replace('/api/v1', '') 
      : API_BASE_URL.replace('http://', 'ws://').replace('/api/v1', '')
  );

  // Fetch initial telemetry stats & alerts
  const fetchData = async () => {
    try {
      const statsRes = await fetch(`${API_BASE_URL}/telemetry/stats`);
      if (statsRes.ok) {
        const statsData = await statsRes.json();
        setStats(statsData);
      }
      const alertsRes = await fetch(`${API_BASE_URL}/alerts?limit=15`);
      if (alertsRes.ok) {
        const alertsData = await alertsRes.json();
        setAlerts(alertsData);
      }
    } catch (err) {
      console.warn('Backend not currently polling REST endpoint:', err);
    }
  };

  useEffect(() => {
    fetchData();

    // WebSocket connection for real-time live push
    let socket;
    try {
      socket = new WebSocket(`${WS_BASE_URL}/ws/telemetry`);
      socket.onopen = () => {
        setWsConnected(true);
      };
      socket.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);
          if (msg.type === 'INITIAL_STATE') {
            setStats(msg.stats);
            setAlerts(msg.recent_alerts);
          } else if (msg.type === 'NEW_ALERT') {
            setStats(msg.stats);
            setAlerts((prev) => [msg.alert, ...prev.slice(0, 24)]);
          }
        } catch (e) {
          console.error(e);
        }
      };
      socket.onclose = () => {
        setWsConnected(false);
      };
    } catch (err) {
      console.warn('WebSocket connect failed', err);
    }

    return () => {
      if (socket) socket.close();
    };
  }, []);

  // Simulate incoming live packet flow
  const triggerSimulation = async () => {
    setIsSimulating(true);
    try {
      const res = await fetch(`${API_BASE_URL}/telemetry/simulate_flow`, {
        method: 'POST',
      });
      if (res.ok) {
        const newAlert = await res.json();
        setAlerts((prev) => [newAlert, ...prev.slice(0, 24)]);
        fetchData();
      }
    } catch (err) {
      console.error('Simulation trigger failed:', err);
    } finally {
      setIsSimulating(false);
    }
  };

  return (
    <div className="min-h-screen bg-void text-gray-100 flex flex-col">
      {/* Top SOC Navbar */}
      <header className="h-16 border-b border-slate-800 bg-surface/70 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-cyan-950/80 border border-cyan-500/40 text-cyan-400 flex items-center justify-center shadow-[0_0_15px_rgba(6,182,212,0.3)]">
            <Shield className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-sm font-bold text-white tracking-wider flex items-center gap-2">
              ADAPTIVE NIDS <span className="text-[10px] text-cyan-400 font-mono">SOC CONSOLE</span>
            </h1>
            <div className="flex items-center gap-2 text-[11px] text-slate-400 font-mono">
              <span className={`inline-block w-2 h-2 rounded-full ${wsConnected ? 'bg-emerald-400' : 'bg-amber-400'}`} />
              <span>{wsConnected ? 'TELEMETRY SOCKET CONNECTED' : 'POLLING MODE'}</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <TrafficStatusBadge status={stats.status} />

          <button
            onClick={triggerSimulation}
            disabled={isSimulating}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-cyan-950/80 hover:bg-cyan-900 border border-cyan-500/40 text-cyan-300 shadow-[0_0_15px_rgba(6,182,212,0.2)] transition-all disabled:opacity-50 font-mono"
          >
            <Play className={`w-3.5 h-3.5 ${isSimulating ? 'animate-spin' : ''}`} />
            <span>Simulate Flow</span>
          </button>

          <div className="h-6 w-px bg-slate-800" />

          <div className="flex items-center gap-2 px-3 py-1 rounded-lg bg-slate-900 border border-slate-800 text-xs">
            <UserCheck className="w-4 h-4 text-emerald-400" />
            <span className="text-slate-300 font-medium">{user?.username || 'Operator'}</span>
            <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 uppercase">
              {user?.role || 'Analyst'}
            </span>
          </div>

          <button
            onClick={logout}
            className="p-1.5 rounded-lg text-slate-400 hover:text-red-400 hover:bg-red-950/30 transition-colors"
            title="Sign Out"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </header>

      {/* Main SOC Dashboard Grid */}
      <main className="flex-1 p-6 max-w-7xl mx-auto w-full space-y-6">
        {/* KPI Cards Row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricsCard
            title="Total Packets Analyzed"
            value={stats.total_packets_analyzed.toLocaleString()}
            subtitle={`${stats.packets_per_sec} packets/sec`}
            icon={Activity}
            trend="Live Stream"
            color="cyan"
          />
          <MetricsCard
            title="Malicious Incursions"
            value={stats.malicious_packets_count.toLocaleString()}
            subtitle={`Incursion Ratio: ${(stats.attack_ratio * 100).toFixed(1)}%`}
            icon={Zap}
            trend={stats.status === 'Normal' ? 'Defended' : 'Alerting'}
            color={stats.malicious_packets_count > 0 ? 'red' : 'emerald'}
          />
          <MetricsCard
            title="Average Latency"
            value={`${stats.avg_inference_latency_ms} ms`}
            subtitle="Tree Ensemble + Scaling"
            icon={Cpu}
            trend="Lightweight"
            color="emerald"
          />
          <MetricsCard
            title="System Footprint"
            value={`${stats.cpu_usage_pct}% CPU`}
            subtitle={`RAM: ${stats.ram_usage_mb} MB`}
            icon={Server}
            trend="Edge Ready"
            color="purple"
          />
        </div>

        {/* Analytics & Machine Learning Visuals Row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Attack Distribution Chart */}
          <div className="soc-card p-5 bg-surface/80 border border-slate-800 lg:col-span-1 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <Layers className="w-4 h-4 text-cyan-400" />
                  Attack Class Distribution
                </h3>
                <span className="text-[10px] font-mono text-slate-500">UNSW-NB15</span>
              </div>
              <p className="text-xs text-slate-400 mb-4">
                Multiclass detection breakdown across heterogeneous ensemble.
              </p>
            </div>

            <AttackDistributionChart distribution={stats.attack_distribution} />
          </div>

          {/* Model Weights & Dynamic Ensemble Panel */}
          <div className="soc-card p-5 bg-surface/80 border border-slate-800 lg:col-span-2">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <Radio className="w-4 h-4 text-violet-400" />
                  Heterogeneous Ensemble & Adaptive Weighting
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Dynamic weight reallocation based on inference confidence & prediction entropy.
                </p>
              </div>
              <button
                onClick={fetchData}
                className="p-1.5 rounded-lg text-slate-400 hover:text-cyan-400 bg-slate-900 border border-slate-800 transition-colors"
                title="Refresh State"
              >
                <RefreshCw className="w-3.5 h-3.5" />
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-5">
              <div className="p-3.5 rounded-xl bg-slate-900/90 border border-slate-800">
                <div className="flex justify-between items-center text-xs mb-1">
                  <span className="font-semibold text-slate-300">Random Forest</span>
                  <span className="font-mono text-cyan-400 font-bold">33%</span>
                </div>
                <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden mb-2">
                  <div className="h-full bg-cyan-400" style={{ width: '33%' }} />
                </div>
                <span className="text-[10px] text-slate-500 font-mono">Variance Dampener</span>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-900/90 border border-slate-800">
                <div className="flex justify-between items-center text-xs mb-1">
                  <span className="font-semibold text-slate-300">XGBoost</span>
                  <span className="font-mono text-blue-400 font-bold">37%</span>
                </div>
                <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden mb-2">
                  <div className="h-full bg-blue-400" style={{ width: '37%' }} />
                </div>
                <span className="text-[10px] text-slate-500 font-mono">Gradient Boundary</span>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-900/90 border border-slate-800">
                <div className="flex justify-between items-center text-xs mb-1">
                  <span className="font-semibold text-slate-300">CatBoost</span>
                  <span className="font-mono text-violet-400 font-bold">30%</span>
                </div>
                <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden mb-2">
                  <div className="h-full bg-violet-400" style={{ width: '30%' }} />
                </div>
                <span className="text-[10px] text-slate-500 font-mono">Categorical Splitter</span>
              </div>
            </div>

            {/* Feature Selection & Zero-Day Summary */}
            <div className="p-4 rounded-xl bg-cyan-950/20 border border-cyan-500/20 flex flex-col sm:flex-row items-center justify-between gap-4">
              <div>
                <h4 className="text-xs font-semibold text-cyan-300 mb-0.5">
                  Intelligent Feature Selection Active
                </h4>
                <p className="text-[11px] text-slate-400">
                  Compressed 49 high-dimensional network flow metrics down to 15 key discriminators via Mutual Information & Random Forest Importance.
                </p>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <span className="px-2.5 py-1 rounded bg-slate-900 border border-cyan-500/40 text-cyan-300 font-mono text-xs">
                  15 / 49 Features
                </span>
                <span className="px-2.5 py-1 rounded bg-pink-950/80 border border-pink-500/40 text-pink-300 font-mono text-xs">
                  Zero-Day Hook Active
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Real-time Detection Feed Table */}
        <div className="soc-card bg-surface/80 border border-slate-800 overflow-hidden">
          <div className="p-5 border-b border-slate-800 flex items-center justify-between">
            <div>
              <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                <Activity className="w-4 h-4 text-emerald-400" />
                Live Network Flow Detection Telemetry
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Streaming ingestion of evaluated flows with confidence rankings and anomaly tags.
              </p>
            </div>
            <span className="text-xs font-mono text-cyan-400 bg-cyan-950/40 border border-cyan-800/60 px-2.5 py-1 rounded-lg">
              Showing {alerts.length} Incursions
            </span>
          </div>

          <DetectionFeedTable alerts={alerts} />
        </div>
      </main>
    </div>
  );
}
