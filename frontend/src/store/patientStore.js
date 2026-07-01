/**
 * store/patientStore.js
 * ──────────────────────
 * Zustand store for the currently selected patient
 * so any component can read it without prop drilling.
 */
import { create } from 'zustand';

const usePatientStore = create((set) => ({
  currentPatient: null,
  setCurrentPatient: (patient) => set({ currentPatient: patient }),
  clearCurrentPatient: () => set({ currentPatient: null }),
}));

export default usePatientStore;
