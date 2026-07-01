/** api/reports.js — PDF Report API calls */
import api from './axiosInstance';

export const uploadReportApi = async (patientId, file, reportType, description) => {
  const formData = new FormData();
  formData.append('file', file);
  if (reportType) formData.append('report_type', reportType);
  if (description) formData.append('description', description);

  const { data } = await api.post(
    `/api/v1/patients/${patientId}/reports/`,
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  );
  return data;
};

export const getReportsApi = async (patientId) => {
  const { data } = await api.get(`/api/v1/patients/${patientId}/reports/`);
  return data;
};

export const deleteReportApi = async (reportId) => {
  await api.delete(`/api/v1/reports/${reportId}`);
};
