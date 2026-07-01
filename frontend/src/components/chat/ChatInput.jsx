/** components/chat/ChatInput.jsx */
import { useState, useRef } from 'react';
import { Send, Loader2 } from 'lucide-react';

const SAMPLE_QUESTIONS = [
  'What medications is this patient currently taking?',
  'What are the recent lab results?',
  'Does this patient have any allergies?',
  'Summarise this patient\'s medical history.',
];

export default function ChatInput({ onSend, disabled }) {
  const [value, setValue] = useState('');
  const textareaRef = useRef(null);

  const handleSend = () => {
    const q = value.trim();
    if (!q || disabled) return;
    onSend(q);
    setValue('');
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = (e) => {
    setValue(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 140) + 'px';
  };

  return (
    <div className="chat-input-area">
      {/* Sample questions */}
      <div className="chat-suggestions">
        {SAMPLE_QUESTIONS.map((q) => (
          <button
            key={q}
            className="chat-suggestion-chip"
            onClick={() => { setValue(q); textareaRef.current?.focus(); }}
            disabled={disabled}
          >
            {q}
          </button>
        ))}
      </div>

      {/* Input row */}
      <div className="chat-input-row">
        <textarea
          ref={textareaRef}
          className="chat-textarea"
          placeholder="Ask about this patient's medical history… (Enter to send, Shift+Enter for new line)"
          value={value}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          rows={1}
        />
        <button
          className={`chat-send-btn ${disabled || !value.trim() ? '' : 'chat-send-btn--active'}`}
          onClick={handleSend}
          disabled={disabled || !value.trim()}
          aria-label="Send message"
        >
          {disabled ? <Loader2 size={18} className="animate-spin" /> : <Send size={18} />}
        </button>
      </div>
      <p style={{ fontSize: '0.68rem', color: 'var(--color-text-muted)', textAlign: 'center', marginTop: '0.5rem' }}>
        AI answers are based solely on uploaded patient records.
      </p>
    </div>
  );
}
