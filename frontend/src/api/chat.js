/** api/chat.js — AI Chat API calls */
import api, { handleApiError } from './axiosInstance';

export const createSessionApi = async (patientId, title = 'New Conversation') => {
  try {
    const { data } = await api.post(`/api/v1/patients/${patientId}/sessions/`, { title });
    return data;
  } catch (error) {
    handleApiError(error, 'Unable to create chat session');
  }
};

export const getSessionsApi = async (patientId) => {
  try {
    const { data } = await api.get(`/api/v1/patients/${patientId}/sessions/`);
    return data;
  } catch (error) {
    handleApiError(error, 'Unable to load chat sessions');
  }
};

export const getMessagesApi = async (sessionId) => {
  try {
    const { data } = await api.get(`/api/v1/sessions/${sessionId}/messages/`);
    return data;
  } catch (error) {
    handleApiError(error, 'Unable to load chat messages');
  }
};

export const askQuestionApi = async (sessionId, question) => {
  try {
    const { data } = await api.post(`/api/v1/sessions/${sessionId}/ask`, { question });
    return data; // { question_message, answer_message, session_id }
  } catch (error) {
    handleApiError(error, 'Unable to ask question');
  }
};
