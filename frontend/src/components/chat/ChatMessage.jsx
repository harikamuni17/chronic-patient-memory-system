/** components/chat/ChatMessage.jsx */
import { Bot, User } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { formatDateTime } from '../../utils/helpers';

export default function ChatMessage({ message }) {
  const isUser = message.role === 'user';
  const isTemp = String(message.id).startsWith('temp-');

  return (
    <div className={`chat-message ${isUser ? 'chat-message--user' : 'chat-message--ai'}`}>
      {/* Icon */}
      <div className={`chat-avatar ${isUser ? 'chat-avatar--user' : 'chat-avatar--ai'}`}>
        {isUser ? <User size={15} /> : <Bot size={15} />}
      </div>

      <div className="chat-bubble-wrapper">
        <div className={`chat-bubble ${isUser ? 'chat-bubble--user' : 'chat-bubble--ai'} ${isTemp ? 'chat-bubble--pending' : ''}`}>
          {isUser ? (
            <p style={{ margin: 0, lineHeight: 1.6 }}>{message.content}</p>
          ) : (
            <div className="chat-markdown">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
          )}
        </div>
        {!isTemp && (
          <span className="chat-timestamp">{formatDateTime(message.created_at)}</span>
        )}
      </div>
    </div>
  );
}
