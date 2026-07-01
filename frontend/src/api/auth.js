/** api/auth.js — Authentication API calls */
import api from './axiosInstance';

/**
 * Login with email + password.
 * Returns { access_token, token_type }
 */
export const loginApi = async (email, password) => {
  // FastAPI's OAuth2 form requires URL-encoded body
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);

  const { data } = await api.post('/api/v1/auth/login', formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  return data;
};

/** Register a new doctor account */
export const registerApi = async (name, email, password) => {
  const { data } = await api.post('/api/v1/auth/register', { name, email, password });
  return data;
};

/** Get the profile of the currently logged-in doctor */
export const getMeApi = async () => {
  const { data } = await api.get('/api/v1/auth/me');
  return data;
};
