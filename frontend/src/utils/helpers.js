/** utils/helpers.js — Reusable helper functions */
import { format, formatDistanceToNow, parseISO } from 'date-fns';

/** Format an ISO date string to a readable date */
export const formatDate = (dateStr) => {
  if (!dateStr) return '—';
  try { return format(parseISO(dateStr), 'MMM d, yyyy'); }
  catch { return dateStr; }
};

/** Format ISO date to date + time */
export const formatDateTime = (dateStr) => {
  if (!dateStr) return '—';
  try { return format(parseISO(dateStr), 'MMM d, yyyy · h:mm a'); }
  catch { return dateStr; }
};

/** "3 hours ago" relative timestamps */
export const timeAgo = (dateStr) => {
  if (!dateStr) return '—';
  try { return formatDistanceToNow(parseISO(dateStr), { addSuffix: true }); }
  catch { return dateStr; }
};

/** Convert bytes to human-readable size */
export const formatFileSize = (bytes) => {
  if (!bytes) return '—';
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

/** Get initials from a full name ("John Doe" → "JD") */
export const getInitials = (name = '') => {
  return name
    .split(' ')
    .slice(0, 2)
    .map((w) => w[0]?.toUpperCase() || '')
    .join('');
};

/** Extract a friendly error message from an Axios error */
export const getErrorMessage = (error) => {
  return (
    error?.response?.data?.detail ||
    error?.response?.data?.message ||
    error?.message ||
    'An unexpected error occurred.'
  );
};

/** Gender badge colour helper */
export const genderBadgeClass = (gender) => {
  const g = gender?.toLowerCase();
  if (g === 'male') return 'badge-blue';
  if (g === 'female') return 'badge-purple';
  return 'badge-orange';
};

/** Report type colour helper */
export const reportTypeBadgeClass = (type) => {
  const t = (type || '').toLowerCase();
  if (t.includes('blood')) return 'badge-red';
  if (t.includes('mri') || t.includes('xray') || t.includes('scan')) return 'badge-purple';
  if (t.includes('prescription')) return 'badge-green';
  return 'badge-orange';
};

/** Truncate long strings */
export const truncate = (str = '', max = 60) =>
  str.length > max ? str.slice(0, max) + '…' : str;
