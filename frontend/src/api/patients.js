/** api/patients.js — Patient CRUD API calls */
import api, { handleApiError } from './axiosInstance';

const BASE = '/api/v1/patients';

export const getPatientsApi = async ({ skip = 0, limit = 20, search = '' } = {}) => {
  try {
    const params = { skip, limit };
    if (search) params.search = search;
    const { data } = await api.get(`${BASE}/`, { params });
    return data; // { total, patients }
  } catch (error) {
    handleApiError(error, 'Unable to load patients');
  }
};

export const getPatientApi = async (id) => {
  try {
    const { data } = await api.get(`${BASE}/${id}`);
    return data;
  } catch (error) {
    handleApiError(error, 'Unable to load patient');
  }
};

export const getPatientStatsApi = async () => {
  try {
    const { data } = await api.get(`${BASE}/stats`);
    return data;
  } catch (error) {
    handleApiError(error, 'Unable to load patient stats');
  }
};

export const createPatientApi = async (patientData) => {
  try {
    const { data } = await api.post(`${BASE}/`, patientData);
    return data;
  } catch (error) {
    handleApiError(error, 'Unable to create patient');
  }
};

export const updatePatientApi = async (id, patientData) => {
  try {
    const { data } = await api.patch(`${BASE}/${id}`, patientData);
    return data;
  } catch (error) {
    handleApiError(error, 'Unable to update patient');
  }
};

export const deletePatientApi = async (id) => {
  try {
    await api.delete(`${BASE}/${id}`);
  } catch (error) {
    handleApiError(error, 'Unable to delete patient');
  }
};
