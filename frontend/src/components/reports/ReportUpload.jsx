/**
 * components/reports/ReportUpload.jsx
 * ──────────────────────────────────────
 * Drag-and-drop PDF uploader with progress feedback.
 */
import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, X, CheckCircle, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import { uploadReportApi } from '../../api/reports';
import { formatFileSize } from '../../utils/helpers';
import { REPORT_TYPE_OPTIONS, MAX_PDF_SIZE_MB } from '../../utils/constants';

export default function ReportUpload({ patientId, onUploaded }) {
  const [file, setFile]             = useState(null);
  const [reportType, setReportType] = useState('');
  const [description, setDesc]      = useState('');
  const [uploading, setUploading]   = useState(false);
  const [status, setStatus]         = useState(null); // 'success' | 'error'

  const onDrop = useCallback((accepted, rejected) => {
    if (rejected.length > 0) {
      toast.error('Please upload a valid PDF (max 20 MB).');
      return;
    }
    setFile(accepted[0]);
    setStatus(null);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxSize: MAX_PDF_SIZE_MB * 1024 * 1024,
    multiple: false,
  });

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setStatus(null);
    try {
      const report = await uploadReportApi(patientId, file, reportType, description);
      setStatus('success');
      toast.success(`"${file.name}" uploaded and indexed!`);
      onUploaded(report);
      setFile(null);
      setReportType('');
      setDesc('');
    } catch (err) {
      setStatus('error');
      toast.error(err?.response?.data?.detail || 'Upload failed.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      {/* Drop zone */}
      <div
        {...getRootProps()}
        style={{
          border: `2px dashed ${isDragActive ? 'var(--color-primary)' : file ? 'var(--color-success)' : 'var(--color-border)'}`,
          borderRadius: 'var(--radius-lg)',
          padding: '2rem',
          textAlign: 'center',
          cursor: 'pointer',
          background: isDragActive ? 'var(--color-primary-glow)' : 'var(--color-bg-input)',
          transition: 'all 0.2s ease',
        }}
      >
        <input {...getInputProps()} />
        {file ? (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem' }}>
            <FileText size={24} color="var(--color-success)" />
            <div style={{ textAlign: 'left' }}>
              <div style={{ fontWeight: 600, fontSize: '0.875rem', color: 'var(--color-text-primary)' }}>{file.name}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>{formatFileSize(file.size)}</div>
            </div>
            <button
              style={{ marginLeft: 'auto', background: 'transparent', border: 'none', color: 'var(--color-text-muted)', cursor: 'pointer' }}
              onClick={(e) => { e.stopPropagation(); setFile(null); }}
            >
              <X size={16} />
            </button>
          </div>
        ) : (
          <>
            <Upload size={32} style={{ margin: '0 auto 0.75rem', color: 'var(--color-text-muted)' }} />
            <p style={{ fontWeight: 600, color: 'var(--color-text-secondary)', marginBottom: '0.25rem' }}>
              {isDragActive ? 'Drop the PDF here' : 'Drag & drop a PDF report'}
            </p>
            <p style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
              or click to browse · PDF only · max {MAX_PDF_SIZE_MB} MB
            </p>
          </>
        )}
      </div>

      {/* Metadata */}
      {file && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
          <div className="form-group">
            <label className="form-label">Report Type</label>
            <select className="form-select" value={reportType} onChange={(e) => setReportType(e.target.value)}>
              <option value="">Select type...</option>
              {REPORT_TYPE_OPTIONS.map((t) => <option key={t}>{t}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Description</label>
            <input className="form-input" placeholder="Optional note..." value={description} onChange={(e) => setDesc(e.target.value)} />
          </div>
        </div>
      )}

      {/* Status feedback */}
      {status === 'success' && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--color-success)', fontSize: '0.8rem' }}>
          <CheckCircle size={16} /> Report uploaded and indexed in ChromaDB successfully.
        </div>
      )}
      {status === 'error' && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--color-danger)', fontSize: '0.8rem' }}>
          <AlertCircle size={16} /> Upload failed. Please try again.
        </div>
      )}

      <button
        className="btn btn-primary"
        onClick={handleUpload}
        disabled={!file || uploading}
        style={{ alignSelf: 'flex-start' }}
      >
        {uploading ? (
          <><div className="spinner" style={{ width: 14, height: 14 }} /> Processing PDF…</>
        ) : (
          <><Upload size={15} /> Upload & Index</>
        )}
      </button>
    </div>
  );
}
