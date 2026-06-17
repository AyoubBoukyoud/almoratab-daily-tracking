import axios from 'axios';
import { useAuthStore } from '../store/authStore';

// In production, we prefer the relative path '/api' which is handled by Vercel Rewrites
// This avoids Mixed Content issues and CORS problems.
const baseURL = import.meta.env.MODE === 'production'
  ? '/api'
  : (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000');

const client = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
  timeout: 30000, // 30s timeout — HuggingFace Spaces can be slow on cold start
});

// Retry interceptor: handle HuggingFace Spaces cold starts (502/503/504/timeout)
client.interceptors.response.use(undefined, async (error) => {
  const config = error.config;
  if (!config || config._retryCount >= 2) return Promise.reject(error);

  const isRetryable =
    !error.response || // network error / timeout
    [502, 503, 504].includes(error.response.status); // HF Spaces waking up

  if (isRetryable && !config.url?.includes('/auth/login')) {
    config._retryCount = (config._retryCount || 0) + 1;
    const delay = config._retryCount * 3000; // 3s, 6s
    await new Promise((r) => setTimeout(r, delay));
    return client(config);
  }
  return Promise.reject(error);
});

// Request interceptor: attach bearer token to headers
client.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: handle 401 and try refreshing token
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Log auth errors for debugging in production
    if (error.response?.status === 401) {
      const detail = typeof error.response.data === 'object' 
        ? JSON.stringify(error.response.data) 
        : error.response.data;
      console.warn(`[Auth Error] 401 Unauthorized for: ${originalRequest.url}. Detail: ${detail}`);
    }

    // If 401 and we haven't retried yet and it's not a login/refresh attempt
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url.includes('/auth/login') &&
      !originalRequest.url.includes('/auth/refresh')
    ) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return client(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const res = await axios.post(
          `${client.defaults.baseURL}/auth/refresh`,
          {},
          { withCredentials: true }
        );
        const { access_token, user } = res.data;

        // Save new credentials in Zustand
        useAuthStore.getState().setAuth(user, access_token);

        processQueue(null, access_token);
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return client(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        // Refresh token failed -> logout and redirect
        useAuthStore.getState().clearAuth();
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default client;
