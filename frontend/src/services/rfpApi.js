import axios from "axios";

const API_BASE = "http://localhost:8000";

// --- CORE DATA ---

export async function fetchRfps(status = "", search = "") {
  // Build query params: ?status=NEW&search=Cable
  const params = new URLSearchParams();
  if (status && status !== "ALL") params.append("status", status);
  if (search) params.append("search", search);

  const res = await axios.get(`${API_BASE}/rfps/?${params.toString()}`);
  return res.data;
}

export async function fetchLogs() {
  const res = await axios.get(`${API_BASE}/rfps/logs`);
  return res.data;
}

export async function fetchUser() {
  const res = await axios.get(`${API_BASE}/rfps/me`);
  return res.data;
}

// --- ACTIONS ---

export async function createRfp(formData) {
  const res = await axios.post(`${API_BASE}/rfps/`, formData);
  return res.data;
}

export async function triggerScraper() {
  return axios.post(`${API_BASE}/rfps/scrape`);
}

export async function runSalesAgent() {
  return axios.post(`${API_BASE}/rfps/run-sales-agent`);
}

export async function runMainAgent() {
  return axios.post(`${API_BASE}/rfps/run-main-agent`);
}

// Helper to get the full download URL
export function getDownloadUrl(rfpId) {
  return `${API_BASE}/rfps/${rfpId}/download`;
}