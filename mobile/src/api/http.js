import { API_URL } from "../config";
import { storage } from "../storage";

export const apiFetch = async (path, options = {}) => {
  const token = await storage.getItem("token");
  const headers = { "Content-Type": "application/json", ...options.headers };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${API_URL}${path}`, { ...options, headers });
  const data = await res.json().catch(() => ({}));
  if (data.status === "error") throw new Error(data.message || "API error");
  return data.data;
};
