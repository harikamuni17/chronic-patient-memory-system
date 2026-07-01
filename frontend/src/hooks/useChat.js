/** hooks/useChat.js — Chat session + RAG Q&A logic */
import { useState, useEffect, useCallback, useRef } from 'react';
import toast from 'react-hot-toast';
import {
  createSessionApi,
  getSessionsApi,
  getMessagesApi,
  askQuestionApi,
} from '../api/chat';
import { getErrorMessage } from '../utils/helpers';

const useChat = (patientId) => {
  const [sessions, setSessions]       = useState([]);
  const [activeSession, setActiveSession] = useState(null);
  const [messages, setMessages]       = useState([]);
  const [loadingSessions, setLoadingSessions] = useState(false);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [sending, setSending]         = useState(false);
  const messagesEndRef = useRef(null);

  /* ── Scroll to bottom on new message ─────── */
  const scrollToBottom = () =>
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });

  useEffect(scrollToBottom, [messages]);

  /* ── Fetch all sessions for this patient ─── */
  const fetchSessions = useCallback(async () => {
    if (!patientId) return;
    setLoadingSessions(true);
    try {
      const data = await getSessionsApi(patientId);
      setSessions(data);
      // Auto-select the first (most recent) session
      if (data.length > 0 && !activeSession) {
        selectSession(data[0]);
      }
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setLoadingSessions(false);
    }
  }, [patientId]);

  useEffect(() => { fetchSessions(); }, [fetchSessions]);

  /* ── Load messages for a selected session ── */
  const selectSession = useCallback(async (session) => {
    setActiveSession(session);
    setLoadingMessages(true);
    try {
      const msgs = await getMessagesApi(session.id);
      setMessages(msgs);
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setLoadingMessages(false);
    }
  }, []);

  /* ── Start a new session ─────────────────── */
  const startNewSession = async () => {
    try {
      const session = await createSessionApi(patientId, 'New Conversation');
      setSessions((prev) => [session, ...prev]);
      setActiveSession(session);
      setMessages([]);
    } catch (err) {
      toast.error(getErrorMessage(err));
    }
  };

  /* ── Ask a question (RAG) ────────────────── */
  const sendMessage = async (question) => {
    if (!activeSession || !question.trim()) return;
    setSending(true);

    // Optimistically add the user message
    const tempUserMsg = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content: question,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempUserMsg]);

    try {
      const result = await askQuestionApi(activeSession.id, question);
      // Replace temp message + add AI reply
      setMessages((prev) => [
        ...prev.filter((m) => m.id !== tempUserMsg.id),
        result.question_message,
        result.answer_message,
      ]);
      // Update session title in the list
      setSessions((prev) =>
        prev.map((s) =>
          s.id === activeSession.id
            ? { ...s, title: result.question_message.content.slice(0, 60) }
            : s
        )
      );
    } catch (err) {
      setMessages((prev) => prev.filter((m) => m.id !== tempUserMsg.id));
      toast.error(getErrorMessage(err));
    } finally {
      setSending(false);
    }
  };

  return {
    sessions, activeSession, messages,
    loadingSessions, loadingMessages, sending,
    messagesEndRef,
    fetchSessions, selectSession, startNewSession, sendMessage,
  };
};

export default useChat;
