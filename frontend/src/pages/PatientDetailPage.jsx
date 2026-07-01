/**
 * pages/PatientDetailPage.jsx
 * ─────────────────────────────
 * Full patient profile with tabbed sections:
 *   Overview · Reports · Timeline
 */
import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  User, FileText, Clock, MessageSquare, Edit2,
  Droplets, Phone, Mail, MapPin, AlertCircle, Pill,
} from 'lucide-react';
import { usePatient } from '../hooks/usePatients';
import { usePatients } from '../hooks/usePatients';
import { getReportsApi } from '../api/reports';
import { getSessionsApi } from '../api/chat';
import usePatientStore from '../store/patientStore';
import ReportUpload from '../components/reports/ReportUpload';
import ReportList   from '../components/reports/ReportList';
import Timeline     from '../components/timeline/Timeline';
import PatientForm  from '../components/patients/PatientForm';
import LoadingSpinner from '../components/common/LoadingSpinner';
import { formatDate, genderBadgeClass, getInitials } from '../utils/helpers';

const TABS = [
  { id: 'overview',  label: 'Overview',  icon: User },
  { id: 'reports',   label: 'Reports',   icon: FileText },
  { id: 'timeline',  label: 'Timeline',  icon: Clock },
];

export default function PatientDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { patient, loading, refetch } = usePatient(id);
  const { updatePatient } = usePatients();
  const { setCurrentPatient } = usePatientStore();

  const [tab, setTab]         = useState('overview');
  const [reports, setReports] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [editing, setEditing] = useState(false);

  // Set the global current patient for Navbar
  useEffect(() => { if (patient) setCurrentPatient(patient); }, [patient]);

  // Load reports + sessions for timeline
  useEffect(() => {
    if (!id) return;
    getReportsApi(id).then(setReports).catch(() => {});
    getSessionsApi(id).then(setSessions).catch(() => {});
  }, [id]);

  if (loading) return <main className="page-content"><LoadingSpinner size="lg" text="Loading patient…" /></main>;
  if (!patient) return <main className="page-content"><p style={{ color: 'var(--color-text-muted)' }}>Patient not found.</p></main>;

  const InfoRow = ({ icon: Icon, label, value, color }) => (
    value ? (
      <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start', padding: '0.625rem 0', borderBottom: '1px solid var(--color-border)' }}>
        <Icon size={15} style={{ marginTop: 2, color: color || 'var(--color-text-muted)', flexShrink: 0 }} />
        <div>
          <div style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.125rem' }}>{label}</div>
          <div style={{ fontSize: '0.875rem', color: 'var(--color-text-primary)' }}>{value}</div>
        </div>
      </div>
    ) : null
  );

  const MedSection = ({ icon: Icon, label, value, iconColor }) => (
    value ? (
      <div style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid var(--color-border)', borderRadius: 'var(--radius-md)', padding: '1rem', borderLeft: `3px solid ${iconColor || 'var(--color-primary)'}` }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
          <Icon size={15} color={iconColor} />
          <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>{label}</span>
        </div>
        <p style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', lineHeight: 1.6 }}>{value}</p>
      </div>
    ) : null
  );

  return (
    <main className="page-content fade-in">
      {/* Patient header card */}
      <div className="card-flat" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', flexWrap: 'wrap' }}>
          <div className="avatar avatar-xl">{getInitials(patient.name)}</div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap', marginBottom: '0.375rem' }}>
              <h2 style={{ fontSize: '1.375rem', fontWeight: 800, letterSpacing: '-0.02em' }}>{patient.name}</h2>
              <span className={`badge ${genderBadgeClass(patient.gender)}`}>{patient.gender}</span>
              {patient.blood_group && <span className="badge badge-red"><Droplets size={10} /> {patient.blood_group}</span>}
            </div>
            <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>Age: <strong style={{ color: 'var(--color-text-secondary)' }}>{patient.age}</strong></span>
              {patient.date_of_birth && <span style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>DOB: <strong style={{ color: 'var(--color-text-secondary)' }}>{formatDate(patient.date_of_birth)}</strong></span>}
              <span style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>Added: <strong style={{ color: 'var(--color-text-secondary)' }}>{formatDate(patient.created_at)}</strong></span>
            </div>
          </div>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button className="btn btn-secondary btn-sm" onClick={() => setEditing(true)}>
              <Edit2 size={14} /> Edit
            </button>
            <button className="btn btn-primary btn-sm" onClick={() => navigate(`/patients/${id}/chat`)}>
              <MessageSquare size={14} /> AI Chat
            </button>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="tab-list">
        {TABS.map(({ id: tid, label, icon: Icon }) => (
          <button key={tid} className={`tab-item ${tab === tid ? 'active' : ''}`} onClick={() => setTab(tid)}>
            <Icon size={14} /> {label}
          </button>
        ))}
      </div>

      {/* Tab panels */}
      {tab === 'overview' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }} className="fade-in">
          {/* Contact */}
          <div className="card-flat">
            <h3 className="section-title">Contact Details</h3>
            <InfoRow icon={Phone} label="Phone"   value={patient.contact_number} />
            <InfoRow icon={Mail}  label="Email"   value={patient.email} />
            <InfoRow icon={MapPin} label="Address" value={patient.address} />
          </div>
          {/* Medical */}
          <div className="card-flat">
            <h3 className="section-title">Medical Profile</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              <MedSection icon={AlertCircle} label="Allergies"          value={patient.allergies}          iconColor="#f87171" />
              <MedSection icon={Activity}    label="Chronic Conditions"  value={patient.chronic_conditions}  iconColor="var(--color-primary)" />
              <MedSection icon={Pill}        label="Current Medications" value={patient.current_medications} iconColor="#a78bfa" />
              {patient.notes && <MedSection icon={FileText} label="Doctor's Notes" value={patient.notes} iconColor="var(--color-accent)" />}
            </div>
          </div>
        </div>
      )}

      {tab === 'reports' && (
        <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="card-flat">
            <h3 className="section-title">Upload New Report</h3>
            <ReportUpload
              patientId={id}
              onUploaded={(r) => setReports((prev) => [r, ...prev])}
            />
          </div>
          <div className="card-flat">
            <h3 className="section-title">Uploaded Reports ({reports.length})</h3>
            <ReportList
              reports={reports}
              onDeleted={(rid) => setReports((prev) => prev.filter((r) => r.id !== rid))}
            />
          </div>
        </div>
      )}

      {tab === 'timeline' && (
        <div className="card-flat fade-in">
          <h3 className="section-title">Patient Timeline</h3>
          <Timeline reports={reports} sessions={sessions} />
        </div>
      )}

      {editing && (
        <PatientForm
          initialData={patient}
          onClose={() => setEditing(false)}
          onSubmit={async (data) => { await updatePatient(id, data); refetch(); setEditing(false); }}
        />
      )}
    </main>
  );
}
