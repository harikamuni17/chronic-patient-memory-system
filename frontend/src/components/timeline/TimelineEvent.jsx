/** components/timeline/TimelineEvent.jsx */
import { formatDate, reportTypeBadgeClass } from '../../utils/helpers';
import { FileText, MessageSquare } from 'lucide-react';

export default function TimelineEvent({ event, isLast }) {
  const isReport = event.type === 'report';
  const color = isReport ? '#f87171' : 'var(--color-primary)';

  return (
    <div style={{ display: 'flex', gap: '1rem', position: 'relative' }}>
      {/* Vertical line */}
      {!isLast && (
        <div style={{
          position: 'absolute', left: 15, top: 32, bottom: -8,
          width: 2, background: 'var(--color-border)',
        }} />
      )}

      {/* Icon */}
      <div style={{
        width: 32, height: 32, borderRadius: '50%', flexShrink: 0,
        background: isReport ? 'rgba(239,68,68,0.12)' : 'var(--color-primary-glow)',
        border: `2px solid ${color}`, display: 'flex', alignItems: 'center', justifyContent: 'center',
        zIndex: 1,
      }}>
        {isReport
          ? <FileText size={14} color={color} />
          : <MessageSquare size={14} color={color} />}
      </div>

      {/* Content */}
      <div style={{
        flex: 1, background: 'rgba(255,255,255,0.03)', border: '1px solid var(--color-border)',
        borderRadius: 'var(--radius-md)', padding: '0.625rem 0.875rem', marginBottom: '0.75rem',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '0.5rem' }}>
          <p style={{ fontSize: '0.8125rem', fontWeight: 600, color: 'var(--color-text-primary)' }}>
            {event.title}
          </p>
          <span style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)', flexShrink: 0 }}>
            {formatDate(event.date)}
          </span>
        </div>
        {event.subtitle && (
          <p style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginTop: '0.2rem' }}>
            {event.subtitle}
          </p>
        )}
        {event.badge && (
          <span className={`badge ${reportTypeBadgeClass(event.badge)}`} style={{ marginTop: '0.35rem', fontSize: '0.65rem' }}>
            {event.badge}
          </span>
        )}
      </div>
    </div>
  );
}
