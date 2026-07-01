/**
 * pages/ChatPage.jsx
 * ───────────────────
 * Full-screen AI chat for a patient.
 * Layout: ChatHistory sidebar (left) + ChatWindow (center) + ChatInput (bottom)
 */
import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { usePatient } from '../hooks/usePatients';
import usePatientStore from '../store/patientStore';
import useChat from '../hooks/useChat';
import ChatHistory from '../components/chat/ChatHistory';
import ChatWindow  from '../components/chat/ChatWindow';
import ChatInput   from '../components/chat/ChatInput';
import '../components/chat/Chat.css';

export default function ChatPage() {
  const { id: patientId } = useParams();
  const { patient }       = usePatient(patientId);
  const { setCurrentPatient } = usePatientStore();

  const {
    sessions, activeSession, messages,
    loadingSessions, loadingMessages, sending,
    messagesEndRef,
    selectSession, startNewSession, sendMessage,
  } = useChat(patientId);

  useEffect(() => { if (patient) setCurrentPatient(patient); }, [patient]);

  return (
    <div style={{
      position: 'fixed',
      top: 'var(--navbar-height)',
      left: 'var(--sidebar-width)',
      right: 0,
      bottom: 0,
      display: 'flex',
      background: 'var(--color-bg-secondary)',
    }}>
      {/* History sidebar */}
      <ChatHistory
        sessions={sessions}
        activeSession={activeSession}
        onSelect={selectSession}
        onNew={startNewSession}
        loading={loadingSessions}
      />

      {/* Main chat area */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <ChatWindow
          messages={messages}
          loading={loadingMessages}
          sending={sending}
          messagesEndRef={messagesEndRef}
          activeSession={activeSession}
        />
        <ChatInput onSend={sendMessage} disabled={sending || !activeSession} />
      </div>
    </div>
  );
}
