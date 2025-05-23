import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import { useAuth } from '@/api/authService';
import StudySession from '@/views/StudySession.vue';
import ActiveStudySession from '@/views/ActiveStudySession.vue';

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
    component: StudySession,
    meta: { requiresAuth: true }
  },
  {
    path: '/active-session/:sessionId',
    name: 'ActiveStudySession',
    component: ActiveStudySession,
    meta: { requiresAuth: true },
    props: true
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

router.beforeEach(async (to, from, next) => {
  const { checkAuth } = useAuth();

  try {
    const isAuth = await checkAuth(); // Ensure checkAuth is awaited if it returns a Promise
    console.log('Authentication status:', isAuth);

    if (to.path === '/' && !isAuth) {
      next('/login'); // Redirect root path to login if not authenticated
    } else if (to.meta.requiresAuth && !isAuth) {
      next('/login'); // Redirect to login if not authenticated
    } else if ((to.path === '/login' || to.path === '/register') && isAuth) {
      next('/dashboard'); // Redirect to dashboard if already authenticated
    } else {
      next(); // Allow navigation for other cases
    }
  } catch (error) {
    console.error('Authentication check failed:', error);
    next('/login'); // Redirect to login if an error occurs during authentication check
  }
});

export default router;