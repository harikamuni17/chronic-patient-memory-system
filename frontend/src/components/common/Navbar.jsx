/**
 * components/common/Navbar.jsx
 * ─────────────────────────────
 * Fixed top navigation bar showing breadcrumb, page title, and doctor info.
 */
import { useLocation, useNavigate } from 'react-router-dom';
import { Bell, ArrowLeft } from 'lucide-react';
import useAuthStore from '../../store/authStore';
import usePatientStore from '../../store/patientStore';
import { getInitials } from '../../utils/helpers';
import './Navbar.css';

const pageTitles = {
  '/dashboard': 'Dashboard',
  '/patients':  'Patients',
};

export default function Navbar() {
  const { user } = useAuthStore();
  const { currentPatient } = usePatientStore();
  const location = useLocation();
  const navigate = useNavigate();

  const isPatientDetail = location.pathname.match(/^\/patients\/\d+/);
  const isChat          = location.pathname.includes('/chat');

  const getTitle = () => {
    if (isChat)          return `AI Chat — ${currentPatient?.name || 'Patient'}`;
    if (isPatientDetail) return currentPatient?.name || 'Patient Details';
    return pageTitles[location.pathname] || 'MedMemory';
  };

  return (
    <header className="navbar">
      <div className="navbar-left">
        {isPatientDetail && (
          <button className="navbar-back" onClick={() => navigate(-1)}>
            <ArrowLeft size={18} />
          </button>
        )}
        <div>
          <h1 className="navbar-title">{getTitle()}</h1>
          {currentPatient && isPatientDetail && (
            <p className="navbar-subtitle">
              {currentPatient.age} yrs · {currentPatient.gender} · {currentPatient.blood_group || 'Blood group unknown'}
            </p>
          )}
        </div>
      </div>

      <div className="navbar-right">
        <button className="navbar-icon-btn" aria-label="Notifications">
          <Bell size={18} />
          <span className="navbar-badge" />
        </button>
        <div className="navbar-user">
          <div>
            <div className="navbar-user-name">{user?.name}</div>
            <div className="navbar-user-role">Attending Doctor</div>
          </div>
          <div className="avatar" style={{ width: 36, height: 36, fontSize: '0.8rem' }}>
            {getInitials(user?.name)}
          </div>
        </div>
      </div>
    </header>
  );
}
