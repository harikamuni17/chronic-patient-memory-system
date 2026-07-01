/**
 * pages/DashboardPage.jsx
 * ─────────────────────────
 * Shows stats cards + recent patients table.
 * Also doubles as the /patients route (showPatients prop).
 */
import { Users, FileText, MessageSquare, Activity } from 'lucide-react';
import StatsCard       from '../components/dashboard/StatsCard';
import RecentPatients  from '../components/dashboard/RecentPatients';
import PatientList     from '../components/patients/PatientList';
import LoadingSpinner  from '../components/common/LoadingSpinner';
import { usePatientStats, usePatients } from '../hooks/usePatients';

export default function DashboardPage({ showPatients = false }) {
  const { stats, loading: statsLoading } = usePatientStats();
  const patientsHook = usePatients();

  if (showPatients) {
    return (
      <main className="page-content fade-in">
        <PatientList {...patientsHook} />
      </main>
    );
  }

  return (
    <main className="page-content fade-in">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">Dashboard</h1>
          <p className="page-subtitle">Overview of your patient management system</p>
        </div>
      </div>

      {/* Stats */}
      {statsLoading ? (
        <LoadingSpinner text="Loading stats…" />
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
          <StatsCard icon={Users}         label="Total Patients"  value={stats?.total_patients}      color="blue"   />
          <StatsCard icon={FileText}      label="Reports Uploaded" value={stats?.total_reports}       color="green"  />
          <StatsCard icon={MessageSquare} label="AI Chat Sessions" value={stats?.total_chat_sessions} color="purple" />
          <StatsCard icon={Activity}      label="System Status"    value="Online"                     color="orange" />
        </div>
      )}

      {/* Recent patients */}
      <div className="card-flat" style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
          <h2 className="section-title" style={{ margin: 0 }}>Recent Patients</h2>
          <a href="/patients" className="btn btn-ghost btn-sm" style={{ fontSize: '0.8rem' }}>View all</a>
        </div>
        {patientsHook.loading ? (
          <LoadingSpinner />
        ) : (
          <RecentPatients patients={patientsHook.patients.slice(0, 8)} />
        )}
      </div>
    </main>
  );
}
