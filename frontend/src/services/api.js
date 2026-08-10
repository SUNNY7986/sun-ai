import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// =========================
// Authentication
// =========================

export const registerUser = (data) =>
  API.post("/register", data);

export const loginUser = (formData) =>
  API.post("/login", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

export const getProfile = (token) =>
  API.get("/profile", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

// =========================
// AI Analysis
// =========================

export const analyzeLog = (data) =>
  API.post("/analyze", data);

// =========================
// Dashboard
// =========================

export const getDashboard = () =>
  API.get("/dashboard");

// =========================
// History
// =========================

export const getHistory = () =>
  API.get("/history");

// =========================
// Upload Log
// =========================

export const uploadLog = (formData) =>
  API.post("/upload-log", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

// =========================
// Delete Analysis
// =========================

export const deleteAnalysis = (id) =>
  API.delete(`/analysis/${id}`);

// =========================
// Download Report
// =========================

export const downloadReport = (id) =>
  `${API.defaults.baseURL}/download-report/${id}`;

// =========================

export default API;