/**
 * components/patients/PatientList.jsx
 * ──────────────────────────────────────
 * Searchable, paginated grid of PatientCards with delete confirmation.
 */
import { useState } from 'react';
import { Search, UserPlus, AlertTriangle } from 'lucide-react';
import PatientCard  from './PatientCard';
import PatientForm  from './PatientForm';
import LoadingSpinner from '../common/LoadingSpinner';

export default function PatientList({
  patients, total, loading, search, page, limit,
  setSearch, setPage, createPatient, updatePatient, deletePatient,
}) {
  const [showAdd, setShowAdd]       = useState(false);
  const [editTarget, setEditTarget] = useState(null);
  const [deleteTarget, setDeleteTarget] = useState(null);
  const [deleting, setDeleting]     = useState(false);
  const totalPages = Math.ceil(total / limit);

  const handleDelete = async () => {
    setDeleting(true);
    await deletePatient(deleteTarget.id, deleteTarget.name);
    setDeleting(false);
    setDeleteTarget(null);
  };

  return (
    <div>
      {/* Toolbar */}
      <div className="page-header">
        <div>
          <h1 className="page-title">Patients</h1>
          <p className="page-subtitle">{total} patient{total !== 1 ? 's' : ''} under your care</p>
        </div>
        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          <div className="search-wrapper" style={{ width: 260 }}>
            <Search size={15} className="search-icon" />
            <input
              className="search-input"
              placeholder="Search patients…"
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(0); }}
            />
          </div>
          <button className="btn btn-primary" onClick={() => setShowAdd(true)}>
            <UserPlus size={16} /> Add Patient
          </button>
        </div>
      </div>

      {/* Grid */}
      {loading ? (
        <LoadingSpinner text="Loading patients…" />
      ) : patients.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon"><UserPlus size={28} /></div>
          <p style={{ fontWeight: 600, color: 'var(--color-text-secondary)' }}>No patients found</p>
          <p style={{ fontSize: '0.85rem' }}>{search ? `No results for "${search}"` : 'Click "Add Patient" to add your first patient.'}</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1rem' }}>
          {patients.map((p) => (
            <PatientCard
              key={p.id}
              patient={p}
              onEdit={(pt) => setEditTarget(pt)}
              onDelete={(pt) => setDeleteTarget(pt)}
            />
          ))}
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div style={{ display: 'flex', justifyContent: 'center', gap: '0.5rem', marginTop: '2rem' }}>
          {Array.from({ length: totalPages }, (_, i) => (
            <button
              key={i}
              className={`btn ${i === page ? 'btn-primary' : 'btn-secondary'}`}
              style={{ minWidth: 36, padding: '0.4rem 0.75rem', fontSize: '0.8rem' }}
              onClick={() => setPage(i)}
            >
              {i + 1}
            </button>
          ))}
        </div>
      )}

      {/* Add Modal */}
      {showAdd && (
        <PatientForm
          onClose={() => setShowAdd(false)}
          onSubmit={createPatient}
        />
      )}

      {/* Edit Modal */}
      {editTarget && (
        <PatientForm
          initialData={editTarget}
          onClose={() => setEditTarget(null)}
          onSubmit={(data) => updatePatient(editTarget.id, data)}
        />
      )}

      {/* Delete Confirm */}
      {deleteTarget && (
        <div className="modal-overlay">
          <div className="modal" style={{ maxWidth: 420, textAlign: 'center' }}>
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '1.25rem' }}>
              <div style={{ width: 56, height: 56, borderRadius: '50%', background: 'rgba(239,68,68,0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <AlertTriangle size={26} color="#f87171" />
              </div>
            </div>
            <h3 style={{ fontWeight: 700, marginBottom: '0.5rem' }}>Delete Patient?</h3>
            <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem', marginBottom: '1.5rem' }}>
              This will permanently delete <strong style={{ color: 'var(--color-text-primary)' }}>{deleteTarget.name}</strong> and all their reports and chat history. This action cannot be undone.
            </p>
            <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
              <button className="btn btn-secondary" onClick={() => setDeleteTarget(null)}>Cancel</button>
              <button className="btn btn-danger" onClick={handleDelete} disabled={deleting}>
                {deleting ? 'Deleting…' : 'Yes, Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
