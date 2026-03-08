import { API_URL } from "../config";
import { storage } from "../storage";
import { jwtDecode } from "jwt-decode";

const getAuthHeaders = async () => {
  const token = await storage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
};

const extractError = (err) =>
  err.response?.data?.message || err.message || "Ошибка";

export const login = async (email, password) => {
  const res = await fetch(`${API_URL}/auth/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  const data = await res.json().catch(() => ({}));
  if (data.status === "error") throw new Error(data.message || "Ошибка входа");
  const token = data.data?.token;
  if (!token) throw new Error("Нет токена");
  await storage.setItem("token", token);
  const decoded = jwtDecode(token);
  const user = data.data?.user || {};
  return { ...decoded, ...user };
};

export const sendRegistrationCode = async (email, password) => {
  const res = await fetch(`${API_URL}/auth/register/send-code/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  const data = await res.json().catch(() => ({}));
  if (data.status === "error") throw new Error(data.message || "Ошибка");
  return data;
};

export const verifyRegistrationCode = async (email, password, code) => {
  const res = await fetch(`${API_URL}/auth/register/verify/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, code }),
  });
  const data = await res.json().catch(() => ({}));
  if (data.status === "error") throw new Error(data.message || "Ошибка");
  const token = data.data?.token;
  if (token) await storage.setItem("token", token);
  const decoded = token ? jwtDecode(token) : {};
  const user = data.data?.user || {};
  return { ...decoded, ...user };
};

export const sendForgotPasswordCode = async (email) => {
  const res = await fetch(`${API_URL}/auth/forgot-password/send-code/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });
  const data = await res.json().catch(() => ({}));
  if (data.status === "error") throw new Error(data.message || "Не удалось отправить код");
  return data;
};

export const verifyForgotPasswordCode = async (email, code, newPassword) => {
  const res = await fetch(`${API_URL}/auth/forgot-password/verify/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, code, new_password: newPassword }),
  });
  const data = await res.json().catch(() => ({}));
  if (data.status === "error") throw new Error(data.message || "Неверный или истёкший код");
  const token = data.data?.token;
  if (!token) throw new Error("Нет токена");
  await storage.setItem("token", token);
  const decoded = jwtDecode(token);
  const user = data.data?.user || {};
  return { ...decoded, ...user };
};

export const loginWithGoogleIdToken = async (idToken) => {
  const res = await fetch(`${API_URL}/auth/google-id-token/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id_token: idToken }),
  });
  const data = await res.json().catch(() => ({}));
  if (data.status === "error") throw new Error(data.message || "Ошибка входа через Google");
  const token = data.data?.token;
  if (!token) throw new Error("Нет токена");
  await storage.setItem("token", token);
  const decoded = jwtDecode(token);
  const user = data.data?.user || {};
  return { ...decoded, ...user };
};

export const logoutAll = async () => {
  try {
    const headers = await getAuthHeaders();
    await fetch(`${API_URL}/auth/logout-all/`, { method: "POST", headers });
  } catch (e) {
    console.warn("logoutAll error:", e);
  }
};

export const check = async () => {
  const token = await storage.getItem("token");
  if (!token) return null;
  const headers = await getAuthHeaders();
  const res = await fetch(`${API_URL}/auth/check/`, { headers });
  const data = await res.json().catch(() => ({}));
  const payload = data?.data ?? data;
  if (payload?.token) {
    await storage.setItem("token", payload.token);
    const decoded = jwtDecode(payload.token);
    const user = payload.user || {};
    return { ...decoded, ...user };
  }
  if (res.status === 401) {
    await storage.removeItem("token");
    await storage.removeItem("currentUser");
    await storage.removeItem("currentUserId");
    await storage.removeItem("userProfile");
  }
  return null;
};
