/**
 * api/axiosInstance.js
 * ─────────────────────
 * Preconfigured Axios instance that:
 *   • Reads the base URL from Vite env (falls back to Vite proxy /api)
 *   • Attaches the JWT bearer token from localStorage on every request
 *   • Globally intercepts 401 responses → clears token → redirects to /login
 */

import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 30000, // 30 s (longer for AI responses)
  headers: { 'Content-Type': 'application/json' },
});

/* ── Request interceptor: inject JWT ── */
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

/* ── Response interceptor: handle 401 globally ── */
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      // Avoid infinite redirect loop on the login page itself
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
