/** api/patients.js — Patient CRUD API calls */
import api from './axiosInstance';

const BASE = '/api/v1/patients';

export const getPatientsApi = async ({ skip = 0, limit = 20, search = '' } = {}) => {
  const params = { skip, limit };
  if (search) params.search = search;
  const { data } = await api.get(`${BASE}/`, { params });
  return data; // { total, patients }
};

export const getPatientApi = async (id) => {
  const { data } = await api.get(`${BASE}/${id}`);
  return data;
};

export const getPatientStatsApi = async () => {
  const { data } = await api.get(`${BASE}/stats`);
  return data;
};

export const createPatientApi = async (patientData) => {
  const { data } = await api.post(`${BASE}/`, patientData);
  return data;
};

export const updatePatientApi = async (id, patientData) => {
  const { data } = await api.patch(`${BASE}/${id}`, patientData);
  return data;
};

export const deletePatientApi = async (id) => {
  await api.delete(`${BASE}/${id}`);
};
