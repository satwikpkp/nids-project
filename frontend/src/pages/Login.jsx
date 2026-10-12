import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Shield, Lock, User, AlertCircle, ArrowRight, Activity, Terminal } from 'lucide-react';

export default function Login({ onSwitchToRegister }) {
  const { login } = useAuth();
  const [identifier, setIdentifier] = useState('admin@soc.defense');
  const [password, setPassword] = useState('Admin@123456');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      await login(identifier, password);
    } catch (err) {
      setError(err.message || 'Authentication failed. Please verify credentials.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-void px-4 relative overflow-hidden">
      {/* Dynamic Cyber Grid & Radial Glow Background */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(6,182,212,0.15),rgba(255,255,255,0))] pointer-events-none" />
      <div className="absolute -top-40 -right-40 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none animate-pulse-slow" />
      <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-md relative z-10">
        {/* Brand Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-cyan-950/60 border border-cyan-500/40 text-cyan-400 mb-4 shadow-[0_0_25px_rgba(6,182,212,0.3)]">
            <Shield className="w-8 h-8" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white flex items-center justify-center gap-2">
            Adaptive NIDS <span className="text-xs px-2 py-0.5 rounded font-mono bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">v1.0</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Autonomous Intrusion Detection & Threat Intelligence
          </p>
        </div>

        {/* Login Panel Card */}
        <div className="soc-card p-8 bg-surface/80 border border-slate-800">
          <div className="flex items-center justify-between pb-6 mb-6 border-b border-slate-800/80">
            <div>
              <h2 className="text-lg font-semibold text-white">Operator Sign In</h2>
              <p className="text-xs text-slate-400">Enter authenticated credentials</p>
            </div>
            <span className="flex items-center gap-1.5 text-xs text-emerald-400 font-mono bg-emerald-950/40 border border-emerald-500/30 px-2.5 py-1 rounded-full">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              SOC LIVE
            </span>
          </div>

          {error && (
            <div className="mb-6 p-3 rounded-lg bg-red-950/40 border border-red-500/40 text-red-300 text-xs flex items-start gap-2.5">
              <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">
                Username or Email
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                  <User className="w-4 h-4" />
                </div>
                <input
                  type="text"
                  required
                  value={identifier}
                  onChange={(e) => setIdentifier(e.target.value)}
                  placeholder="analyst@defense.net"
                  className="w-full pl-9 pr-3 py-2.5 text-sm bg-slate-900/90 border border-slate-700/80 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-colors font-mono"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-xs font-medium text-slate-300">
                  Password
                </label>
                <span className="text-xs text-slate-500">Encrypted AES-256</span>
              </div>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                  <Lock className="w-4 h-4" />
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••••"
                  className="w-full pl-9 pr-3 py-2.5 text-sm bg-slate-900/90 border border-slate-700/80 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-colors font-mono"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full mt-2 py-2.5 px-4 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-medium text-sm rounded-lg shadow-[0_0_20px_rgba(6,182,212,0.3)] transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {isSubmitting ? (
                <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  <span>Authenticate Operator</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          {/* Quick Demo Credentials Helper */}
          <div className="mt-6 pt-5 border-t border-slate-800 text-xs text-slate-400">
            <div className="flex items-center gap-1.5 text-cyan-400 mb-1 font-mono text-[11px]">
              <Terminal className="w-3.5 h-3.5" />
              <span>Default Security Credentials:</span>
            </div>
            <div className="bg-slate-950/60 p-2.5 rounded border border-slate-800/80 font-mono text-[11px] text-slate-300 space-y-0.5">
              <div>User: <span className="text-cyan-300">admin@soc.defense</span></div>
              <div>Pass: <span className="text-cyan-300">Admin@123456</span></div>
            </div>
          </div>

          <div className="mt-4 text-center">
            <button
              type="button"
              onClick={onSwitchToRegister}
              className="text-xs text-slate-400 hover:text-cyan-400 transition-colors"
            >
              Need a new operator account? <span className="text-cyan-400 underline underline-offset-2">Register Analyst</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
