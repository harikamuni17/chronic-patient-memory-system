/** components/patients/PatientCard.jsx */
import { useNavigate } from 'react-router-dom';
import { MessageSquare, FileText, Trash2, Edit2, Phone, Droplets } from 'lucide-react';
import { getInitials, genderBadgeClass } from '../../utils/helpers';

export default function PatientCard({ patient, onEdit, onDelete }) {
  const navigate = useNavigate();

  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem', cursor: 'default' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.875rem' }}>
        <div className="avatar avatar-lg">{getInitials(patient.name)}</div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <h3 style={{ fontWeight: 700, fontSize: '0.9375rem', color: 'var(--color-text-primary)', marginBottom: '0.25rem', lineHeight: 1.2 }}>
            {patient.name}
          </h3>
          <span className={`badge ${genderBadgeClass(patient.gender)}`}>
            {patient.age} yrs · {patient.gender}
          </span>
        </div>
        {/* Actions */}
        <div style={{ display: 'flex', gap: '0.25rem' }}>
          <button className="btn btn-ghost" style={{ padding: '0.3rem' }} onClick={() => onEdit(patient)} title="Edit">
            <Edit2 size={14} />
          </button>
          <button className="btn btn-ghost" style={{ padding: '0.3rem', color: 'var(--color-danger)' }} onClick={() => onDelete(patient)} title="Delete">
            <Trash2 size={14} />
          </button>
        </div>
      </div>

      {/* Info rows */}
      {patient.contact_number && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>
          <Phone size={13} /> {patient.contact_number}
        </div>
      )}
      {patient.blood_group && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>
          <Droplets size={13} color="#f87171" /> {patient.blood_group}
        </div>
      )}

      {/* Conditions */}
      {patient.chronic_conditions && (
        <div style={{
          background: 'rgba(255,255,255,0.03)', borderRadius: 'var(--radius-sm)',
          padding: '0.5rem 0.75rem', fontSize: '0.75rem', color: 'var(--color-text-secondary)',
          borderLeft: '2px solid var(--color-primary)', lineHeight: 1.5,
        }}>
          {patient.chronic_conditions.length > 80
            ? patient.chronic_conditions.slice(0, 80) + '…'
            : patient.chronic_conditions}
        </div>
      )}

      {/* Footer buttons */}
      <div style={{ display: 'flex', gap: '0.5rem', marginTop: 'auto', paddingTop: '0.25rem' }}>
        <button
          className="btn btn-secondary"
          style={{ flex: 1, fontSize: '0.75rem', padding: '0.5rem' }}
          onClick={() => navigate(`/patients/${patient.id}`)}
        >
          <FileText size={13} /> Details
        </button>
        <button
          className="btn btn-primary"
          style={{ flex: 1, fontSize: '0.75rem', padding: '0.5rem' }}
          onClick={() => navigate(`/patients/${patient.id}/chat`)}
        >
          <MessageSquare size={13} /> AI Chat
        </button>
      </div>
    </div>
  );
}
