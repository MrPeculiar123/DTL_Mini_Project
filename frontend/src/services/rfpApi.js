import axios from "axios";

const API_BASE = "http://localhost:8000";

export async function fetchRfps() {
  const res = await axios.get(`${API_BASE}/rfps`);
  return res.data;
}

export async function createRfp(payload) {
  const res = await axios.post(`${API_BASE}/rfps`, payload);
  return res.data;
}
