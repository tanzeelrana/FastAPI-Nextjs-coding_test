import axios from "axios";

const API_URL = "http://localhost:8000";

export const fetchJobs = async () => {
  return await axios.get(`${API_URL}/jobs`);
};

export const createJob = async (assetId) => {
  return await axios.post(`${API_URL}/jobs`, { asset_id: assetId });
};

export const updateJobStatus = async (jobId, status) => {
  return await axios.put(`${API_URL}/jobs/${jobId}/status`, { status });
};
