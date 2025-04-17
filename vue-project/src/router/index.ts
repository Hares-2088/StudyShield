import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import { useAuth } from '@/api/authService';

const routes: Array<RouteRecordRaw> = [
  { path: '/', redirect: '/login' },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/shop',
    name: 'Shop',
    component: () => import('@/views/Shop.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/challenges',
    name: 'Challenges',
    component: () => import('@/views/Challenges.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/start-session',
    name: 'StartSession',
    component: () => import('@/views/StudySession.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const { checkAuth, isAuthenticated } = useAuth();
  const isAuth = checkAuth();

  if (to.meta.requiresAuth && !isAuth) {
    next('/login');
  } else if ((to.path === '/login' || to.path === '/register') && isAuth) {
    next('/dashboard');
  } else {
    next();
  }
});

export default router;