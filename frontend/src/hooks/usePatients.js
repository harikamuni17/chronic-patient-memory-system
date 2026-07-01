/** hooks/usePatients.js — Patient CRUD logic */
import { useState, useEffect, useCallback } from 'react';
import toast from 'react-hot-toast';
import {
  getPatientsApi,
  getPatientApi,
  createPatientApi,
  updatePatientApi,
  deletePatientApi,
  getPatientStatsApi,
} from '../api/patients';
import { getErrorMessage } from '../utils/helpers';

/** Hook for paginated + searchable patient list */
export const usePatients = (initialSearch = '') => {
  const [patients, setPatients]   = useState([]);
  const [total, setTotal]         = useState(0);
  const [loading, setLoading]     = useState(false);
  const [search, setSearch]       = useState(initialSearch);
  const [page, setPage]           = useState(0);
  const limit = 12;

  const fetchPatients = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getPatientsApi({ skip: page * limit, limit, search });
      setPatients(data.patients);
      setTotal(data.total);
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [search, page]);

  useEffect(() => { fetchPatients(); }, [fetchPatients]);

  const createPatient = async (formData) => {
    const patient = await createPatientApi(formData);
    toast.success(`Patient "${patient.name}" added successfully!`);
    fetchPatients();
    return patient;
  };

  const updatePatient = async (id, formData) => {
    const patient = await updatePatientApi(id, formData);
    toast.success('Patient record updated.');
    fetchPatients();
    return patient;
  };

  const deletePatient = async (id, name) => {
    await deletePatientApi(id);
    toast.success(`Patient "${name}" deleted.`);
    fetchPatients();
  };

  return {
    patients, total, loading, search, page, limit,
    setSearch, setPage, createPatient, updatePatient,
    deletePatient, refetch: fetchPatients,
  };
};

/** Hook for a single patient */
export const usePatient = (id) => {
  const [patient, setPatient] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchPatient = useCallback(async () => {
    if (!id) return;
    setLoading(true);
    try {
      const data = await getPatientApi(id);
      setPatient(data);
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => { fetchPatient(); }, [fetchPatient]);

  return { patient, loading, refetch: fetchPatient };
};

/** Hook for dashboard stats */
export const usePatientStats = () => {
  const [stats, setStats]   = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    getPatientStatsApi()
      .then(setStats)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return { stats, loading };
};
