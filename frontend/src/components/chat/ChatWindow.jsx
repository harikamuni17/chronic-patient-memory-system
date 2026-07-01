/** components/chat/ChatWindow.jsx — Main chat panel with messages */
import { Bot, MessageSquare, Sparkles } from 'lucide-react';
import ChatMessage from './ChatMessage';
import LoadingSpinner from '../common/LoadingSpinner';
import './Chat.css';

export default function ChatWindow({ messages, loading, sending, messagesEndRef, activeSession }) {
  if (loading) return <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}><LoadingSpinner text="Loading messages…" /></div>;

  if (!activeSession) {
    return (
      <div className="chat-welcome">
        <div className="chat-welcome-icon">
          <Bot size={40} />
        </div>
        <h2 className="chat-welcome-title">AI Medical Assistant</h2>
        <p className="chat-welcome-sub">
          Select a conversation or start a new one to ask questions about this patient's medical history.
        </p>
        <div className="chat-welcome-chips">
          {['What are the current medications?', 'Any recent test results?', 'What conditions does this patient have?'].map((q) => (
            <div key={q} className="chat-welcome-chip">
              <Sparkles size={12} /> {q}
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (!messages.length) {
    return (
      <div className="chat-welcome">
        <div className="chat-welcome-icon"><MessageSquare size={36} /></div>
        <h3 className="chat-welcome-title" style={{ fontSize: '1.125rem' }}>Start Asking Questions</h3>
        <p className="chat-welcome-sub">Type your question below. The AI will answer strictly from this patient's uploaded records.</p>
      </div>
    );
  }

  return (
    <div className="chat-messages">
      {messages.map((msg) => (
        <ChatMessage key={msg.id} message={msg} />
      ))}

      {/* Thinking indicator */}
      {sending && (
        <div className="chat-message chat-message--ai">
          <div className="chat-avatar chat-avatar--ai"><Bot size={15} /></div>
          <div className="chat-bubble chat-bubble--ai chat-bubble--thinking">
            <span className="thinking-dot" /><span className="thinking-dot" /><span className="thinking-dot" />
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}
