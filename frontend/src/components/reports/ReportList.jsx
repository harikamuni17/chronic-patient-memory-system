/** components/reports/ReportList.jsx */
import { useState } from 'react';
import { FileText, Trash2, CheckCircle, Clock, Tag } from 'lucide-react';
import toast from 'react-hot-toast';
import { deleteReportApi } from '../../api/reports';
import { formatDate, formatFileSize, reportTypeBadgeClass } from '../../utils/helpers';

export default function ReportList({ reports = [], onDeleted }) {
  const [deletingId, setDeletingId] = useState(null);

  const handleDelete = async (report) => {
    if (!window.confirm(`Delete "${report.original_filename}"?`)) return;
    setDeletingId(report.id);
    try {
      await deleteReportApi(report.id);
      toast.success('Report deleted.');
      onDeleted(report.id);
    } catch {
      toast.error('Failed to delete report.');
    } finally {
      setDeletingId(null);
    }
  };

  if (!reports.length) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon"><FileText size={28} /></div>
        <p>No reports uploaded yet.</p>
        <p style={{ fontSize: '0.8rem' }}>Upload PDF reports above to enable AI-powered queries.</p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.625rem' }}>
      {reports.map((r) => (
        <div key={r.id}
          style={{
            background: 'rgba(255,255,255,0.03)', border: '1px solid var(--color-border)',
            borderRadius: 'var(--radius-md)', padding: '0.875rem 1rem',
            display: 'flex', alignItems: 'center', gap: '0.875rem',
            transition: 'border-color 0.15s',
          }}
          onMouseEnter={(e) => e.currentTarget.style.borderColor = 'rgba(14,165,233,0.25)'}
          onMouseLeave={(e) => e.currentTarget.style.borderColor = 'var(--color-border)'}
        >
          <div style={{ width: 40, height: 40, borderRadius: 'var(--radius-sm)', background: 'rgba(239,68,68,0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
            <FileText size={18} color="#f87171" />
          </div>

          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontWeight: 600, fontSize: '0.8375rem', color: 'var(--color-text-primary)', marginBottom: '0.2rem', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {r.original_filename}
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
              {r.report_type && (
                <span className={`badge ${reportTypeBadgeClass(r.report_type)}`} style={{ fontSize: '0.65rem' }}>
                  <Tag size={10} /> {r.report_type}
                </span>
              )}
              <span style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)' }}>{formatFileSize(r.file_size)}</span>
              <span style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)' }}>{formatDate(r.created_at)}</span>
            </div>
          </div>

          {/* Embedding status */}
          {r.is_embedded ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', fontSize: '0.7rem', color: 'var(--color-success)', flexShrink: 0 }}>
              <CheckCircle size={13} /> Indexed
            </div>
          ) : (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', fontSize: '0.7rem', color: 'var(--color-warning)', flexShrink: 0 }}>
              <Clock size={13} /> Pending
            </div>
          )}

          <button
            className="btn btn-ghost"
            style={{ padding: '0.3rem', color: 'var(--color-danger)', flexShrink: 0 }}
            disabled={deletingId === r.id}
            onClick={() => handleDelete(r)}
            title="Delete report"
          >
            <Trash2 size={15} />
          </button>
        </div>
      ))}
    </div>
  );
}
