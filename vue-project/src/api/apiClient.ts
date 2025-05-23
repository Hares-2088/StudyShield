import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE,
  withCredentials: true,        // to send/receive cookies
});

let isRefreshing = false;
let pendingRequests: Array<() => void> = [];

// Attach interceptors
apiClient.interceptors.response.use(
  r => r,
  async err => {
    const { config, response } = err;
    if (response?.status === 401 && !config._retry) {
      config._retry = true;
      if (!isRefreshing) {
        isRefreshing = true;
        try {
          const refreshRes = await apiClient.post('/auth/refresh');
          const newToken   = refreshRes.data.access_token;
          localStorage.setItem('access_token', newToken);
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
          pendingRequests.forEach(cb => cb());
          pendingRequests = [];
        } catch {
          // redirect to login, etc.
          window.location.href = '/login';
        } finally {
          isRefreshing = false;
        }
      }
      // queue up this request
      return new Promise(resolve => {
        pendingRequests.push(() => {
          config.headers['Authorization'] = `Bearer ${localStorage.getItem('access_token')}`;
          resolve(apiClient(config));
        });
      });
    }
    return Promise.reject(err);
  }
);

// inject the access token on each request
apiClient.interceptors.request.use(cfg => {
  const t = localStorage.getItem('access_token');
  if (t) cfg.headers!['Authorization'] = `Bearer ${t}`;
  return cfg;
});

export default apiClient;
