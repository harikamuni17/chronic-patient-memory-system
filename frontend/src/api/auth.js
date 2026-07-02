/** api/auth.js — Authentication API calls */
import api, { handleApiError } from './axiosInstance';

/**
 * Login with email + password.
 * Returns { access_token, token_type }
 */
export const loginApi = async (email, password) => {
  try {
    // FastAPI's OAuth2 form requires URL-encoded body
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const { data } = await api.post('/api/v1/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return data;
  } catch (error) {
    handleApiError(error, 'Unable to sign in');
  }
};

/** Register a new doctor account */
export const registerApi = async (name, email, password) => {
  try {
    const { data } = await api.post('/api/v1/auth/register', { name, email, password });
    return data;
  } catch (error) {
    handleApiError(error, 'Unable to register doctor');
  }
};

/** Get the profile of the currently logged-in doctor */
export const getMeApi = async () => {
  try {
    const { data } = await api.get('/api/v1/auth/me');
    return data;
  } catch (error) {
    handleApiError(error, 'Unable to load current user');
  }
};
