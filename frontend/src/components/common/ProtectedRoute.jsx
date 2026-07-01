/**
 * components/common/ProtectedRoute.jsx
 * ──────────────────────────────────────
 * Guards protected routes. Redirects unauthenticated users to /login.
 * Renders the full app shell (Sidebar + Navbar + content) for auth users.
 */
import { Navigate, Outlet } from 'react-router-dom';
import useAuthStore from '../../store/authStore';
import Sidebar from './Sidebar';
import Navbar  from './Navbar';

export default function ProtectedRoute() {
  const { isAuthenticated } = useAuthStore();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="app-shell">
      <Sidebar />
      <div className="app-main">
        <Navbar />
        <Outlet />
      </div>
    </div>
  );
}
