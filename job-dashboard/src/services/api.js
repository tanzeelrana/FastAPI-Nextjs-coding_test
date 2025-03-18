import axios from "axios";

const API_URL = "http://localhost:8000";

export const fetchJobs = async () => {
  try {
    const response = await axios.get(`${API_URL}/jobs`);
    return response;
  } catch (error) {
    console.error(
      "Error fetching jobs:",
      error.response?.data || error.message
    );
    throw error;
  }
};

export const createJob = async (assetId) => {
  try {
    const response = await axios.post(`${API_URL}/jobs`, { asset_id: assetId });
    return response;
  } catch (error) {
    console.error("Error creating job:", error.response?.data || error.message);
    throw error;
  }
};

export const updateJobStatus = async (jobId, status) => {
  try {
    const response = await axios.put(`${API_URL}/jobs/${jobId}/status`, {
      status,
    });
    return response;
  } catch (error) {
    console.error(
      `Error updating job ${jobId} to ${status}:`,
      error.response?.data || error.message
    );
    throw error;
  }
};
