/**
 * App.jsx — Root router
 * Defines all application routes with React Router v6.
 * Protected routes redirect to /login when unauthenticated.
 */
import { Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute    from './components/common/ProtectedRoute';
import LoginPage         from './pages/LoginPage';
import DashboardPage     from './pages/DashboardPage';
import PatientDetailPage from './pages/PatientDetailPage';
import ChatPage          from './pages/ChatPage';
import NotFoundPage      from './pages/NotFoundPage';

export default function App() {
  return (
    <Routes>
      {/* Public */}
      <Route path="/login" element={<LoginPage />} />

      {/* Protected — wrapped in shell layout */}
      <Route element={<ProtectedRoute />}>
        <Route path="/dashboard"            element={<DashboardPage />} />
        <Route path="/patients"             element={<DashboardPage showPatients />} />
        <Route path="/patients/:id"         element={<PatientDetailPage />} />
        <Route path="/patients/:id/chat"    element={<ChatPage />} />
      </Route>

      {/* Redirects */}
      <Route path="/"  element={<Navigate to="/dashboard" replace />} />
      <Route path="*"  element={<NotFoundPage />} />
    </Routes>
  );
}
