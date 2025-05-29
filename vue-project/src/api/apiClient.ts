// src/api/apiClient.ts
import axios from 'axios'
import router from '@/router'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE,
  withCredentials: true,
})

let hasTriedRefresh = false

apiClient.interceptors.response.use(
  r => r,
  async err => {
    const { config, response } = err

    // only handle 401 once per request
    if (response?.status === 401 && !config._retry) {
      config._retry = true

      // If it's the refresh endpoint itself, bail straight to login
      if (config.url?.endsWith('/auth/refresh') || config.url?.endsWith('/auth/logout')) {
        // clear out tokens so guard will kick in
        localStorage.removeItem('access_token')
        delete apiClient.defaults.headers.common['Authorization']
        router.push({ name: 'Login' })
        return Promise.reject(err)
      }

      // If we've already tried a refresh during this page load, drop into login
      if (hasTriedRefresh) {
        localStorage.removeItem('access_token')
        delete apiClient.defaults.headers.common['Authorization']
        router.push({ name: 'Login' })
        return Promise.reject(err)
      }

      hasTriedRefresh = true

      try {
        // hit your refresh endpoint (will read httponly cookie)
        const { data } = await apiClient.post('/auth/refresh')
        const newToken = data.access_token
        localStorage.setItem('access_token', newToken)
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${newToken}`

        // replay the original request
        config.headers!['Authorization'] = `Bearer ${newToken}`
        return apiClient(config)
      } catch {
        // refresh failed → force logout via router
        localStorage.removeItem('access_token')
        delete apiClient.defaults.headers.common['Authorization']
        router.push({ name: 'Login' })
        return Promise.reject(err)
      }
    }

    return Promise.reject(err)
  }
)

apiClient.interceptors.request.use(cfg => {
  const t = localStorage.getItem('access_token')
  if (t) cfg.headers!['Authorization'] = `Bearer ${t}`
  return cfg
})

export default apiClient
