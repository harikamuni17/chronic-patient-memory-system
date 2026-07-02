/** api/reports.js — PDF Report API calls */
import api, { handleApiError } from './axiosInstance';

export const uploadReportApi = async (patientId, file, reportType, description) => {
  try {
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
  } catch (error) {
    handleApiError(error, 'Unable to upload report');
  }
};

export const getReportsApi = async (patientId) => {
  try {
    const { data } = await api.get(`/api/v1/patients/${patientId}/reports/`);
    return data;
  } catch (error) {
    handleApiError(error, 'Unable to load reports');
  }
};

export const deleteReportApi = async (reportId) => {
  try {
    await api.delete(`/api/v1/reports/${reportId}`);
  } catch (error) {
    handleApiError(error, 'Unable to delete report');
  }
};
