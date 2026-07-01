/** components/common/LoadingSpinner.jsx */
export default function LoadingSpinner({ size = 'md', text = '' }) {
  const sizes = { sm: 20, md: 32, lg: 48 };
  const px = sizes[size] || 32;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem', padding: '2rem' }}>
      <div
        style={{
          width: px,
          height: px,
          border: '3px solid rgba(255,255,255,0.08)',
          borderTopColor: 'var(--color-primary)',
          borderRadius: '50%',
          animation: 'spin 0.7s linear infinite',
        }}
      />
      {text && <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>{text}</p>}
    </div>
  );
}

/** Full-page loading overlay */
export function PageLoader({ text = 'Loading...' }) {
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'var(--color-bg-primary)',
    }}>
      <LoadingSpinner size="lg" text={text} />
    </div>
  );
}
