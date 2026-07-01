/**
 * store/authStore.js
 * ───────────────────
 * Zustand store for authentication state.
 * Persists user + token in localStorage for page-refresh survival.
 */
import { create } from 'zustand';
import { getMeApi } from '../api/auth';

const useAuthStore = create((set, get) => ({
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  token: localStorage.getItem('access_token') || null,
  isAuthenticated: !!localStorage.getItem('access_token'),
  isLoading: false,

  /** Called after a successful login API response */
  setAuth: (token, user) => {
    localStorage.setItem('access_token', token);
    localStorage.setItem('user', JSON.stringify(user));
    set({ token, user, isAuthenticated: true });
  },

  /** Fetch & refresh the current user profile */
  refreshUser: async () => {
    try {
      const user = await getMeApi();
      localStorage.setItem('user', JSON.stringify(user));
      set({ user });
    } catch {
      get().logout();
    }
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    set({ user: null, token: null, isAuthenticated: false });
  },

  setLoading: (isLoading) => set({ isLoading }),
}));

export default useAuthStore;
