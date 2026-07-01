/**
 * components/common/Sidebar.jsx
 * ──────────────────────────────
 * Fixed left sidebar with navigation links and doctor profile footer.
 */
import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard, Users, MessageSquare, FileText,
  LogOut, Activity, ChevronRight,
} from 'lucide-react';
import useAuthStore from '../../store/authStore';
import { getInitials } from '../../utils/helpers';
import './Sidebar.css';

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/patients',  icon: Users,           label: 'Patients'  },
];

export default function Sidebar() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">
          <Activity size={22} strokeWidth={2.5} />
        </div>
        <div>
          <div className="sidebar-logo-title">MedMemory</div>
          <div className="sidebar-logo-sub">AI Health System</div>
        </div>
      </div>

      {/* Nav */}
      <nav className="sidebar-nav">
        <div className="sidebar-nav-label">Main Menu</div>
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `sidebar-link ${isActive ? 'sidebar-link--active' : ''}`
            }
          >
            <Icon size={18} />
            <span>{label}</span>
            <ChevronRight size={14} className="sidebar-link-arrow" />
          </NavLink>
        ))}
      </nav>

      {/* Bottom: doctor profile */}
      <div className="sidebar-footer">
        <div className="sidebar-user">
          <div className="avatar" style={{ width: 36, height: 36, fontSize: '0.8rem' }}>
            {getInitials(user?.name)}
          </div>
          <div className="sidebar-user-info">
            <div className="sidebar-user-name">{user?.name || 'Doctor'}</div>
            <div className="sidebar-user-email">{user?.email || ''}</div>
          </div>
        </div>
        <button className="sidebar-logout" onClick={handleLogout} title="Logout">
          <LogOut size={16} />
        </button>
      </div>
    </aside>
  );
}
