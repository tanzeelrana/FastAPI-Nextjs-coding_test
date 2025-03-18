"use client";
import { useState, useEffect } from "react";
import { fetchJobs, createJob, updateJobStatus } from "@/services/api";

export default function Page() {
  const [jobs, setJobs] = useState([]);
  const [assetId, setAssetId] = useState("");

  useEffect(() => {
    fetchJobs().then((res) => setJobs(res.data));
  }, []);

  const handleCreateJob = async () => {
    if (!assetId.trim()) return;
    await createJob(assetId);
    setAssetId("");
    fetchJobs().then((res) => setJobs(res.data));
  };

  const handleUpdateStatus = async (id, status) => {
    await updateJobStatus(id, status);
    fetchJobs().then((res) => setJobs(res.data));
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Job Dashboard</h1>

      {/* Job Creation Form */}
      <div className="mb-6 flex gap-2">
        <input
          type="text"
          value={assetId}
          onChange={(e) => setAssetId(e.target.value)}
          placeholder="Enter Asset ID"
          className="border p-2 w-full rounded"
        />
        <button
          onClick={handleCreateJob}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Create Job
        </button>
      </div>

      {/* Job List */}
      <table className="table-auto w-full border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-100">
            <th className="border px-4 py-2">Job ID</th>
            <th className="border px-4 py-2">Asset ID</th>
            <th className="border px-4 py-2">Status</th>
            <th className="border px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map((job) => (
            <tr key={job.id}>
              <td className="border px-4 py-2">{job.id}</td>
              <td className="border px-4 py-2">{job.asset_id}</td>
              <td className="border px-4 py-2">
                <span
                  className={`px-2 py-1 rounded text-white ${
                    job.status === "pending"
                      ? "bg-yellow-500"
                      : job.status === "processing"
                      ? "bg-blue-500"
                      : "bg-green-500"
                  }`}
                >
                  {job.status}
                </span>
              </td>
              <td className="border px-4 py-2 flex gap-2">
                <button
                  onClick={() => handleUpdateStatus(job.id, "processing")}
                  className="bg-yellow-500 text-white px-2 py-1 rounded"
                >
                  Process
                </button>
                <button
                  onClick={() => handleUpdateStatus(job.id, "completed")}
                  className="bg-green-500 text-white px-2 py-1 rounded"
                >
                  Complete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
