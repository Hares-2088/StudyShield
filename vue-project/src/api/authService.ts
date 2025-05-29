// src/api/authService.ts
import apiClient from './apiClient';
import { ref } from 'vue';
import type { User } from '../models/User';
import { useUserStore } from '@/stores/userStore';
import { useRouter } from 'vue-router';

const isAuthenticated = ref(false);
const user = ref<User | null>(null)

export function useAuth() {
    const userStore = useUserStore();
    const router = useRouter();

    const login = async (email: string, password: string) => {
        try {
            // build the form body
            const params = new URLSearchParams();
            params.append('username', email);
            params.append('password', password);

            // explicitly tell axios to send form data
            const response = await apiClient.post(
                '/auth/token',
                params.toString(),
                {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                }
            );

            localStorage.setItem('access_token', response.data.access_token);
            apiClient.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`


            isAuthenticated.value = true;

            // Fetch user data and update the userStore
            await userStore.fetchUserData();

            return true;
        } catch (error: any) {
            console.error('Login failed:', error.response?.data || error.message);
            throw new Error(error.response?.data?.detail || 'Login failed');
        }
    };

    const register = async (data: { name: string; email: string; password: string }) => {
        try {
            await apiClient.post('/auth/register', {
                name: data.name,
                email: data.email,
                password: data.password,
            });
            return true;
        } catch (error: any) {
            console.error('Registration failed:', error.response?.data || error.message);
            throw new Error(error.response?.data?.detail || 'Registration failed');
        }
    };

    const logout = async () => {
        try {
            // tell the server we’re logging out (optional)
            await apiClient.post('/auth/logout');
        } catch (err) {
            // even if it fails, we’ll still clear the token client-side
            console.warn('Logout endpoint failed:', err);
        } finally {
            // 🔑 remove the token so no further calls are authenticated
            localStorage.removeItem('access_token');
            isAuthenticated.value = false;
            user.value = null;

            // redirect to login or home
            router.push({ name: 'Login' });
        }
    };

    const checkAuth = async () => {
        try {
            const response = await apiClient.get('/users/me'); 
            if (response.status === 200 && response.data) {
                isAuthenticated.value = true;
                user.value = response.data;
                return true;
            }
        } catch (error) {
            console.error('Authentication check failed:', error);
            isAuthenticated.value = false;
            user.value = null;
            return false;
        }
    };

    const fetchUser = async () => {
        try {
            const response = await apiClient.get<any>('/users/me');
            const d = response.data;

            // map snake_case → camelCase AND include every required field
            const mapped = {
                id: d._id,
                name: d.name,
                email: d.email,
                coins: d.coins,
                dayStreak: d.day_streak,
                longestStreak: d.longest_streak,
                streak_multiplier: d.streak_multiplier ?? 0,
                lastActiveDate: d.last_active_date,
                challenges: d.challenges,
                milestones: d.milestones,
                purchasedItems: d.purchased_items,
                blockedWebsites: d.blocked_websites,
                totalFocusTime: d.total_focus_time,
                todayFocusTime: d.today_focus_time ?? 0,
                weeklyFocusTime: d.weekly_focus_time,
                monthlyFocusTime: d.monthly_focus_time,
                studyStats: d.study_stats,
                isPhoneLockEnabled: d.is_phone_lock_enabled ?? false,
                isActive: d.is_active,
                role: d.role,
                lastLogin: d.last_login
            } as User;  // <— tell TS “this exactly matches User”

            user.value = mapped;

        } catch (error) {
            console.error('Failed to fetch user:', error);
            user.value = null;
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