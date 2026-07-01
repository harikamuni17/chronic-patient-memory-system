/** hooks/useAuth.js — Login / logout logic */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { loginApi } from '../api/auth';
import { getMeApi } from '../api/auth';
import useAuthStore from '../store/authStore';
import { getErrorMessage } from '../utils/helpers';

const useAuth = () => {
  const [loading, setLoading] = useState(false);
  const { setAuth, logout } = useAuthStore();
  const navigate = useNavigate();

  const login = async (email, password) => {
    setLoading(true);
    try {
      const { access_token } = await loginApi(email, password);
      // getMeApi uses the token via the interceptor after we store it
      localStorage.setItem('access_token', access_token);
      const freshUser = await getMeApi();
      setAuth(access_token, freshUser);
      toast.success(`Welcome back, ${freshUser.name}!`);
      navigate('/dashboard');
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    toast.success('Logged out successfully.');
    navigate('/login');
  };

  return { login, handleLogout, loading };
};

export default useAuth;
