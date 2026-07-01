/** components/chat/ChatHistory.jsx — Left sidebar listing past sessions */
import { MessageSquare, Plus, Clock } from 'lucide-react';
import { timeAgo } from '../../utils/helpers';

export default function ChatHistory({ sessions, activeSession, onSelect, onNew, loading }) {
  return (
    <aside className="chat-history-sidebar">
      <div className="chat-history-header">
        <span style={{ fontWeight: 600, fontSize: '0.875rem', color: 'var(--color-text-primary)' }}>
          Conversations
        </span>
        <button className="btn btn-primary btn-sm" onClick={onNew} title="New conversation">
          <Plus size={14} /> New
        </button>
      </div>

      <div className="chat-history-list">
        {loading ? (
          <div style={{ padding: '1rem', textAlign: 'center', color: 'var(--color-text-muted)', fontSize: '0.8rem' }}>
            Loading…
          </div>
        ) : sessions.length === 0 ? (
          <div style={{ padding: '1.5rem 1rem', textAlign: 'center' }}>
            <MessageSquare size={28} style={{ margin: '0 auto 0.5rem', color: 'var(--color-text-muted)' }} />
            <p style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>No conversations yet.</p>
          </div>
        ) : (
          sessions.map((s) => (
            <button
              key={s.id}
              className={`chat-session-item ${activeSession?.id === s.id ? 'chat-session-item--active' : ''}`}
              onClick={() => onSelect(s)}
            >
              <div className="chat-session-icon">
                <MessageSquare size={14} />
              </div>
              <div className="chat-session-info">
                <p className="chat-session-title">{s.title}</p>
                <p className="chat-session-time">
                  <Clock size={10} /> {timeAgo(s.created_at)}
                </p>
              </div>
            </button>
          ))
        )}
      </div>
    </aside>
  );
}
