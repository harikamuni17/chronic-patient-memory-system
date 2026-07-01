/** pages/NotFoundPage.jsx */
import { useNavigate } from 'react-router-dom';
import { AlertTriangle, Home } from 'lucide-react';

export default function NotFoundPage() {
  const navigate = useNavigate();
  return (
    <div style={{
      minHeight: '100vh', display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      background: 'var(--color-bg-primary)', gap: '1.5rem', textAlign: 'center', padding: '2rem',
    }}>
      <div style={{
        width: 80, height: 80, borderRadius: '1.25rem',
        background: 'rgba(245,158,11,0.12)', border: '1px solid rgba(245,158,11,0.25)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}>
        <AlertTriangle size={36} color="#fbbf24" />
      </div>
      <div>
        <h1 style={{ fontSize: '4rem', fontWeight: 800, color: 'var(--color-text-primary)', lineHeight: 1, marginBottom: '0.5rem' }}>404</h1>
        <p style={{ fontSize: '1.125rem', fontWeight: 600, color: 'var(--color-text-secondary)', marginBottom: '0.5rem' }}>Page Not Found</p>
        <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>The page you are looking for doesn't exist or has been moved.</p>
      </div>
      <button className="btn btn-primary" onClick={() => navigate('/dashboard')}>
        <Home size={16} /> Back to Dashboard
      </button>
    </div>
  );
}
