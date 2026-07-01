/** components/timeline/Timeline.jsx */
import TimelineEvent from './TimelineEvent';
import { Clock } from 'lucide-react';

export default function Timeline({ reports = [], sessions = [] }) {
  // Merge reports and chat sessions into one sorted timeline
  const events = [
    ...reports.map((r) => ({
      id: `report-${r.id}`, type: 'report',
      title: r.original_filename,
      subtitle: r.description || null,
      badge: r.report_type,
      date: r.created_at,
    })),
    ...sessions.map((s) => ({
      id: `session-${s.id}`, type: 'chat',
      title: s.title || 'AI Chat Session',
      subtitle: null, badge: null,
      date: s.created_at,
    })),
  ].sort((a, b) => new Date(b.date) - new Date(a.date));

  if (!events.length) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon"><Clock size={28} /></div>
        <p>No timeline events yet.</p>
        <p style={{ fontSize: '0.8rem' }}>Uploaded reports and AI chats will appear here.</p>
      </div>
    );
  }

  return (
    <div>
      {events.map((ev, i) => (
        <TimelineEvent key={ev.id} event={ev} isLast={i === events.length - 1} />
      ))}
    </div>
  );
}
