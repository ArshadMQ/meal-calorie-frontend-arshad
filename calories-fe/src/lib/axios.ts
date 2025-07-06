"use client";

import axios from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const tokenMatch = document.cookie.match(/token=([^;]+)/);
  const token = tokenMatch ? tokenMatch[1] : null;

  if (token) {
    config.headers.Authorizations = `Bearer ${token}`;
  }

  return config;
});

api.interceptors.response.use(
  (res) => res,
  (error) => {
    console.error("Error from API:", error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default api;
