// src/api/authService.ts
import apiClient from './apiClient';
import { ref } from 'vue';

const isAuthenticated = ref(false);
const user = ref(null);

export function useAuth() {

    const login = async (email: string, password: string) => {
        try {
          // build the form body
          const params = new URLSearchParams();
          params.append('username', email);
          params.append('password', password);
      
          // explicitly tell axios to send form data
          const response = await apiClient.post(
            '/auth/token',
            params.toString(),                // serialize to "username=…&password=…"
            {
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
              }
            }
          );
      
          localStorage.setItem('access_token', response.data.access_token);
          isAuthenticated.value = true;
          await fetchUser();
          return true;
        } catch (error: any) {
          console.error('Login failed:', error.response?.data || error.message);
          throw new Error(error.response?.data?.detail || 'Login failed');
        }
      };      

    const register = async (email: string, password: string) => {
        try {
            await apiClient.post('/auth/register', {
                email,
                password,
            });
            return true;
        } catch (error: any) {
            console.error('Registration failed:', error.response?.data || error.message);
            throw new Error(error.response?.data?.detail || 'Registration failed');
        }
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        isAuthenticated.value = false;
        user.value = null;
    };

    const checkAuth = () => {
        const token = localStorage.getItem('access_token');
        isAuthenticated.value = !!token;
        return isAuthenticated.value;
    };

    const fetchUser = async () => {
        try {
            const response = await apiClient.get('/users/me');
            user.value = response.data;
            console.log('User fetched:', user.value);
        } catch (error) {
            console.error('Failed to fetch user:', error);
        }
    };

    const refreshToken = async () => {
        try {
            const response = await apiClient.post('/auth/refresh');
            localStorage.setItem('access_token', response.data.access_token);
            isAuthenticated.value = true;
        } catch (error) {
            console.error('Failed to refresh token:', error);
            logout();
        }
    };

    return {
        login,
        register,
        logout,
        checkAuth,
        fetchUser,
        refreshToken,
        isAuthenticated,
        user,
    };
}