import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Shield, Lock, User, Mail, AlertCircle, ArrowRight, CheckCircle2 } from 'lucide-react';

export default function Register({ onSwitchToLogin }) {
  const { register } = useAuth();
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [fullName, setFullName] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('analyst');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      await register({
        email,
        username,
        full_name: fullName,
        password,
        role,
      });
    } catch (err) {
      setError(err.message || 'Registration failed. Please check form inputs.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-void px-4 relative overflow-hidden py-10">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(6,182,212,0.15),rgba(255,255,255,0))] pointer-events-none" />
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-md relative z-10">
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-cyan-950/60 border border-cyan-500/40 text-cyan-400 mb-3 shadow-[0_0_25px_rgba(6,182,212,0.3)]">
            <Shield className="w-7 h-7" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white">
            Register Security Analyst
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Enroll new operator into the NIDS clearance registry
          </p>
        </div>

        <div className="soc-card p-8 bg-surface/80 border border-slate-800">
          {error && (
            <div className="mb-5 p-3 rounded-lg bg-red-950/40 border border-red-500/40 text-red-300 text-xs flex items-start gap-2.5">
              <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-3.5">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">
                Full Name
              </label>
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Agent Alex Vance"
                className="w-full px-3 py-2 text-sm bg-slate-900/90 border border-slate-700/80 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-colors"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Username
                </label>
                <input
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="avance"
                  className="w-full px-3 py-2 text-sm bg-slate-900/90 border border-slate-700/80 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-colors font-mono"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Access Role
                </label>
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  className="w-full px-3 py-2 text-sm bg-slate-900/90 border border-slate-700/80 rounded-lg text-white focus:outline-none focus:border-cyan-500 font-mono"
                >
                  <option value="analyst">Analyst</option>
                  <option value="admin">Administrator</option>
                  <option value="auditor">Auditor</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">
                Official Email
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                  <Mail className="w-4 h-4" />
                </div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="analyst@soc.defense"
                  className="w-full pl-9 pr-3 py-2 text-sm bg-slate-900/90 border border-slate-700/80 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-colors font-mono"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                  <Lock className="w-4 h-4" />
                </div>
                <input
                  type="password"
                  required
                  minLength={6}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••••"
                  className="w-full pl-9 pr-3 py-2 text-sm bg-slate-900/90 border border-slate-700/80 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-colors font-mono"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full mt-3 py-2.5 px-4 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-medium text-sm rounded-lg shadow-[0_0_20px_rgba(6,182,212,0.3)] transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {isSubmitting ? (
                <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  <span>Create Account</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          <div className="mt-5 text-center">
            <button
              type="button"
              onClick={onSwitchToLogin}
              className="text-xs text-slate-400 hover:text-cyan-400 transition-colors"
            >
              Already registered? <span className="text-cyan-400 underline underline-offset-2">Sign in to SOC</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
