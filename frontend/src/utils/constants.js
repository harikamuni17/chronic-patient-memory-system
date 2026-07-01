/** utils/constants.js — App-wide constants */

export const ROUTES = {
  LOGIN:          '/login',
  DASHBOARD:      '/dashboard',
  PATIENTS:       '/patients',
  PATIENT_DETAIL: '/patients/:id',
  CHAT:           '/patients/:id/chat',
};

export const GENDER_OPTIONS = ['Male', 'Female', 'Other', 'Prefer not to say'];

export const BLOOD_GROUP_OPTIONS = ['A+', 'A−', 'B+', 'B−', 'AB+', 'AB−', 'O+', 'O−', 'Unknown'];

export const REPORT_TYPE_OPTIONS = [
  'Blood Test',
  'MRI Scan',
  'X-Ray',
  'CT Scan',
  'Ultrasound',
  'Prescription',
  'Lab Report',
  'Discharge Summary',
  'Consultation Notes',
  'ECG / EEG',
  'Other',
];

export const MAX_PDF_SIZE_MB = 20;

/** Number of patients per page on the patient list */
export const PATIENTS_PER_PAGE = 12;

/** Max messages to show before auto-scrolling */
export const MAX_VISIBLE_MESSAGES = 100;
