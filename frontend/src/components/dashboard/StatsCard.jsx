/** components/dashboard/StatsCard.jsx */
export default function StatsCard({ icon: Icon, label, value, color, trend }) {
  const colorMap = {
    blue:   { bg: 'rgba(14,165,233,0.12)',  border: 'rgba(14,165,233,0.2)',  iconBg: 'rgba(14,165,233,0.2)',  iconColor: '#38bdf8' },
    green:  { bg: 'rgba(16,185,129,0.12)',  border: 'rgba(16,185,129,0.2)',  iconBg: 'rgba(16,185,129,0.2)',  iconColor: '#34d399' },
    purple: { bg: 'rgba(139,92,246,0.12)',  border: 'rgba(139,92,246,0.2)',  iconBg: 'rgba(139,92,246,0.2)',  iconColor: '#a78bfa' },
    orange: { bg: 'rgba(245,158,11,0.12)',  border: 'rgba(245,158,11,0.2)',  iconBg: 'rgba(245,158,11,0.2)',  iconColor: '#fbbf24' },
  };
  const c = colorMap[color] || colorMap.blue;

  return (
    <div style={{
      background: c.bg,
      border: `1px solid ${c.border}`,
      borderRadius: 'var(--radius-lg)',
      padding: '1.5rem',
      display: 'flex',
      alignItems: 'center',
      gap: '1.25rem',
      transition: 'transform 0.2s ease, box-shadow 0.2s ease',
      cursor: 'default',
    }}
    onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-3px)'; e.currentTarget.style.boxShadow = '0 8px 30px rgba(0,0,0,0.3)'; }}
    onMouseLeave={e => { e.currentTarget.style.transform = ''; e.currentTarget.style.boxShadow = ''; }}
    >
      <div style={{
        width: 52, height: 52, borderRadius: '0.75rem',
        background: c.iconBg, display: 'flex',
        alignItems: 'center', justifyContent: 'center',
        flexShrink: 0,
      }}>
        <Icon size={24} color={c.iconColor} />
      </div>
      <div>
        <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.25rem' }}>
          {label}
        </div>
        <div style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--color-text-primary)', lineHeight: 1 }}>
          {value ?? '—'}
        </div>
        {trend && (
          <div style={{ fontSize: '0.7rem', color: 'var(--color-success)', marginTop: '0.25rem' }}>{trend}</div>
        )}
      </div>
    </div>
  );
}
