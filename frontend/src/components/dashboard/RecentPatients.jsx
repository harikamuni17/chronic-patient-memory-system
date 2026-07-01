/** components/dashboard/RecentPatients.jsx */
import { useNavigate } from 'react-router-dom';
import { UserRound, ChevronRight } from 'lucide-react';
import { getInitials, formatDate, genderBadgeClass } from '../../utils/helpers';

export default function RecentPatients({ patients = [] }) {
  const navigate = useNavigate();

  if (!patients.length) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon"><UserRound size={28} /></div>
        <p>No patients yet. Add your first patient to get started.</p>
      </div>
    );
  }

  return (
    <div className="table-wrapper">
      <table className="table">
        <thead>
          <tr>
            <th>Patient</th>
            <th>Age / Gender</th>
            <th>Condition</th>
            <th>Added</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {patients.map((p) => (
            <tr
              key={p.id}
              style={{ cursor: 'pointer' }}
              onClick={() => navigate(`/patients/${p.id}`)}
            >
              <td>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <div className="avatar" style={{ width: 34, height: 34, fontSize: '0.75rem' }}>
                    {getInitials(p.name)}
                  </div>
                  <div>
                    <div style={{ fontWeight: 600, color: 'var(--color-text-primary)', fontSize: '0.875rem' }}>{p.name}</div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)' }}>{p.email || 'No email'}</div>
                  </div>
                </div>
              </td>
              <td>
                <span className={`badge ${genderBadgeClass(p.gender)}`}>
                  {p.age}y · {p.gender}
                </span>
              </td>
              <td style={{ maxWidth: 180, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {p.chronic_conditions || <span style={{ color: 'var(--color-text-muted)' }}>—</span>}
              </td>
              <td>{formatDate(p.created_at)}</td>
              <td>
                <ChevronRight size={16} style={{ color: 'var(--color-text-muted)' }} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
