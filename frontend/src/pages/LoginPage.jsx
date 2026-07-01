/**
 * pages/LoginPage.jsx
 * ─────────────────────
 * Full-page animated login with glassmorphism card and gradient background.
 */
import { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import { Activity, Mail, Lock, Eye, EyeOff, LogIn } from 'lucide-react';
import useAuth from '../hooks/useAuth';
import useAuthStore from '../store/authStore';
import './LoginPage.css';

export default function LoginPage() {
  const { isAuthenticated } = useAuthStore();
  const { login, loading }  = useAuth();

  const [email, setEmail]       = useState('admin@hospital.com');
  const [password, setPassword] = useState('Admin@12345');
  const [showPw, setShowPw]     = useState(false);

  if (isAuthenticated) return <Navigate to="/dashboard" replace />;

  const handleSubmit = (e) => {
    e.preventDefault();
    login(email, password);
  };

  return (
    <div className="login-page">
      {/* Animated background orbs */}
      <div className="login-orb login-orb--1" />
      <div className="login-orb login-orb--2" />
      <div className="login-orb login-orb--3" />

      <div className="login-card-wrapper">
        {/* Brand */}
        <div className="login-brand">
          <div className="login-brand-icon">
            <Activity size={28} strokeWidth={2.5} />
          </div>
          <div>
            <h1 className="login-brand-title">MedMemory</h1>
            <p className="login-brand-sub">Chronic Patient Memory System</p>
          </div>
        </div>

        {/* Card */}
        <div className="login-card">
          <div className="login-card-header">
            <h2 className="login-card-title">Welcome back, Doctor</h2>
            <p className="login-card-sub">Sign in to access your patients' AI-powered records.</p>
          </div>

          <form className="login-form" onSubmit={handleSubmit} id="login-form">
            {/* Email */}
            <div className="form-group">
              <label className="form-label" htmlFor="email">Email Address</label>
              <div className="login-input-wrapper">
                <Mail size={16} className="login-input-icon" />
                <input
                  id="email"
                  className="form-input login-input"
                  type="email"
                  placeholder="doctor@hospital.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  autoComplete="email"
                />
              </div>
            </div>

            {/* Password */}
            <div className="form-group">
              <label className="form-label" htmlFor="password">Password</label>
              <div className="login-input-wrapper">
                <Lock size={16} className="login-input-icon" />
                <input
                  id="password"
                  className="form-input login-input"
                  type={showPw ? 'text' : 'password'}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  className="login-pw-toggle"
                  onClick={() => setShowPw((v) => !v)}
                  aria-label={showPw ? 'Hide password' : 'Show password'}
                >
                  {showPw ? <EyeOff size={15} /> : <Eye size={15} />}
                </button>
              </div>
            </div>

            {/* Seed credentials hint */}
            <div className="login-hint">
              <span>Default: <code>admin@hospital.com</code> / <code>Admin@12345</code></span>
            </div>

            <button
              type="submit"
              className="btn btn-primary btn-full btn-lg login-submit"
              disabled={loading}
              id="login-submit-btn"
            >
              {loading ? (
                <><div className="spinner" style={{ width: 18, height: 18 }} /> Signing in…</>
              ) : (
                <><LogIn size={18} /> Sign In</>
              )}
            </button>
          </form>

          <p className="login-footer-text">
            All data is encrypted and stored securely. HIPAA compliant.
          </p>
        </div>
      </div>
    </div>
  );
}
