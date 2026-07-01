/** api/chat.js — AI Chat API calls */
import api from './axiosInstance';

export const createSessionApi = async (patientId, title = 'New Conversation') => {
  const { data } = await api.post(`/api/v1/patients/${patientId}/sessions/`, { patient_id: patientId, title });
  return data;
};

export const getSessionsApi = async (patientId) => {
  const { data } = await api.get(`/api/v1/patients/${patientId}/sessions/`);
  return data;
};

export const getMessagesApi = async (sessionId) => {
  const { data } = await api.get(`/api/v1/sessions/${sessionId}/messages/`);
  return data;
};

export const askQuestionApi = async (sessionId, question) => {
  const { data } = await api.post(`/api/v1/sessions/${sessionId}/ask`, { question });
  return data; // { question_message, answer_message, session_id }
};
