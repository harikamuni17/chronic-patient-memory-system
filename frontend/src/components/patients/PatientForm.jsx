/**
 * components/patients/PatientForm.jsx
 * ──────────────────────────────────────
 * Reusable modal form for creating and editing patients.
 * Controlled inputs with validation feedback.
 */
import { useState } from 'react';
import { X, UserPlus, Save } from 'lucide-react';
import { GENDER_OPTIONS, BLOOD_GROUP_OPTIONS } from '../../utils/constants';

const EMPTY_FORM = {
  name: '', age: '', gender: 'Male', date_of_birth: '',
  contact_number: '', email: '', address: '',
  blood_group: '', allergies: '', chronic_conditions: '',
  current_medications: '', notes: '',
};

export default function PatientForm({ onClose, onSubmit, initialData = null }) {
  const isEdit = !!initialData;
  const [form, setForm] = useState(isEdit ? { ...EMPTY_FORM, ...initialData } : EMPTY_FORM);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const set = (field, value) => {
    setForm((f) => ({ ...f, [field]: value }));
    if (errors[field]) setErrors((e) => ({ ...e, [field]: '' }));
  };

  const validate = () => {
    const errs = {};
    if (!form.name.trim())    errs.name = 'Name is required.';
    if (!form.age || form.age < 0 || form.age > 150) errs.age = 'Enter a valid age (0–150).';
    if (!form.gender)         errs.gender = 'Gender is required.';
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;
    setLoading(true);
    try {
      const payload = { ...form, age: Number(form.age) };
      // Remove empty strings → send null so backend ignores them
      Object.keys(payload).forEach((k) => { if (payload[k] === '') payload[k] = null; });
      await onSubmit(payload);
      onClose();
    } catch {
      // Error toasts are shown in the hook
    } finally {
      setLoading(false);
    }
  };

  const Field = ({ label, name, type = 'text', placeholder, required }) => (
    <div className="form-group">
      <label className="form-label">{label}{required && <span style={{ color: 'var(--color-danger)', marginLeft: 2 }}>*</span>}</label>
      <input
        className="form-input"
        type={type}
        placeholder={placeholder}
        value={form[name] ?? ''}
        onChange={(e) => set(name, e.target.value)}
        style={errors[name] ? { borderColor: 'var(--color-danger)' } : {}}
      />
      {errors[name] && <span style={{ color: 'var(--color-danger)', fontSize: '0.75rem' }}>{errors[name]}</span>}
    </div>
  );

  return (
    <div className="modal-overlay" onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div className="modal" style={{ maxWidth: 680 }}>
        <div className="modal-header">
          <h2 className="modal-title">{isEdit ? 'Edit Patient' : 'Add New Patient'}</h2>
          <button className="btn btn-ghost" onClick={onClose}><X size={18} /></button>
        </div>

        <form onSubmit={handleSubmit}>
          {/* ── Personal Info ── */}
          <p style={{ fontSize: '0.7rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-text-muted)', marginBottom: '0.75rem' }}>Personal Information</p>

          <div className="form-grid" style={{ marginBottom: '1rem' }}>
            <Field label="Full Name" name="name" placeholder="John Doe" required />
            <Field label="Age" name="age" type="number" placeholder="45" required />
          </div>

          <div className="form-grid" style={{ marginBottom: '1rem' }}>
            <div className="form-group">
              <label className="form-label">Gender <span style={{ color: 'var(--color-danger)' }}>*</span></label>
              <select className="form-select" value={form.gender} onChange={(e) => set('gender', e.target.value)}>
                {GENDER_OPTIONS.map((g) => <option key={g}>{g}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Blood Group</label>
              <select className="form-select" value={form.blood_group || ''} onChange={(e) => set('blood_group', e.target.value)}>
                <option value="">Unknown</option>
                {BLOOD_GROUP_OPTIONS.map((g) => <option key={g}>{g}</option>)}
              </select>
            </div>
          </div>

          <div className="form-grid" style={{ marginBottom: '1rem' }}>
            <Field label="Date of Birth" name="date_of_birth" type="date" />
            <Field label="Contact Number" name="contact_number" placeholder="+91 98765 43210" />
          </div>

          <div className="form-group" style={{ marginBottom: '1rem' }}>
            <Field label="Email Address" name="email" type="email" placeholder="patient@example.com" />
          </div>

          <div className="form-group" style={{ marginBottom: '1.5rem' }}>
            <label className="form-label">Address</label>
            <textarea className="form-textarea" rows={2} placeholder="123 Main St, City..." value={form.address || ''} onChange={(e) => set('address', e.target.value)} />
          </div>

          {/* ── Medical Info ── */}
          <p style={{ fontSize: '0.7rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-text-muted)', marginBottom: '0.75rem' }}>Medical Information</p>

          <div className="form-group" style={{ marginBottom: '1rem' }}>
            <label className="form-label">Allergies</label>
            <textarea className="form-textarea" rows={2} placeholder="Penicillin, Sulfa drugs..." value={form.allergies || ''} onChange={(e) => set('allergies', e.target.value)} />
          </div>

          <div className="form-group" style={{ marginBottom: '1rem' }}>
            <label className="form-label">Chronic Conditions</label>
            <textarea className="form-textarea" rows={2} placeholder="Type 2 Diabetes, Hypertension..." value={form.chronic_conditions || ''} onChange={(e) => set('chronic_conditions', e.target.value)} />
          </div>

          <div className="form-group" style={{ marginBottom: '1rem' }}>
            <label className="form-label">Current Medications</label>
            <textarea className="form-textarea" rows={2} placeholder="Metformin 500mg, Lisinopril 10mg..." value={form.current_medications || ''} onChange={(e) => set('current_medications', e.target.value)} />
          </div>

          <div className="form-group" style={{ marginBottom: '1.5rem' }}>
            <label className="form-label">Doctor's Notes</label>
            <textarea className="form-textarea" rows={2} placeholder="Additional observations..." value={form.notes || ''} onChange={(e) => set('notes', e.target.value)} />
          </div>

          <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end' }}>
            <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? <div className="spinner" style={{ width: 16, height: 16 }} /> : (isEdit ? <Save size={16} /> : <UserPlus size={16} />)}
              {loading ? 'Saving...' : isEdit ? 'Save Changes' : 'Add Patient'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
