const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const api = {
  async request(endpoint, options = {}) {
    const token = localStorage.getItem('nids_token');
    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    };

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
      });

      const data = await response.json().catch(() => null);

      if (!response.ok) {
        throw new Error(data?.detail || data?.message || 'Network request failed');
      }

      return data;
    } catch (err) {
      throw err;
    }
  },

  auth: {
    login(credentials) {
      return api.request('/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
      });
    },
    register(userData) {
      return api.request('/auth/register', {
        method: 'POST',
        body: JSON.stringify(userData),
      });
    },
    getMe() {
      return api.request('/auth/me');
    },
  },
};
