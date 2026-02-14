import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to all requests
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle response errors
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear tokens and redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API calls
export const authAPI = {
  register: (email, password, fullName) =>
    axiosInstance.post('/api/v1/auth/register', {
      email,
      password,
      full_name: fullName,
    }),

  login: (email, password) =>
    axiosInstance.post('/api/v1/auth/login', {
      email,
      password,
    }),

  getCurrentUser: () =>
    axiosInstance.get('/api/v1/auth/me'),
};

// Tasks API calls
export const tasksAPI = {
  getTasks: (skip = 0, limit = 100) =>
    axiosInstance.get('/api/v1/tasks', {
      params: { skip, limit },
    }),

  getTask: (taskId) =>
    axiosInstance.get(`/api/v1/tasks/${taskId}`),

  createTask: (title, description) =>
    axiosInstance.post('/api/v1/tasks', {
      title,
      description,
    }),

  updateTask: (taskId, title, description) =>
    axiosInstance.put(`/api/v1/tasks/${taskId}`, {
      title: title !== undefined ? title : undefined,
      description: description !== undefined ? description : undefined,
    }),

  deleteTask: (taskId) =>
    axiosInstance.delete(`/api/v1/tasks/${taskId}`),
};

export default axiosInstance;
